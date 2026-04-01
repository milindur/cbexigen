# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2022 - 2023 chargebyte GmbH
# Copyright (c) 2022 - 2023 Contributors to EVerest

""" Tools for the Exi Codegenerator config """
import hashlib
import importlib
import io
import urllib.request
import zipfile

from typing import Union, Dict
from pathlib import Path

CONFIG_ARGS: Dict[str, Union[str, Path]] = {
    'program_dir': '',
    'config_file': '',
    'log_dir': '',
    'template_dir': '',
    'output_dir': '',
    'schema_base_dir': ''
}

CONFIG_PARAMS: Dict[str, Union[str, int]] = {
    # add debug code while generating code
    'add_debug_code': 0,
    # generate analysis tree while generating code
    'generate_analysis_tree': 0,
    'generate_analysis_tree_20': 0,
    # root structure definitions
    'root_struct_name': 'exiDocument',
    'root_parameter_name': 'exiDoc',
    # name addendum definitions
    'array_define_addendum': '_ARRAY_SIZE',
    'char_define_addendum': '_CHARACTER_SIZE',
    # name prefix definitions
    'init_function_prefix': 'init_',
    'encode_function_prefix': 'encode_',
    'decode_function_prefix': 'decode_',
    'choice_sequence_prefix': 'choice_',
    # do optimizations
    'apply_optimizations': 0,
    # generate fragment de- and encoder
    'generate_fragments': 0,
    # fragment structure definitions
    'fragment_struct_name': 'exiFragment',
    'fragment_parameter_name': 'exiFrag',
    'xmldsig_fragment_struct_name': 'xmldsigFragment',
    'xmldsig_fragment_parameter_name': 'xmldsigFrag',
    # general c-code style
    'c_code_indent_chars': 4,
    'c_replace_chars': [' ', '-'],
}

__CONFIG_MODULE = None


def check_config_file():
    result = True

    if not Path(CONFIG_ARGS['program_dir'], CONFIG_ARGS['config_file']).resolve().exists():
        result = False

    return result


def set_config_arg_from_config_file(arg_name: str, config_dir: str):
    CONFIG_ARGS[arg_name] = Path(CONFIG_ARGS['program_dir'], config_dir).resolve()


def get_config_module():
    global __CONFIG_MODULE

    if __CONFIG_MODULE is None:
        config_module_name = Path(CONFIG_ARGS['config_file']).name
        if config_module_name.endswith('.py'):
            config_module_name = config_module_name[:-3]
        __CONFIG_MODULE = importlib.import_module(config_module_name)

    return __CONFIG_MODULE


def get_fragment_parameter_for_schema(schema_prefix):
    fragments = []

    config_module = get_config_module()
    parameter = schema_prefix + 'fragments'
    if hasattr(config_module, parameter):
        fragments = getattr(config_module, parameter)

    return fragments


def check_config_parameters():
    result = True

    if not Path(CONFIG_ARGS['output_dir']).exists():
        Path(CONFIG_ARGS['output_dir']).mkdir(parents=True, exist_ok=True)

    if not Path(CONFIG_ARGS['log_dir']).exists():
        Path(CONFIG_ARGS['log_dir']).mkdir(parents=True, exist_ok=True)

    return result


