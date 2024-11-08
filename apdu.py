

'''

// CLA for the entire protocol
#define CLA 0x80

'''


class APDUMsg:
	# https://en.wikipedia.org/wiki/Smart_card_application_protocol_data_unit
	def __init__(self, CLA, CMD, OP, cmd_data):
		# Instruction parameters for the command, e.g., offset into file at which to write the data
		# First some sanity checks.
		must_be_byte(CLA)
		must_be_byte(CMD)
		must_be_byte(OP)
		assert CLA == 0x80 # CLA must always be 0x80

		self.CLA = CLA
		self.CMD = CMD
		self.OP = OP
		self.data = cmd_data # This is the stuff after the 3 byte header.



def bytes_or_nothing(thing): # Checks for None
	if thing == None or thing[0] == None:
		return bytes([])
	else:
		return bytes(thing)


def deserialize_to_obj(message_bytes: bytes) -> APDUMsg: # This deserializes a single message to a APDUMsg object.
	# def __init__(self, CLA, CMD, OP, cmd_data):

	header = message_bytes[:3] # Three first bytes.
	cmd_data = message_bytes[3:] # Then the rest is just data for the command.
	#print("header == "+str(header))
	#print("message_bytes == "+str(message_bytes))
	if len(header) == 3:
		CLA, CMD, OP = header # Take the first three things.
	else:
		CLA, CMD = header
		OP = None
		cmd_data = [None]
	assert isinstance(CLA, int)
	assert isinstance(CMD, int)
	assert isinstance(OP, int) or OP == None
	must_be_byte(CLA)
	must_be_byte(CMD)
	must_be_byte(OP)
	# Now create the object...
	msg_obj = APDUMsg(CLA, CMD, OP, cmd_data) # Create the object.
	return msg_obj

def serialize_to_bytes(msg: APDUMsg) -> bytes:
	return bytes_or_nothing([msg.CLA]) + bytes_or_nothing([msg.CMD]) + bytes_or_nothing([msg.OP]) + bytes_or_nothing(msg.data) # Maybe something like this???

def serialize_with_length(msg: APDUMsg) -> bytes:
	msg_bytes = serialize_to_bytes(msg)
	if len(msg_bytes) > 255:
		print("FUUUUUCCCKKKK")
		exit(1)
	return bytes([len(msg_bytes)]) + msg_bytes # Just something like this maybe???


def must_be_byte(value: int) -> None: # Checks that an integer can fit in one byte. Basically only used for sanity checking.
	if value == None:
		return # Just a quick little shorthand :D
	assert value >= 0 and value <= 255
	return








