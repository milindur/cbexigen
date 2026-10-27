/* SPDX-License-Identifier: Apache-2.0 */

/*
 * Prints an EXI signed integer through the generated XML helper.
 * Includes the generated decoder source to reach its static helpers.
 *
 * usage: xml_signed_driver <0|1 negative> <magnitude hex, may be empty>
 */
#include "iso2_msgDefDecoder.c"

int main(int argc, char** argv) {
    exi_signed_t value;
    char xml[256] = {0};
    size_t pos = 0;
    size_t i;

    if (argc != 3 || strlen(argv[2]) % 2 != 0 || strlen(argv[2]) / 2 > sizeof(value.data.octets)) {
        fprintf(stderr, "usage: %s <0|1 negative> <magnitude hex>\n", argv[0]);
        return 2;
    }

    memset(&value, 0, sizeof(value));
    value.is_negative = argv[1][0] == '1';
    value.data.octets_count = strlen(argv[2]) / 2;
    for (i = 0; i < value.data.octets_count; i++) {
        unsigned int byte;
        sscanf(&argv[2][2 * i], "%2x", &byte);
        value.data.octets[i] = (uint8_t)byte;
    }

    xml_write_signed(xml, sizeof(xml), &pos, &value);
    printf("%s\n", xml);
    return 0;
}
