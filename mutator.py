
# from apdu import * # For APDU parsing...
from fileparse import *
from apdu import * 


def test_mutator():
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


	# Now we have the chunks in chunks. Try to parse them to the APDUMsg objects.





	return


if __name__=="__main__":

	print("You should use this with AFL or libfuzzer. When running standalone, this just runs some tests. See https://aflplus.plus/docs/custom_mutators/ for details.")

	test_mutator()

	exit(0)
