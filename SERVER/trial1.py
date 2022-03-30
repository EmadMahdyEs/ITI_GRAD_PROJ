import socket
import threading


# open the hex file
file = open("USART_ARM_PROJECT.hex","r")
# get the record and remove the preceding colon
records = [line[1:] for line in file]


HEADER = 64
PORT = 5050
#SERVER = "192.168.79.1"
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER,PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"


Server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
Server.bind(ADDR)

counter=0

#this function is called only when a data is received from the client.
def handle_client(conn,addr):
	global counter
	print(f"New Connection {addr} connected ")

	connected = True
	while connected:
		msg__ = conn.recv(2048).decode(FORMAT)
		print(msg__)
		if(msg__=="version=3.2"):
			conn.send("update version=3.3\n".encode(FORMAT))
		elif (msg__=="version=3.3"):
			conn.send("no\n".encode(FORMAT))
		elif (msg__=="ok"):
			SEND()
		elif (msg__=="complete"):
			counter=0

        # msg_length = conn.recv(HEADER).decode(FORMAT)
        # if msg_length:
        #     msg_length = int(msg_length)
        #     msg = conn.recv(msg_length).decode(FORMAT)
        #     if msg == DISCONNECT_MESSAGE:
        #         connected = False
        #     print(f"[{addr}] {msg}")
        #     conn.send("Meg Received".encode(FORMAT))

connection = 0



def SEND():
	global counter
	data = ":"+records[counter]
	connection.send(data.encode(FORMAT))
	counter+=1
	
def start():
    Server.listen()
    print(f"[Listening] server is listening on {SERVER}")
    while True:
        conn , addr =  Server.accept()
        global connection
        connection = conn
		#arg handle_client is the function to be called when a message received from the client.
        thread = threading.Thread(target =handle_client, args=(conn, addr))
		#means regularly check for a received message.
        thread.start()
        print(f"[Active Connections] {threading.activeCount() - 1}")

print("[Starting] the server is starting ...")
start()


#print(SERVER)