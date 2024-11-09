
# from apdu import * # For APDU parsing...
from fileparse import *
from apdu import * 
from generic_mutator.generic_mutator_bytes import * # For "mutate"
from message_mutator import *
import ins


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


if __name__ == "__main__":
	print("This program is used to generate a certain message file. This is used for debugging and stuff not in actual fuzzing.")
	generate_message()
	exit(0)
