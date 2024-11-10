
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

def generate_btctx_message():
	# This function generates a btctx style message...

	# Now do the shit...

	fh = open("oofshit/sample.bin", "rb")

	total_data = fh.read()

	fh.close()

	#data1, data2 = total_data[:100], total_data[100:]
	#assert len(data1) < 256 and len(data2) < 256
	assert len(total_data) < 256

	auth_btctx_msg1 = APDUMsg(0x80, ins.INS_SIGN, 0x02, total_data) # Just do some bullshit
	#auth_btctx_msg2 = APDUMsg(0x80, ins.INS_SIGN, 0x02, data1)


	return [auth_btctx_msg1]




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


	some_bullshit_messages = generate_btctx_message()

	# messages.append(some_bullshit_message)
	messages += some_bullshit_messages
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
