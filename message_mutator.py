
from fileparse import *
from apdu import * 
from generic_mutator.generic_mutator_bytes import * # For "mutate"
import random
import copy
import ins

MAX_COPY_AMOUNT = 10 # Just a boatload of shit.
MAX_DELETE_AMOUNT = 10

def mutate_messages(messages: list): # Mutates the messages in-place.

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



