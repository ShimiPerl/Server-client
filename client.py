import socket
import chatlib  # To use chatlib functions or consts, use chatlib.****

SERVER_IP = "127.0.0.1"  # Our server will run on same computer as client
SERVER_PORT = 5678

# HELPER SOCKET METHODS

def build_and_send_message(conn, code, data):
	"""
	Builds a new message using chatlib, wanted code and message. 
	Prints debug info, then sends it to the given socket.
	Paramaters: conn (socket object), code (str), data (str)
	Returns: Nothing
	"""
	# Implement Code
	build_msg = chatlib.build_message(code,data)

	if(build_msg != "None"):
		conn.send(build_msg.encode())
	else:
		conn.send("None".encode())
	
def recv_message_and_parse(conn):
	"""
	Recieves a new message from given socket,
	then parses the message using chatlib.
	Paramaters: conn (socket object)
	Returns: cmd (str) and data (str) of the received message. 
	If error occured, will return None, None
	"""
	# Implement Code
	# to handle a error
	recv1 = conn.recv(1024).decode()
	cmd, data = chatlib.parse_message(recv1)
	if((cmd != "None")):
		return cmd, data
	else:
		return None,None

def connect():
    # Implement Code
	my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	my_socket.connect((SERVER_IP,SERVER_PORT))
	return my_socket

def error_and_exit(error_msg):
    # Implement code
    print(error_msg) 
    exit()
	
def login(conn):
	global username
	username = input("Please enter username: \n")
	password = input("Please enter password: \n")
		
    # Implement code
	while True:
		full_data = username + '#' + password

		build_and_send_message(conn, chatlib.PROTOCOL_CLIENT["login_msg"],full_data)

		cmd,data = recv_message_and_parse(conn)

		if(cmd == "LOGIN_OK"):
			print("\n Log in went good !!! \n")
			break	
		else:
			print("it didnt work \n")
			username = input("Please enter username: \n")
			password = input("Please enter password: \n")
	return

def logout(conn):

    # Implement code
	build_and_send_message(conn,"LOGOUT","")

def buil_send_recv_parse(conn,cmd,data):
	build_and_send_message(conn,cmd,data)
	msg_send , data_infun = recv_message_and_parse(conn)
	return msg_send, data_infun

def get_score(conn):
	cmd = "MY_SCORE"
	data1 = username
	cmd2 , data = buil_send_recv_parse(conn,cmd,data1)
	if(cmd2 != "None"):
		print(cmd2 + " " + data + "\n")
	else:
		print("Error \n")

def get_highscore(conn):
	cmd , data = buil_send_recv_parse(conn,"HIGHSCORE","")
	print(cmd + "\n" + data + "\n")

def play_question(conn):
	cmd , data = buil_send_recv_parse(conn,"GET_QUESTION","")
	list_shimi = chatlib.split_data(data,6)
	for x in range(6):
		print(list_shimi[x])

	answer = input("what is the answer? \n")
	answer = list_shimi[0] + "#" + answer + "#" + username
	cmd , data = buil_send_recv_parse(conn,"SEND_ANSWER",answer)
	if(cmd != "NO_QUESTIONS"):
		if(cmd != "WRONG_ANSWER"):
			print(cmd + "\n")
		else:
			print(data)
	else:
         print("no more question")

def get_logged_users(conn):
	cmd , data = buil_send_recv_parse(conn,"LOGGED","")
	print(data)

def main():
	socket_client = connect()
	login(socket_client)
	while True:
		what_client = input("What do you what do to? \n" + "A = My score \n" + "B = Highscore \n" + "C = Get qustion \n" + "D = Logged \n" + "E = Log out \n" + "Answer: ")
		if(what_client == "A"):
			get_score(socket_client)
		elif(what_client == "B"):
			get_highscore(socket_client)
		elif(what_client == "C"):
			play_question(socket_client)
		elif(what_client == "D"):
			get_logged_users(socket_client)
		elif((what_client == "E")):
			logout(socket_client)
			break
		else:
			print()

	socket_client.close()

if __name__ == '__main__':
    main()