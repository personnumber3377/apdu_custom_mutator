

from generic_mutator_bytes import *

if __name__=="__main__":
	input_data = b""
	COUNT = 100000
	for _ in range(COUNT):
		input_data = mutate_generic(input_data)
		print(input_data)
	exit(0)
