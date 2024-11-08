

def try_parse_chunks(file_data: bytes) -> list:
	# This is a file reader type parser.
	cur_byte_idx = 0

	out = [] # Output chunks.

	while True: # Parse loop.
		# Check if we are at the end.
		if cur_byte_idx >= len(file_data):
			break
		# First get length.
		length = file_data[cur_byte_idx]
		cur_byte_idx += 1 # Advance counter
		if cur_byte_idx + length >= len(file_data): # Invalid input. Return None
			return None
		# Now read the chunk data
		chunk_data = file_data[cur_byte_idx:cur_byte_idx+length]
		cur_byte_idx += length # Advance reader.
		out.append(chunk_data)
	return out

def try_parse_input(input_stuff: bytes): # This tries to parse the input bytes...

	apdu_chunks = try_parse_chunks(input_stuff) # This carves out the apdu chunk stuff.
	if not apdu_chunks:
		return input_stuff # Just return the original input (for now).
	#print(apdu_chunks)
	return apdu_chunks




















