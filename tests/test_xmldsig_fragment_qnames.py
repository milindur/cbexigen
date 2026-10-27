# SPDX-License-Identifier: Apache-2.0
"""Regression coverage for xmldsig fragment XML QName rendering."""

import re
import tempfile
import xml.etree.ElementTree as ET

from test_element_fragment_grammar import generate, require_schema

XMLDSIG_NS = "http://www.w3.org/2000/09/xmldsig#"


def test_generated_xmldsig_fragment_tags_are_prefixed_qnames():
    require_schema()
    with tempfile.TemporaryDirectory(prefix="cbexigen-xmldsig-qnames-") as work_dir:
        code_root = generate(work_dir, xml_output=True)
        source = (code_root / "iso-2" / "iso2_msgDefDecoder.c").read_text()
    fragment_fn = source.split("int decode_iso2_xmldsigFragment", 1)[1].split("return error;", 1)[0]

    tag_names = re.findall(r'"<(/?)([^>"\s]+)[>"\s]', fragment_fn)
    assert tag_names

    for is_close, name in tag_names:
        assert "{" not in name
        assert name.startswith("ns")
        assert ":" in name

        if not is_close:
            prefix = name.split(":", 1)[0]
            ET.fromstring(f'<{name} xmlns:{prefix}="{XMLDSIG_NS}"/>')
