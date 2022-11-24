# Protocol Constants

CMD_FIELD_LENGTH = 16	# Exact length of cmd field (in bytes)
LENGTH_FIELD_LENGTH = 4   # Exact length of length field (in bytes)
MAX_DATA_LENGTH = 10**LENGTH_FIELD_LENGTH-1  # Max size of data field according to protocol
MSG_HEADER_LENGTH = CMD_FIELD_LENGTH + 1 + LENGTH_FIELD_LENGTH + 1  # Exact size of header (CMD+LENGTH fields)
MAX_MSG_LENGTH = MSG_HEADER_LENGTH + MAX_DATA_LENGTH  # Max size of total message
DELIMITER = "|"  # Delimiter character in protocol
DATA_DELIMITER = "#"  # Delimiter in the data part of the message

# Protocol Messages 
# In this dictionary we will have all the client and server command names

PROTOCOL_CLIENT = {
"login_msg" : "LOGIN",
"logout_msg" : "LOGOUT"
} # .. Add more commands if needed


PROTOCOL_SERVER = {
"login_ok_msg" : "LOGIN_OK",
"login_failed_msg" : "ERROR"
} # ..  Add more commands if needed

# Other constants

ERROR_RETURN = None  # What is returned in case of an error

def build_message(cmd, data):
	"""
	Gets command name (str) and data field (str) and creates a valid protocol message
	Returns: str, or None if error occured
	"""
    # Implement code ...
	if((len(cmd) < 17) and (len(data) < MAX_DATA_LENGTH)):
		fullmsg = ""
		cmdMinos = 16 - len(cmd)
		fields = 0

		for x in data:
			fields += 1
		
		for x in range(cmdMinos):
			cmd += " "

		if(fields < 10):
			fullmsg = cmd + '|' + "000" + str(fields) + '|' + data

		if(9 < fields < 100):
			fullmsg = cmd + '|' + "00" + str(fields) + '|' + data	
		
		if(99 < fields < 1000):
			fullmsg = cmd + '|' + "0" + str(fields) + '|' + data	
			
		if(999 < fields < 10000):
			fullmsg = cmd + '|' + str(fields) + '|' + data

		return fullmsg
	else:
		return ERROR_RETURN

def parse_message(data):
	"""
	Parses protocol message and returns command name and data field
	Returns: cmd (str), data (str). If some error occured, returns None, None
	"""
    # Implement code ...
	str1 = data[17:21]

	if((data != "") and (data[16] == '|') and (data[21] == '|') and (int(str1) > -1) and (data[17].isalpha() == False) and (data[18].isalpha() == False) and (data[19].isalpha() == False) and (data[20].isalpha() == False)):
		cmd = ""
		for element in data[0:16]:
			if(element != ' '):
				cmd += element
				
		msg = ""
		for element in data[22::]:
			if(element != '"'):
				msg += element

		return cmd, msg
	else:
		return ERROR_RETURN	, ERROR_RETURN

    # The function should return 2 values

def split_data(msg, expected_fields):
	"""
	Helper method. gets a string and number of expected fields in it. Splits the string 
	using protocol's data field delimiter (|#) and validates that there are correct number of fields.
	Returns: list of fields if all ok. If some error occured, returns None
	"""
	# Implement code ...
	fields = 0
	for element in msg:
		if(element == '#'):
			fields = fields+1

	if(fields!= expected_fields):
		return ERROR_RETURN

	fields = 0
	fields1 = 0
	list = []
	for element in msg:
		if(element != '#'):
			fields = fields+1
		else:
			list.append(msg[fields1:fields])
			fields1 = fields + 1
			fields += 1 

	list.append(msg[fields1::])		

	return list

def join_data(msg_fields):
	"""
	Helper method. Gets a list, joins all of it's fields to one string divided by the data delimiter. 
	Returns: string that looks like cell1#cell2#cell3
	"""
	# Implement code ...
	str1 = ""
	j = 0
	
	for x in msg_fields:
			str1 = str1 + str(x)
			str1 = str1 + "#"
			j = j + 1
	str1 = str1[:-1]

	return str1