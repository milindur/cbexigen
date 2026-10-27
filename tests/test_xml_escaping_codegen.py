# SPDX-License-Identifier: Apache-2.0
"""Regression coverage for generated XML escaping code helpers."""

from pathlib import Path

import sys

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from cbexigen.decoder_classes import ExiDecoderCode  # noqa: E402


def test_c_string_literal_escapes_generated_enum_source_text():
    literal = ExiDecoderCode._ExiDecoderCode__c_string_literal('A&B<"\\\n\r\t')

    assert literal == 'A&B<\\"\\\\\\n\\r\\t'


def test_xml_enum_literals_keep_utf8_byte_lengths_for_generated_c_writes():
    decoder = object.__new__(ExiDecoderCode)

    [(literal, byte_length)] = decoder._ExiDecoderCode__xml_enum_literals(['A&B<"é'])

    assert literal == 'A&B<\\"é'
    assert byte_length == len('A&B<"é'.encode('utf-8'))


def test_generated_decoder_defines_separate_text_and_attribute_escape_helpers():
    source = (REPO_ROOT / "src" / "cbexigen" / "decoder_classes.py").read_text()

    assert "xml_write_escaped_text" in source
    assert "xml_write_escaped_attr" in source
    assert "&quot;" in source
    assert "&amp;" in source
    assert "&lt;" in source
