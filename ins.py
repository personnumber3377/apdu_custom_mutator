
# This file contains all of the valid CMD fields. This was taken from the rsk-powhsm source code.


'''

[INS_SIGN = 0x02,
INS_GET_PUBLIC_KEY = 0x04,
RSK_IS_ONBOARD = 0x06,
RSK_MODE_CMD = 0x43,
INS_ADVANCE = 0x10,
INS_ADVANCE_PARAMS = 0x11,
INS_GET_STATE = 0x20,
INS_RESET_STATE = 0x21,
INS_UPD_ANCESTOR = 0x30,
INS_ATTESTATION = 0x50,
INS_HEARTBEAT = 0x60,
INS_EXIT = 0xff]
'''


# P1_RECEIPT


INS_SIGN = 0x02
INS_GET_PUBLIC_KEY = 0x04
RSK_IS_ONBOARD = 0x06
RSK_MODE_CMD = 0x43
INS_ADVANCE = 0x10
INS_ADVANCE_PARAMS = 0x11
INS_GET_STATE = 0x20
INS_RESET_STATE = 0x21
INS_UPD_ANCESTOR = 0x30
INS_ATTESTATION = 0x50
INS_HEARTBEAT = 0x60
INS_EXIT = 0xff

# All valid instructions in a list...

all_instructions = [INS_SIGN,
	INS_GET_PUBLIC_KEY,
	RSK_IS_ONBOARD,
	RSK_MODE_CMD,
	INS_ADVANCE,
	INS_ADVANCE_PARAMS,
	INS_GET_STATE,
	INS_RESET_STATE,
	INS_UPD_ANCESTOR,
	INS_ATTESTATION,
	INS_HEARTBEAT,
	INS_EXIT]



# These are the INS_ADVANCE OP STUFF:



'''


// Operation selectors
typedef enum {
    OP_ADVANCE_INIT = 0x02,
    OP_ADVANCE_HEADER_META = 0x03,
    OP_ADVANCE_HEADER_CHUNK = 0x04,
    OP_ADVANCE_PARTIAL = 0x05,
    OP_ADVANCE_SUCCESS = 0x06,
    OP_ADVANCE_BROTHER_LIST_META = 0x07,
    OP_ADVANCE_BROTHER_META = 0x08,
    OP_ADVANCE_BROTHER_CHUNK = 0x09,
} op_code_advance_t;










/*
 * Advance blockchain state.
 *
 * @arg[in] rx number of received bytes from the Host
 * @ret     number of transmited bytes to the host
 */
unsigned int bc_advance(volatile unsigned int rx) {
    uint8_t op = APDU_OP();

    // Check we are getting expected OP
    if (op != OP_ADVANCE_INIT && op != expected_state) {
        FAIL(PROT_INVALID);
    }

    // Check we are getting the expected amount of data
    if (op == OP_ADVANCE_INIT && APDU_DATA_SIZE(rx) != sizeof(uint32_t)) {
        FAIL(PROT_INVALID);
    }
    if ((op == OP_ADVANCE_HEADER_META || op == OP_ADVANCE_BROTHER_META) &&
        APDU_DATA_SIZE(rx) !=
            (sizeof(block.mm_rlp_len) + sizeof(block.cb_txn_hash))) {
        FAIL(PROT_INVALID);
    }
    if (op == OP_ADVANCE_BROTHER_LIST_META &&
        APDU_DATA_SIZE(rx) != sizeof(block.brother_count)) {
        FAIL(PROT_INVALID);
    }
    if (op == OP_ADVANCE_HEADER_CHUNK || op == OP_ADVANCE_BROTHER_CHUNK) {
        uint16_t expected_txlen =
            block.size > 0 ? MIN(block.size - block.recv, MAX_CHUNK_SIZE)
                           : MAX_CHUNK_SIZE;
        if (APDU_DATA_SIZE(rx) != expected_txlen) {
            FAIL(PROT_INVALID);
        }
    }
    uint16_t mm_rlp_len; // Cached mm RLP length

    uint8_t parent_hash[HASH_SIZE];     // Parent hash
    uint8_t cb_txn_hash[HASH_SIZE]; // Coinbase transaction hash (from metadata)






        uint16_t expected_txlen =
            block.size > 0 ? MIN(block.size - block.recv, MAX_CHUNK_SIZE)
                           : MAX_CHUNK_SIZE;

'''



OP_ADVANCE_INIT = 0x02
OP_ADVANCE_HEADER_META = 0x03
OP_ADVANCE_HEADER_CHUNK = 0x04
OP_ADVANCE_PARTIAL = 0x05
OP_ADVANCE_SUCCESS = 0x06
OP_ADVANCE_BROTHER_LIST_META = 0x07
OP_ADVANCE_BROTHER_META = 0x08
OP_ADVANCE_BROTHER_CHUNK = 0x09

'''
advance_ops = [
	OP_ADVANCE_INIT,
	OP_ADVANCE_HEADER_META,
	OP_ADVANCE_HEADER_CHUNK,
	OP_ADVANCE_PARTIAL,
	OP_ADVANCE_SUCCESS,
	OP_ADVANCE_BROTHER_LIST_META,
	OP_ADVANCE_BROTHER_META,
	OP_ADVANCE_BROTHER_CHUNK
]
'''



#  && APDU_DATA_SIZE(rx) != sizeof(uint32_t)
# mm_rlp_len = 2
# t8_t cb_txn_hash[HASH_SIZE]; = HASH_SIZE
# #define HASH_SIZE 32
HASH_SIZE = 32
MAX_CHUNK_SIZE = 80

data_sizes_for_ops = {OP_ADVANCE_INIT: 4, OP_ADVANCE_HEADER_META: 2 + HASH_SIZE, OP_ADVANCE_BROTHER_META: 2 + HASH_SIZE, OP_ADVANCE_BROTHER_LIST_META: 1, OP_ADVANCE_HEADER_CHUNK: MAX_CHUNK_SIZE, OP_ADVANCE_BROTHER_CHUNK: 80} # These are the only data sizes which are accepted by these things...

advance_ops = list(data_sizes_for_ops.keys())


