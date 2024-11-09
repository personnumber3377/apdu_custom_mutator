
# from apdu import * # For APDU parsing...
from fileparse import *
from apdu import * 
from generic_mutator.generic_mutator_bytes import * # For "mutate"
from message_mutator import *
import ins
import copy


def generate_message(): # Generates the message
	# 80 06
	# def __init__(self, CLA, CMD, OP, cmd_data):



	start_msg = APDUMsg(0x80, 0x06, None, [None]) # This message is always the very first one...
	msg_bytes = serialize_with_length(start_msg) # Serialize to bytes...


	'''
	The order of the instructions go as follows:
	OP_ADVANCE_INIT
	OP_ADVANCE_HEADER_META
	OP_ADVANCE_HEADER_CHUNK


	and INS_ADVANCE is just 0x10 , therefore we need to generate the correct messages...

	'''

	# Generate the OP_ADVANCE_INIT msg.

	# && APDU_DATA_SIZE(rx) != sizeof(uint32_t)

	# The data section of the OP_ADVANCE_INIT is just the amount of blocks which are expected.

	init_data = bytes([0x41, 0x41, 0x41, 0x41]) # Just some number.
	init_msg = APDUMsg(0x80, 0x10, ins.OP_ADVANCE_INIT, init_data) # Create the message.

	# Now send the header meta message...
	header_meta_size = ins.data_sizes_for_ops[ins.OP_ADVANCE_HEADER_META] # Just get the stuff.

	header_meta_data = bytes([0x41]) * header_meta_size # Just generate some data...

	# Now try to create the packet thing...

	header_meta_msg = APDUMsg(0x80, 0x10, ins.OP_ADVANCE_HEADER_META, header_meta_data) # Just something like this maybe???



	# OP_ADVANCE_HEADER_CHUNK




	advance_chunk_header_data_size = ins.data_sizes_for_ops[ins.OP_ADVANCE_HEADER_CHUNK] # Just get the stuff.

	advance_chunk_header_data = bytes([0x41]) * advance_chunk_header_data_size # Just generate some data... This should be 80 decimal.

	# Now try to create the packet thing...

	advance_chunk_header_msg = APDUMsg(0x80, 0x10, ins.OP_ADVANCE_HEADER_CHUNK, advance_chunk_header_data) # Just something like this maybe???


	messages = [start_msg, init_msg, header_meta_msg, advance_chunk_header_msg] # Message array.

	# Now serialize them to bytes..

	thing = bytes([])
	for msg in messages:
		new_bytes_with_length = serialize_with_length(msg) # Just something like this maybe???
		print("new_bytes_with_length == "+str(new_bytes_with_length))
		thing += new_bytes_with_length # Add it to that.

	fh = open("generated.bin", "wb")
	fh.write(thing)
	fh.close()
	return



def serialize_messages(messages):
	thing = bytes([])
	for msg in messages:
		new_bytes_with_length = serialize_with_length(msg) # Just something like this maybe???
		print("new_bytes_with_length == "+str(new_bytes_with_length))
		thing += new_bytes_with_length # Add it to that.
	return thing

def byte_seq(length):
	return bytes([i for i in range(length)])

