

'''

// CLA for the entire protocol
#define CLA 0x80

'''


def must_be_byte(value: int) -> None: # Checks that an integer can fit in one byte. Basically only used for sanity checking.
	assert value >= 0 and value <= 255
	return

class APDUMsg:
	# https://en.wikipedia.org/wiki/Smart_card_application_protocol_data_unit
	def __init__(self, CLA, INS, P1_P2, L_c, cmd_data, L_e):
		# Instruction parameters for the command, e.g., offset into file at which to write the data
		# First some sanity checks.
		must_be_byte(CLA)
		must_be_byte(INS)
		assert CLA == 0x80 # CLA must always be 0x80

		self.CLA = CLA
		self.INS = INS


def parse_apdu_message(message: bytes):
	# Parses a singular APDU message.
	