def process_config_parameters():
    """
        Checks the config file for parameters and overwrites defaults
        with the values from config file
    """
    config_module = get_config_module()

    ''' debug code definitions '''
    # add_debug_code
    if hasattr(config_module, 'add_debug_code'):
        CONFIG_PARAMS['add_debug_code'] = config_module.add_debug_code

    ''' analysis tree definitions '''
    # generate_analysis_tree
    if hasattr(config_module, 'generate_analysis_tree'):
        CONFIG_PARAMS['generate_analysis_tree'] = config_module.generate_analysis_tree
    # generate_analysis_tree_20
    if hasattr(config_module, 'generate_analysis_tree_20'):
        CONFIG_PARAMS['generate_analysis_tree_20'] = config_module.generate_analysis_tree_20

    ''' root structure definitions '''
    # root_struct_name
    if hasattr(config_module, 'root_struct_name'):
        CONFIG_PARAMS['root_struct_name'] = config_module.root_struct_name
    # root_parameter_name
    if hasattr(config_module, 'root_parameter_name'):
        CONFIG_PARAMS['root_parameter_name'] = config_module.root_parameter_name

    ''' name addendum definitions '''
    # array_define_addendum
    if hasattr(config_module, 'array_define_addendum'):
        CONFIG_PARAMS['array_define_addendum'] = config_module.array_define_addendum
    # char_define_addendum
    if hasattr(config_module, 'char_define_addendum'):
        CONFIG_PARAMS['char_define_addendum'] = config_module.char_define_addendum
    # byte_define_addendum
    if hasattr(config_module, 'byte_define_addendum'):
        CONFIG_PARAMS['byte_define_addendum'] = config_module.byte_define_addendum

    ''' name prefix definitions '''
    # init_function_prefix
    if hasattr(config_module, 'init_function_prefix'):
        CONFIG_PARAMS['init_function_prefix'] = config_module.init_function_prefix
    # encode_function_prefix
    if hasattr(config_module, 'encode_function_prefix'):
        CONFIG_PARAMS['encode_function_prefix'] = config_module.encode_function_prefix
    # decode_function_prefix
    if hasattr(config_module, 'decode_function_prefix'):
        CONFIG_PARAMS['decode_function_prefix'] = config_module.decode_function_prefix
    # choice_sequence_prefix
    if hasattr(config_module, 'choice_sequence_prefix'):
        CONFIG_PARAMS['choice_sequence_prefix'] = config_module.choice_sequence_prefix

    ''' optimizations '''
    # apply optimizations
    if hasattr(config_module, 'apply_optimizations'):
        CONFIG_PARAMS['apply_optimizations'] = config_module.apply_optimizations

    ''' fragment de- and encoder '''
    # apply fragments
    if hasattr(config_module, 'generate_fragments'):
        CONFIG_PARAMS['generate_fragments'] = config_module.generate_fragments

    ''' fragment structure definitions '''
    # fragment_struct_name
    if hasattr(config_module, 'fragment_struct_name'):
        CONFIG_PARAMS['fragment_struct_name'] = config_module.fragment_struct_name
    # fragment_parameter_name
    if hasattr(config_module, 'fragment_parameter_name'):
        CONFIG_PARAMS['fragment_parameter_name'] = config_module.fragment_parameter_name
    # xmldsig_fragment_struct_name
    if hasattr(config_module, 'xmldsig_fragment_struct_name'):
        CONFIG_PARAMS['xmldsig_fragment_struct_name'] = config_module.xmldsig_fragment_struct_name
    # xmldsig_fragment_parameter_name
    if hasattr(config_module, 'xmldsig_fragment_parameter_name'):
        CONFIG_PARAMS['xmldsig_fragment_parameter_name'] = config_module.xmldsig_fragment_parameter_name

    ''' general c-code style '''
    # c_code_indent_chars (number of spaces)
    if hasattr(config_module, 'c_code_indent_chars'):
        CONFIG_PARAMS['c_code_indent_chars'] = config_module.c_code_indent_chars
    # c_replace_chars (replace with underscore)
    if hasattr(config_module, 'c_replace_chars'):
        CONFIG_PARAMS['c_replace_chars'] = config_module.c_replace_chars


ISO2_SCHEMAS_URL = "https://standards.iso.org/iso/15118/-2/ed-2/en/"
ISO20_SCHEMAS_URL = "https://standards.iso.org/iso/15118/-20/ed-1/en/"
ISO20_AMD1_SCHEMAS_URL = "https://standards.iso.org/iso/15118/-20/ed-1/en/Amd/1/"
ISO20_AMD1_SCHEMAS_ZIP = "AMD1_xsdSchema.zip"

