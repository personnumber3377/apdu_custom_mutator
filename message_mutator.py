
from fileparse import *
from apdu import * 
from generic_mutator.generic_mutator_bytes import * # For "mutate"
import random
import copy



def mutate_messages(messages: list): # Mutates the messages in-place.

	mut_strat = random.randrange(3)

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
		messages.insert(random.randrange(len(messages)), new_msg) # Add a copy of the messages to the list thing..
	else:
		print("FUCKCKKCC"*10000)
		assert False # Just crash.	


	return



