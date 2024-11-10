
from fileparse import *
from apdu import * 
from generic_mutator.generic_mutator_bytes import * # For "mutate"
import random
import copy
import ins

MAX_COPY_AMOUNT = 10 # Just a boatload of shit.
MAX_DELETE_AMOUNT = 10





'''

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


'''


def mutate_data_fixed_size(msg, size) -> None: # This mutates the data field of the message "msg" to a fixed size. This is useful for messages which take a fixed length input and rejects all other input lengths.

	dat_thing = copy.deepcopy(msg.data)
	prev_data = copy.deepcopy(dat_thing)
	dat_thing = dat_thing * 1 # Just multiply by a hundred.
	for _ in range(100):
		dat_thing = bytes(mutate_generic(bytes(dat_thing[:size])))
	if len(dat_thing) <= size:
		dat_thing = dat_thing * 100

	if len(dat_thing) <= size: # Basically a safeguard
		dat = bytes([0x41]*size) # Just return a shit
		msg.data = dat
		return

	assert len(dat_thing) >= size # Should be larger or the same size.



	msg.data = dat_thing[:size] # Cutoff at size...
	if prev_data == msg.data:
		
		dat = bytes([0x41]*size) # Just return a shit
		msg.data = dat
		return 
		#print("FUCK!"*1000)
		#exit(1)
	return

def mutate_bc_advance(messages): # Mutates the bc_advance shit
	# INS_ADVANCE
	# data_sizes = {}
	mutated = False
	for i in range(len(messages)):
		if messages[i].CMD == ins.INS_ADVANCE: # Custom mutator.
			# now the data sizes are in data_sizes_for_ops
			OP_THING = messages[i].OP
			if OP_THING in ins.data_sizes_for_ops:
				data_size = ins.data_sizes_for_ops[OP_THING]
			else:
				messages[i].OP = random.choice(ins.advance_ops) # Select a random operation thing.
				assert messages[i].OP in ins.data_sizes_for_ops # Sanity checking
				data_size = ins.data_sizes_for_ops[messages[i].OP]

			data_before = copy.deepcopy(messages[i].data)
			#print("Mutating the bc shit!!!"*10000)
			#assert False
			if isinstance(data_size, int):
				mutate_data_fixed_size(messages[i], data_size)
			else:
				messages[i].data = mutate_generic(messages[i].data) # Just do something like this..
			new_data = messages[i].data
			#print("previous_data: "+str(data_before)+" "*10+"new_data: "+str(new_data))
			mutated = True
			#assert data_before != new_data # Should change.


	return mutated # Done




def mutate_messages(messages: list, add_buf_chunks: list): # Mutates the messages in-place.



	if random.randrange(3) == 1: # Try to do some bullshit thing.

		other_messages = []
		if add_buf_chunks != None:

			for chunk in add_buf_chunks:
				msg = deserialize_to_obj(chunk)
				if msg == None:
					continue # Skip adding invalid bullshit.
				other_messages.append(msg) # Add that message thing.

			if len(other_messages) != 0: # Atleast one valid message in the other file
				# Now we have the messages of the other file in other_messages . Select a random one and then add it to this data maybe???
				rand_other_message = random.choice(other_messages)
				# Now put it into the list.
				if len(messages) == 0:
					messages.append(rand_other_message)
				else:
					messages.insert(random.randrange(len(messages)), rand_other_message)
				# Now just return
				return


	# These next lines are for message specific mutations only.

	# Check for obvious overrides here before continuing with generic fuzzing strategies.
	if random.randrange(2) == 1: # 50/50 chance
		if mutate_bc_advance(messages): # Message specific mutations. If we mutate here, don't bother mutating the other shit.
			return


	# These rest are generic mutations strategies which can be used on any message.

	if len(messages) == 0: # No messages to mutate. Just do some shit.
		return [APDUMsg(0x80, 0x10, 0x10, bytes(b"aaaaaaaaaaaaaaaa"))] # This is just a safeguard.
		# msg_obj = APDUMsg(CLA, CMD, OP, cmd_data)


	mut_strat = random.randrange(6) # Generate a random integer from 0 to 5 inclusive.

	if mut_strat == 0: # Mutate the data thing.
		# Select message index which to mutate.
		rand_index = random.randrange(len(messages)) # First generate a random index...
		if messages[rand_index].data == [None]:
			return # There is no data, so just do this.
		messages[rand_index].data = bytes(mutate_generic(bytes(messages[rand_index].data)))[:255-3] # Use our generic mutator... we need to cap at 255 bytes, because the length field is one byte only...
		return
	elif mut_strat == 1: # Shuffle the messages. Switch the place of two messages.
		rand_index1 = random.randrange(len(messages)) # First generate a random index...
		rand_index2 = random.randrange(len(messages)) # First generate a random index...
		# Swap those two elements
		messages[rand_index1], messages[rand_index2] = messages[rand_index2], messages[rand_index1]
		#print("Swapped!!!!!!!")
		return
	elif mut_strat == 2:
		# Copy message
		rand_index = random.randrange(len(messages))
		message_to_be_copied = messages[rand_index]
		new_msg = copy.deepcopy(message_to_be_copied)
		# Now insert it into the list at a random location...
		for _ in range(random.randrange(MAX_COPY_AMOUNT)): # Multiply a random amount of times.
			messages.insert(random.randrange(len(messages)), new_msg) # Add a copy of the messages to the list thing..
	elif mut_strat == 3: # Delete a random message.
		del_amount = min(random.randrange(MAX_DELETE_AMOUNT), len(messages))
		for _ in range(del_amount):
			if len(messages) == 0:
				messages.pop(0)
			messages.pop(random.randrange(len(messages))) # Do this
	elif mut_strat == 4: # Change operation of a certain message.
		rand_index = random.randrange(len(messages))
		messages[rand_index].CMD = random.choice(ins.all_instructions) # Select a random command byte.
	elif mut_strat == 5: # Change OP.
		rand_index = random.randrange(len(messages))
		messages[rand_index].OP = random.randrange(256) # random.choice(ins.all_instructions) # Select a random command byte.
	else:
		print("FUCKCKKCC"*10000)
		assert False # Just crash.	

	# Set the CLA fields to 0x80 for all messages. It is completely useless to set this field to anything else other than 0x80 .
	for i in range(len(messages)):
		messages[i].CLA = 0x80 # Set the CLA field.

	return