SCHEMA_SHA256 = {
    ISO2_SCHEMAS_URL: {
        "V2G_CI_AppProtocol.xsd": "2a3ac43bf491a0a1f385e3d5130a12533248aae468492d8633a84b5b08d41a5c",
        "V2G_CI_MsgDef.xsd": "29aff88e07efb9318d2d77126899f32e10c8dfcd02cf080981a8ec67a5e422f4",
        "V2G_CI_MsgBody.xsd": "0dfec11f08ac12733c06f8cdb0a346d6140de6687db12f21ea29e054b684dde2",
        "V2G_CI_MsgDataTypes.xsd": "94d364b870df776f9ced1d6a601eebb8d4cc968d2e7e4269ad454baba6e634a0",
        "V2G_CI_MsgHeader.xsd": "0ba4ddc8bb563c3fc0e99712264958ad0db251dbf689d60d122752345566882e",
        "xmldsig-core-schema.xsd": "838fd7675e7ef4f824c84d0142c1eaddf0a72ddd9876b8191acf751c6f19f358",
    },
    ISO20_SCHEMAS_URL: {
        "V2G_CI_AC.xsd": "53b3b1a239e062a0abfc8aee0e085b024b75ddd50c964c56b385f08a8e7d327f",
        "V2G_CI_ACDP.xsd": "ad3ea1071620119f7df3ec99c66299c91609327def4e62f5654a788fae869db2",
        "V2G_CI_AppProtocol.xsd": "6e44b48ad7d4d645ea83fc8bafde4dad93914ee32da3e14033ac236b0c3a57ed",
        "V2G_CI_CommonMessages.xsd": "c3e1da88621c67167ab8e50dc4bbc82f7f8a9d4674f1230d8a9a2579f1133265",
        "V2G_CI_CommonTypes.xsd": "34d93f080f5227ad7e750ba3a194d44ddd3d2342e22a8f87925634e6cf368adc",
        "V2G_CI_DC.xsd": "42122a5b78a1f256e4ee664c67d7c888661c38550ac4a94faea6b36f11321f72",
        "V2G_CI_WPT.xsd": "8d7d70acd8e5926724c3f430237f3ad1d07a512145d4f31e029f8f029dd91132",
        "xmldsig-core-schema.xsd": "35cf8197da812c85e40d57891b35c94187569ed474a2dac813ce5090dafcd35c",
    },
    ISO20_AMD1_SCHEMAS_URL: {
        "V2G_CI_AC_DER_IEC.xsd": "3072d03da0945be459c716b0fecc32d21eb565162c6fd567ea3c1e0119aadf20",
        "V2G_CI_AC_DER_SAE.xsd": "799d4c6be9d545f7832ffbecdc4bc989630b0c809d58596d68bf12d6e198b21d",
    },
}


def _verify_sha256(file_path: Path, expected: str) -> bool:
    actual = hashlib.sha256(file_path.read_bytes()).hexdigest()
    if actual != expected:
        print(f"SHA-256 mismatch for {file_path.name}: expected {expected[:16]}..., got {actual[:16]}...")
        return False
    return True


def _check_existing_hash(file_path: Path, expected: str | None) -> bool:
    """Check hash of existing file. Returns True if file should be skipped (ok or no hash)."""
    if not expected:
        return True
    if _verify_sha256(file_path, expected):
        return True
    file_path.unlink()
    print(f"Removed {file_path.name} due to hash mismatch. Re-acquiring...")
    return False


def _check_new_hash(file_path: Path, expected: str | None) -> bool:
    """Verify hash after download/extract. Returns False on mismatch."""
    if not expected:
        print(f"Warning: no known hash for {file_path.name}, skipping verification.")
        return True
    if _verify_sha256(file_path, expected):
        return True
    file_path.unlink()
    return False


def _validate_https_url(url: str) -> str:
    if not url.startswith("https://"):
        raise ValueError(f"Only https URLs are allowed, got: {url}")
    return url


def _download_schema_files(base_url: str, schema_names: list, target_path: Path,
                           label: str) -> bool:
    """Download schema files. Returns False if any download failed."""
    hashes = SCHEMA_SHA256.get(base_url, {})
    for schema in schema_names:
        schema_file_path = target_path / schema
        expected = hashes.get(schema)
        if schema_file_path.exists():
            if _check_existing_hash(schema_file_path, expected):
                print(f"{label} schema {schema} is already there. Skipping it.")
                continue
        print(f"{label} schema {schema} not found! Downloading it...")
        try:
            urllib.request.urlretrieve(
                _validate_https_url(base_url + schema), schema_file_path.absolute().as_posix())
        except Exception as err:
            print(f"Download failed for {schema}: {err=}, {type(err)=}")
            if schema_file_path.exists():
                schema_file_path.unlink()
            return False
        if not _check_new_hash(schema_file_path, expected):
            return False
    return True


