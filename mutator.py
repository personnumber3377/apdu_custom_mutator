
# from apdu import * # For APDU parsing...
from fileparse import *
from apdu import * 
from generic_mutator.generic_mutator_bytes import * # For "mutate"
from message_mutator import *

def mutate_contents(databytes: bytes) -> bytes: # Mutates bytes
	chunks = try_parse_input(databytes)
	if chunks == None: # The original data passed to this function was invalid. Return a generic mutation
		return mutate_generic(databytes) # Just use the generic mutator...
	# Now we should get the same file input back if we deserialize with length.
	thing = bytes([])
	messages = []
	for chunk in chunks:
		msg = deserialize_to_obj(chunk)
		messages.append(msg) # Add that message thing.
	# Ok, so now we have the messages in "messages". Select a mutation strategy and mutate.
	mutate_messages(messages) # Mutate the message objects...
	# Serialize back to bytes
	thing = bytes([])
	for msg in messages:
		new_bytes_with_length = serialize_with_length(msg) # Just something like this maybe???
		thing += new_bytes_with_length # Add it to that.
	return thing # Return the final thing

def test_serializing():
	fh = open("input.bin", "rb") # Read the file "input.bin"
	data = fh.read() # Read input data.
	fh.close()
	chunks = try_parse_input(data)
	#print(res)
	for chunk in chunks: # Try to parse the chunks from the input file.
		# print(chunk)
		# First deserialize to the message object:
		msg = deserialize_to_obj(chunk) # Deserialize chunk...
		# Now after that try to serialize back.
		new_bytes = serialize_to_bytes(msg)
		print("chunk: "+str(chunk)+" "*10+"new_bytes: "+str(new_bytes))
		assert chunk == new_bytes # Should be the same

	# Now we should get the same file input back if we deserialize with length.

	thing = bytes([])
	for chunk in chunks:

		msg = deserialize_to_obj(chunk)

		new_bytes_with_length = serialize_with_length(msg) # Just something like this maybe???

		thing += new_bytes_with_length # Add it to that.

	assert thing == data # Final check...

	print("Tests passed!!!")

	return


def test_mutating():
	fh = open("input.bin", "rb") # Read the file "input.bin"
	data = fh.read() # Read input data.
	fh.close()

	for _ in range(1000):
		fh = open("output.bin", "wb") # Read the file "input.bin"
		fh.write(data) # Read input data.
		fh.close()
		data = mutate_contents(data)
		#print("Mutated!")
	print("Mutated data: "+str(data))

	print("test_mutating passed!!!")
	return


if __name__=="__main__":

	print("You should use this with AFL or libfuzzer. When running standalone, this just runs some tests. See https://aflplus.plus/docs/custom_mutators/ for details.")

	# test_serializing()
	test_mutating()
	exit(0)