def gen_btc_trans():

	# This is the start message
	start_msg = APDUMsg(0x80, 0x06, None, [None]) # This message is always the very first one...
	msg_bytes = serialize_with_length(start_msg) # Serialize to bytes...

	length = 21 + 4
	# could also be this: # length = 21 + 32

	# the CMD is ins.INS_SIGN   the OP is basically just 

	# The first 21 bytes of the data field must be "\x05\x2c\x00\x00\x80\x00\x00\x00\x80\x00\x00\x00\x80\x00\x00\x00\x00\x00\x00\x00\x00" or some other path which requires authentication...

	# At this point I don't know what the last 4 bytes should be, so let's just set them to b'AAAA' . :D

	handle_path_data = b"\x05\x2c\x00\x00\x80\x00\x00\x00\x80\x00\x00\x00\x80\x00\x00\x00\x00\x00\x00\x00\x00"+b"\x00\x00\x00\x00"  # +b"\x41\x41\x41\x41"
	handle_path_data = bytes(handle_path_data)
	assert len(handle_path_data) == length
	# Now generate the handle_path_msg
	# start_msg = APDUMsg(0x80, 0x06, None, [None]) # This message is always the very first one...

	messages = []
	handle_path_msg = APDUMsg(0x80, ins.INS_SIGN, 0x01, handle_path_data) # 0x01 == P1_PATH .
	# Now at this point we should trigger the authorized path thing...
	messages.append(handle_path_msg) # Append this message to the messages...

	# Now next up is the auth_sign_handle_btctx message.
	# APDU_TOTAL_DATA_SIZE is basically the length of the handle_path_data thing..
	auth_sign_handle_btctx_data = b"A"*len(handle_path_data)
	# print("len(auth_sign_handle_btctx_data) == "+str(len(auth_sign_handle_btctx_data)))
	# total_length = 82
	total_length = 85 # Just some bullshit here..
	thing = 0
	# actual_data = b"\x00"*thing + b"\x60"*(total_length-thing)

	actual_data = byte_seq(total_length)

	actual_data = list(actual_data)

	# the BTCTX_LENGTH_SIZE bytes is the length
	# Then there is one byte which signifies the thing and then there are two bytes for extra data size, which in our case is zero.


	actual_data[0] = 0xff # The length
	actual_data[1] = 0xff
	actual_data[2] = 0x00
	actual_data[3] = 0x00
	actual_data[4] = 0x00 # This is the thing.
	actual_data[5] = 0x01 # Just set the extra data size to one. This can not be zero.
	actual_data[6] = 0x00

	# THis is the tx version shit. Set the tx version to zero for now..
	actual_data[7] = 0x01
	actual_data[8] = 0x00
	actual_data[9] = 0x00
	actual_data[10] = 0x00



	# actual_data[len(actual_data) - 36] = 0xff # Maybe something like this..

	# So the program starts at the index len(actual_data) - 36    shit..
	# a914c664139327b98043febeab6434eba89bb196d1af87

	program = list(bytes.fromhex("6060606060606060606060606060606060606060606060")) # This is just some program from somewhere...

	print("length before: "+str(len(actual_data)))
	actual_data[len(actual_data) - 36:(len(actual_data) - 36 + len(program))] = program
	# program
	print("length after: "+str(len(actual_data)))

	# actual_data[-10] = 0x01 # Maybe something like this???
	#actual_data[-3] = 0x01
	#actual_data[-2] = 0x01
	# Here is the btcscript shit:

	# actual_data[11] = 0x61 # Maybe just something like this????

	#actual_data[0] = 0 # the first byte is the COMPUTE_MODE (it is either zero aka SIGHASH_COMPUTE_MODE_LEGACY or 1 which is the other thing.)
	
	actual_data.pop(-1)
	actual_data.pop(-1)
	actual_data.pop(-1)


	actual_data = bytes(actual_data)
	


	auth_sign_handle_btctx_msg = APDUMsg(0x80, ins.INS_SIGN, 0x02, actual_data) # 0x02 == P1_BTC shit...

	# append to the messages...
	messages.append(auth_sign_handle_btctx_msg)

	poopoo = copy.deepcopy(actual_data)
	actual_data = list(actual_data)
	actual_data.pop(-1)
	actual_data.pop(-1)
	actual_data = bytes(actual_data)



	st_operand_shit = bytes([0x00])*len(actual_data) # At this point we are in buf[i] in BTCSCRIPT_ST_OPERAND 

	auth_sign_handle_btctx_msg2 = APDUMsg(0x80, ins.INS_SIGN, 0x02, st_operand_shit)



	messages.append(auth_sign_handle_btctx_msg2)

	new_msg_shit = copy.deepcopy(auth_sign_handle_btctx_msg2)


	actual_data = new_msg_shit.data # Just get the data shit from there. Then do the thing....

	actual_data = list(actual_data)

	program = list(bytes.fromhex("a914c664139327b98043febeab6434eba89bb196d1af87")) # This is just some program from somewhere...

	print("length before: "+str(len(actual_data)))
	actual_data[len(actual_data) - 36:(len(actual_data) - 36 + len(program))] = program
	actual_data = bytes(actual_data)
	new_msg_shit.data = actual_data

	messages.append(new_msg_shit)
	# messages.append(auth_sign_handle_btctx_msg)

	# Now is the time for the P1_RECEIPT phase...

	'''

	82
	// Operation selectors
	typedef enum {
	    P1_PATH = 0x01,
	    P1_BTC = 0x02,
	    P1_RECEIPT = 0x04,
	    P1_MERKLEPROOF = 0x08,
	    P1_SUCCESS = 0x81,
	} op_code_sign_t;

	'''

	# STATE_AUTH_RECEIPT


	auth_receipt_msg = APDUMsg(0x80, ins.INS_SIGN, 0x04, b"AAAAAAAAAA") # 0x04 == P1_RECEIPT

	messages.append(auth_receipt_msg)

	final_data = serialize_messages(messages)
	# Now just save this to btc.bin

	fh = open("btc.bin", "wb")
	fh.write(final_data)
	fh.close()
	print("Generated the btc shit...")
	return



if __name__ == "__main__":
	print("This program is used to generate a certain message file. This is used for debugging and stuff not in actual fuzzing.")
	generate_message()
	gen_btc_trans()
	exit(0)
