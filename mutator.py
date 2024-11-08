
# from apdu import * # For APDU parsing...
from fileparse import *



def test_mutator():
	fh = open("input.bin", "rb") # Read the file "input.bin"
	data = fh.read() # Read input data.
	fh.close()
	print(try_parse_input(data)) # Try to parse the chunks from the input file.
	return


if __name__=="__main__":

	print("You should use this with AFL or libfuzzer. When running standalone, this just runs some tests. See https://aflplus.plus/docs/custom_mutators/ for details.")

	test_mutator()

	exit(0)
