##############################################################################
# server.py
##############################################################################

import socket
import chatlib
import random
import select

# GLOBALS
users = {}
questions = {}
logged_users = {} # a dictionary of client hostnames to usernames - will be used later
messages_to_send = []

ERROR_MSG = "Error! "
SERVER_PORT = 5678
SERVER_IP = "127.0.0.1"


# HELPER SOCKET METHODS

def build_and_send_message(conn, code, msg):
	## copy from client
	build_msg = chatlib.build_message(code,msg)

	if(build_msg != "None"):
		messages_to_send.append((conn,build_msg))
		conn.send(build_msg.encode())
	else:
		conn.send("None".encode())
	print("[SERVER] ",build_msg)	  # Debug print

def recv_message_and_parse(conn):
	## copy from client
	recv1 = conn.recv(1024).decode()
	cmd, data = chatlib.parse_message(recv1)
	print("[CLIENT] ",data)
	if((cmd != "None")):
		return cmd, data
	else:
		return None,None
		  
# Data Loaders #

def load_questions():
	"""
	Loads questions bank from file	## FILE SUPPORT TO BE ADDED LATER
	Recieves: -
	Returns: questions dictionary
	"""
	questions = {
				2313 : {"question":"How much is 2+2","answers":["3","4","2","1"],"correct":2},
				4122 : {"question":"What is the capital of France?","answers":["Lion","Marseille","Paris","Montpellier"],"correct":3} 
				}
	
	return questions

def load_user_database():
	"""
	Loads users list from file	## FILE SUPPORT TO BE ADDED LATER
	Recieves: -
	Returns: user dictionary
	"""
	users = {
			"test"		:	{"password":"test","score":0,"questions_asked":[]},
			"yossi"		:	{"password":"123","score":50,"questions_asked":[]},
			"master"	:	{"password":"master","score":200,"questions_asked":[]}
			}
	return users

# SOCKET CREATOR

def setup_socket():
	"""
	Creates new listening socket and returns it
	Recieves: -
	Returns: the socket object
	"""
	# Implement code ...
	print("Setting up server...")
	server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	server_socket.bind((SERVER_IP,SERVER_PORT))
	server_socket.listen()
	print("Server is listen")
	return server_socket
	
def send_error(conn, error_msg):
	"""
	Send error message with given message
	Recieves: socket, message error string from called function
	Returns: None
	"""
	# Implement code ...
	build_and_send_message(conn,ERROR_MSG,error_msg)
	
##### MESSAGE HANDLING

def handle_getscore_message(conn, username):
	global users
	# Implement this in later 
	
	score = users.get(username).get("score")
	build_and_send_message(conn,"YOUR_SCORE",str(score))

def handle_logout_message(conn):
	"""
	Closes the given socket (in laster chapters, also remove user from logged_users dictioary)
	Recieves: socket
	Returns: None
	"""
	global logged_users
	
	# Implement code ...
	conn.close()
	logged_users.pop(conn)
	print("LOGOUT ")

def handle_logged_message(conn):

	list_logged = list(logged_users.keys())

	logged_string = ""
	j = 0
	for x in list_logged:
		logged_string = logged_string + "\n" + str(logged_users.get(list_logged[j]))  + "\n"
		j = j + 1
	
	build_and_send_message(conn,"LOGGED_ANSWER",logged_string)	

def handle_login_message(conn, data,client_address):
	"""
	Gets socket and message data of login message. Checks  user and pass exists and match.
	If not - sends error and finished. If all ok, sends OK message and adds user and address to logged_users
	Recieves: socket, message code and data
	Returns: None (sends answer to client)
	"""
	global users  # This is needed to access the same users dictionary from all functions
	global logged_users	 # To be used later
	
	# Implement code ...
	list_user = chatlib.split_data(data,1)
	if(not bool(users) ):
		users = load_user_database()

	user_name = list_user[0]
	passowred = list_user[1]
	if user_name in users:
		if passowred in users.get(user_name).get("password"):
			build_and_send_message(conn,"LOGIN_OK","")
			print()
			logged_users.update({user_name : {client_address:user_name}})
		else:
			build_and_send_message(conn,"ERROR","passwored not good")
	else:
		build_and_send_message(conn,"ERROR","user name not good")