def download_schemas():
    config_module = get_config_module()

    iso2_schema_full_name = Path(
        CONFIG_ARGS['schema_base_dir'], config_module.c_files_to_generate['iso2_msgDefDatatypes']['schema'])
    iso2_schema_path = iso2_schema_full_name.parent.resolve()

    iso20_schema_full_name = Path(
        CONFIG_ARGS['schema_base_dir'], config_module.c_files_to_generate['iso20_CommonMessages_Datatypes']['schema'])
    iso20_schema_path = iso20_schema_full_name.parent.resolve()

    iso2_schema_path.mkdir(parents=True, exist_ok=True)
    iso20_schema_path.mkdir(parents=True, exist_ok=True)

    iso2_schema_files_names = ['V2G_CI_AppProtocol.xsd', 'V2G_CI_MsgDef.xsd', 'V2G_CI_MsgBody.xsd',
                               'V2G_CI_MsgDataTypes.xsd', 'V2G_CI_MsgHeader.xsd', 'xmldsig-core-schema.xsd']

    iso20_schema_files_names = ['V2G_CI_AC.xsd', 'V2G_CI_ACDP.xsd', 'V2G_CI_AppProtocol.xsd', 'V2G_CI_CommonMessages.xsd',
                                'V2G_CI_CommonTypes.xsd', 'V2G_CI_DC.xsd', 'V2G_CI_WPT.xsd', 'xmldsig-core-schema.xsd']

    _download_schema_files(ISO2_SCHEMAS_URL, iso2_schema_files_names, iso2_schema_path, "ISO15118-2")
    _download_schema_files(ISO20_SCHEMAS_URL, iso20_schema_files_names, iso20_schema_path, "ISO15118-20")

    iso20_amd1_schema_files_names = ['V2G_CI_AC_DER_IEC.xsd', 'V2G_CI_AC_DER_SAE.xsd']
    if not _download_schema_files(ISO20_AMD1_SCHEMAS_URL, iso20_amd1_schema_files_names,
                                  iso20_schema_path, "ISO15118-20 Amd1"):
        print(f"Trying zip fallback: downloading {ISO20_AMD1_SCHEMAS_ZIP}...")
        try:
            with urllib.request.urlopen(  # nosec B310  # nosemgrep
                    _validate_https_url(ISO20_AMD1_SCHEMAS_URL + ISO20_AMD1_SCHEMAS_ZIP)) as response:
                zip_data = io.BytesIO(response.read())
            amd1_hashes = SCHEMA_SHA256.get(ISO20_AMD1_SCHEMAS_URL, {})
            with zipfile.ZipFile(zip_data) as zf:
                for schema in iso20_amd1_schema_files_names:
                    schema_file_path = iso20_schema_path / schema
                    expected = amd1_hashes.get(schema)
                    if schema_file_path.exists():
                        if _check_existing_hash(schema_file_path, expected):
                            print(f"ISO15118-20 Amd1 schema {schema} is already there. Skipping it.")
                            continue
                    matching = [n for n in zf.namelist() if n.endswith(schema)]
                    if matching:
                        with zf.open(matching[0]) as src, open(schema_file_path, 'wb') as dst:
                            dst.write(src.read())
                        print(f"Extracted {schema} from {ISO20_AMD1_SCHEMAS_ZIP}.")
                        if not _check_new_hash(schema_file_path, expected):
                            print(f"Hash verification failed for {schema} from ZIP.")
                            return
                    else:
                        print(f"Error: {schema} not found in {ISO20_AMD1_SCHEMAS_ZIP}.")
        except Exception as err:
            print(f"Error during zip download: {err=}, {type(err)=}")
