/* SPDX-License-Identifier: Apache-2.0 */

/*
 * Decodes one ISO 15118-2 EXI fragment given as hex and prints the generated
 * XML output. Needs a codec generated with generate_xml_output = 1.
 *
 * usage: emaid_fragment_xml_driver <EXI hex>
 */
#include <stdio.h>
#include <string.h>

#include "exi_bitstream.h"
#include "iso2_msgDefDatatypes.h"
#include "iso2_msgDefDecoder.h"

int main(int argc, char** argv) {
    uint8_t buffer[1024];
    char xml[4096] = {0};
    exi_bitstream_t stream;
    struct iso2_exiFragment fragment;
    size_t length;
    size_t i;
    int error;

    if (argc != 2 || strlen(argv[1]) % 2 != 0 || strlen(argv[1]) / 2 > sizeof(buffer)) {
        fprintf(stderr, "usage: %s <EXI hex>\n", argv[0]);
        return 2;
    }

    length = strlen(argv[1]) / 2;
    for (i = 0; i < length; i++) {
        unsigned int byte;
        if (sscanf(&argv[1][2 * i], "%2x", &byte) != 1) {
            fprintf(stderr, "invalid hex at offset %zu\n", 2 * i);
            return 2;
        }
        buffer[i] = (uint8_t)byte;
    }

    exi_bitstream_init(&stream, buffer, length, 0, NULL);
    error = decode_iso2_exiFragment(&stream, &fragment, xml, sizeof(xml));
    if (error != 0) {
        fprintf(stderr, "decode failed: %d\n", error);
        return 1;
    }

    printf("%s\n", xml);
    return 0;
}