def handle_highscore_message(conn):

	list_shimi = list(users.keys())

	y = 0
	for j in list_shimi:
		y = y + 1

	check = 0
	shimi = ""

	while True:
		j = 0
		for x in list_shimi:
			if(y - 1 == j):
				break
			if(users.get(list_shimi[j]).get("score") > users.get(list_shimi[j+1]).get("score")):
				check = j
			else:
				check = j + 1
			j = j + 1

		shimi = shimi + '\n' + str(list_shimi[check]) + str(users.get(list_shimi[check]).get("score"))
		del list_shimi[check]
		y = y - 1	
		if(y == 1):
			shimi = shimi + '\n' + str(list_shimi[0]) + str(users.get(list_shimi[0]).get("score"))
			break

	build_and_send_message(conn,"ALL_SCORE",shimi)
	
def create_random_question():

	string_question = ""
	list_question = []

	dictionary_of_questions = load_questions()
	list_range_of_random = list(dictionary_of_questions.keys())

	j = 0
	for y in list_range_of_random:
		j = j + 1

	random_question = random.randint(0,j-1)
	
	name_of_question = list_range_of_random[random_question]

	list_question.append(name_of_question)
	list_question.append(dictionary_of_questions.get(name_of_question).get("question"))
	list_of_answer = dictionary_of_questions.get(name_of_question).get("answers")
	for x in list_of_answer:
		list_question.append(x)
	list_question.append(dictionary_of_questions.get(name_of_question).get("correct"))

	string_question = chatlib.join_data(list_question)

	return string_question

def handle_question_message(conn):

	question = create_random_question()
	build_and_send_message(conn,"YOUR_QUESTION",question)
	cmd, data = recv_message_and_parse(conn)
	handle_answer_message(conn,cmd,data)

def handle_answer_message(conn,cmd,data):

	list_data = chatlib.split_data(data,2)
	dictionary_of_questions = load_questions()
	list_answer_keys = list(dictionary_of_questions.keys())
	correct_answer = 0
	username = list_data[2]

	for x in list_answer_keys:

		if int(x) == int(list_data[0]):
			correct_answer = x
	
	get_answer = dictionary_of_questions.get(correct_answer).get("correct")

	if(int(get_answer) == int(list_data[1])):
		build_and_send_message(conn,"CORRECT_ANSWER","")
		score = users.get(username).get("score")
		score = score + 5
		users[username]['score'] = score
	else:
		get_answer = str(get_answer)
		build_and_send_message(conn,"WRONG_ANSWER",get_answer)

def handle_client_message(conn, cmd, data,client_address):
	"""
	Gets message code and data and calls the right function to handle command
	Recieves: socket, message code and data
	Returns: None
	"""
	global logged_users	 # To be used later

	if(cmd == "LOGIN"):
		handle_login_message(conn,data,client_address)
	elif(cmd == "MY_SCORE"):
		handle_getscore_message(conn,data)
	elif(cmd == "GET_QUESTION"):
		handle_question_message(conn)
	elif(cmd == "SEND_ANSWER"):
		handle_answer_message(conn,cmd,data)
	elif(cmd == "HIGHSCORE"):
		handle_highscore_message(conn)
	elif(cmd == "LOGGED"):
		handle_logged_message(conn)
	elif((cmd == "LOGOUT") or (cmd == " ") or (cmd == "None")):
		handle_logout_message(conn)
	else:
		build_and_send_message(conn,"ERROR",ERROR_MSG)

def print_client_sockets(list_of_sockets):
	list_shimi = logged_users.keys()
	for x in range(len(list_shimi)):
		print(list_shimi[x])

def main():
	# Initializes global users and questions dicionaries using load functions, will be used later
	global users
	global questions

	client_sockets = []
	
	print("Welcome to Trivia Server!")
	
	# Implement code ...
	conn = setup_socket()
	
	while True:
		ready_to_read, ready_to_write , in_error = select.select([conn]+ client_sockets , [],[])
		for current_socket in ready_to_read:
			if current_socket is conn:
				(client_socket, client_address) = current_socket.accept()
				print("New client joined: ", client_address)
				client_sockets.append(client_socket)
				print("New client" , client_address )
			else:
				cmd, data = recv_message_and_parse(client_socket)
				handle_client_message(client_socket,cmd,data,client_address)
		
if __name__ == '__main__':
	main()