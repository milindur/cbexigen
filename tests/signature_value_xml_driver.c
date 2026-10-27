/* SPDX-License-Identifier: Apache-2.0 */

/*
 * Encodes an ISO 15118-2 xmldsig SignatureValue fragment with Id="A" and content
 * bytes "A", decodes it again and prints the generated XML output.
 * Needs a codec generated with generate_xml_output = 1.
 */
#include <stdio.h>
#include <string.h>

#include "exi_bitstream.h"
#include "iso2_msgDefDatatypes.h"
#include "iso2_msgDefDecoder.h"
#include "iso2_msgDefEncoder.h"

int main(void) {
    uint8_t buffer[256] = {0};
    char xml[1024] = {0};
    exi_bitstream_t stream;
    struct iso2_xmldsigFragment fragment;
    int error;

    init_iso2_xmldsigFragment(&fragment);
    fragment.SignatureValue_isUsed = 1u;
    fragment.SignatureValue.Id_isUsed = 1u;
    fragment.SignatureValue.Id.characters[0] = 'A';
    fragment.SignatureValue.Id.charactersLen = 1;
    fragment.SignatureValue.CONTENT.bytes[0] = 'A';
    fragment.SignatureValue.CONTENT.bytesLen = 1;

    exi_bitstream_init(&stream, buffer, sizeof(buffer), 0, NULL);
    error = encode_iso2_xmldsigFragment(&stream, &fragment);
    if (error == 0) {
        exi_bitstream_init(&stream, buffer, sizeof(buffer), 0, NULL);
        error = decode_iso2_xmldsigFragment(&stream, &fragment, xml, sizeof(xml));
    }
    if (error != 0) {
        fprintf(stderr, "failed: %d\n", error);
        return 1;
    }

    printf("%s\n", xml);
    return 0;
}
