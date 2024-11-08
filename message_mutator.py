
from fileparse import *
from apdu import * 
from generic_mutator.generic_mutator_bytes import * # For "mutate"
import random




def mutate_messages(messages: list): # Mutates the messages in-place.

	mut_strat = random.randrange(3)

	#if mut_strat == 0: # Mutate the data thing.
	# Select message index which to mutate.
	rand_index = random.randrange(len(messages)) # First generate a random index...
	if messages[rand_index].data == [None]:
		return # There is no data, so just do this.
	messages[rand_index].data = bytes(mutate_generic(bytes(messages[rand_index].data)))[:255-3] # Use our generic mutator... we need to cap at 255 bytes, because the length field is one byte only...



	return



