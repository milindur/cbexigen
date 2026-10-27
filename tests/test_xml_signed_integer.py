# SPDX-License-Identifier: Apache-2.0
"""XML output of arbitrary-width EXI signed integers (e.g. X509SerialNumber).

EXI codes a negative integer as its sign plus magnitude m for the value
-(m + 1). Values beyond int64 must still be written as exact decimals.
"""
import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

from test_element_fragment_grammar import generate, require_schema

DRIVER = Path(__file__).resolve().parent / 'xml_signed_driver.c'
MAGNITUDES = [0, 1, 9, 10, 255, 256, 2**63 - 1, 2**63, 2**64, 2**159 + 12345, 2**232 - 1]


class XmlSignedIntegerTest(unittest.TestCase):
    def test_signed_values_are_exact_decimals(self):
        require_schema()
        compiler = os.environ.get('CC') or shutil.which('cc') or shutil.which('gcc')
        if compiler is None:
            raise unittest.SkipTest('no C compiler found')
        with tempfile.TemporaryDirectory(prefix='cbexigen-xml-signed-') as work_dir:
            code_root = generate(work_dir, xml_output=True)
            binary = Path(work_dir) / 'xml_signed_driver'
            sources = sorted((code_root / 'common').glob('*.c')) + [code_root / 'iso-2' / 'iso2_msgDefDatatypes.c']
            subprocess.run([compiler, '-std=c11', '-o', str(binary), str(DRIVER)] + [str(s) for s in sources]
                           + ['-I', str(code_root / 'common'), '-I', str(code_root / 'iso-2')],
                           check=True, capture_output=True)
            for magnitude in MAGNITUDES:
                magnitude_hex = format(magnitude, 'x') if magnitude else ''
                magnitude_hex = magnitude_hex.zfill(len(magnitude_hex) + len(magnitude_hex) % 2)
                for negative in (False, True):
                    with self.subTest(magnitude=magnitude, negative=negative):
                        result = subprocess.run([str(binary), '1' if negative else '0', magnitude_hex],
                                                capture_output=True, text=True, check=True)
                        expected = -(magnitude + 1) if negative else magnitude
                        self.assertEqual(result.stdout.strip(), str(expected))


if __name__ == '__main__':
    unittest.main()
