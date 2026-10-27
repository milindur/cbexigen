# SPDX-License-Identifier: Apache-2.0
"""XML output of ISO 15118-2 fragment roots.

Decodes the Exificient eMAID vectors (element fragment grammar) and a
SignatureValue round trip with generate_xml_output = 1 and checks that the XML
is well formed, carries Id as an attribute of the fragment root and the value
as its text. Skips like test_element_fragment_grammar.
"""
import shutil
import subprocess
import tempfile
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

from test_element_fragment_grammar import compile_driver, generate, read_vectors, require_schema

DRIVER = Path(__file__).resolve().parent / 'emaid_fragment_xml_driver.c'
SIGNATURE_DRIVER = Path(__file__).resolve().parent / 'signature_value_xml_driver.c'
XMLDSIG_NS = 'http://www.w3.org/2000/09/xmldsig#'
BODY_NS = 'urn:iso:15118:2:2013:MsgBody'
DATATYPES_NS = 'urn:iso:15118:2:2013:MsgDataTypes'


class ElementFragmentXmlTest(unittest.TestCase):
    work_dir = None
    code_root = None

    @classmethod
    def setUpClass(cls):
        require_schema()
        cls.work_dir = tempfile.mkdtemp(prefix='cbexigen-fragment-xml-test-')
        cls.code_root = generate(cls.work_dir, xml_output=True)

    @classmethod
    def tearDownClass(cls):
        if cls.work_dir:
            shutil.rmtree(cls.work_dir, ignore_errors=True)

    def test_signature_value_simple_content_is_root_text(self):
        binary = compile_driver(self.code_root, self.work_dir, SIGNATURE_DRIVER)
        result = subprocess.run([str(binary)], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        root = ET.fromstring(result.stdout)
        self.assertEqual(root.tag, f'{{{XMLDSIG_NS}}}SignatureValue')
        self.assertEqual(root.attrib, {'Id': 'A'})
        self.assertEqual(root.text, 'QQ==')
        self.assertEqual(len(root), 0)

    def test_emaid_fragment_xml(self):
        binary = compile_driver(self.code_root, self.work_dir, DRIVER)
        for identifier, value, exi_hex in read_vectors():
            with self.subTest(Id=identifier):
                result = subprocess.run([str(binary), exi_hex], capture_output=True, text=True)
                self.assertEqual(result.returncode, 0, result.stderr)
                root = ET.fromstring(result.stdout)
                self.assertEqual(root.tag, f'{{{BODY_NS}}}eMAID')
                # MsgDataTypes declares attributeFormDefault="qualified"
                self.assertEqual(root.attrib, {f'{{{DATATYPES_NS}}}Id': identifier})
                self.assertEqual(root.text, value)


if __name__ == '__main__':
    unittest.main()
