#importing system module to use sys.exit to exit the program
import sys
#importing socket module to create the sockets
import socket
#importing threading for multithreading
import threading

# List names to append the names of every connected client (Realtime Record)
names = []
# intializing counter to use whenever required(basically useless)
counter=0
counter1=0
#Connections list of every client to append connection (basically a socket object or identity or address of each client socket)(always different for individuals)
connections = []

# setting up thread locker to lock the state for the thread to avoid inconsistent data while chatting such as lost input if message recieved while typing
lock1 = threading.Lock()

# Function namin defined to recieve the client name from client, appending it into the List names and using broadcast function to send the active users list to all active clients. ( with parameter connection (socket object or socket address))
def naming(connection):
	sender = connection.recv(1024) #storing the name of client in variable sender
	names.append(sender)
	broadcast(str(names))
# The broadcast function to broadcast all the useers the list of all active clients.. List names... ( with parameter connection (socket object or socket address))
def broadcast(message):
#For loop to send all list to all the stored connectin(Socket adresses of client sockets)
    for connection in connections:
        print "Sending %s" % message
        connection.send(message)
# Sendall Function defined and modified To send the recieved message from the sender client to the reciever client
def send_all(message,rconnection):
#again for loop to send the message to the reciever clients socket address stored in rconnections list defined bellow.
    	for connection in rconnection:
		lock1.acquire()#acquiring thread lock
		print "Sending " + message
		connection.send(message)
		lock1.release()#releasing thread lock
#recieve connection to recieve the recievers name from sender client and appending recievers name and socket address in rname and rconnection list resectively
def receive(connection):
    rname= []#stores recievers name
    rconnection=[]# stors recievers socket address
    r1 = connection.recv(1024)#recieves name or reciever from sender client
    rname.append(r1)#append is rname list
    rconnection.append(connections[names.index(r1)])#staring new thread to continuosly recieve msg
    while 1:
#recieves message and stores it in message variable
        message = connection.recv(1024)
        if not message:
	    lock1.acquire()
            connections.remove(connection)
	    lock1.release()
            return
	sender1= names[connections.index(connection)]
# deletes senders name and socket adresses from list to avoid recieving same sent msgs
	del names[connections.index(connection)]
	connections.remove(connection)
	#print str('****'+str(rname)) **Enabe this to see Recievers name list
        send_all(message,rconnection)
	connections.append(connection)# Reappends the senders socket adrress
	names.append(sender1);# reappends the Senders name
	#print str(names) **Enable this to see names list

#try and catch(Exception handling
try:
	socket1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	socket1.bind(('0.0.0.0', 7777))
	socket1.listen(10)
	print "~~~~The Server Is Now Live~~~~"
except socket.error , msg:
	print '[error] Failed To Initialize Server.'+'\n'+'Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
	sys.exit()
#Executes loop while true
while 1:
    (connection, address) = socket1.accept()
    lock1.acquire()
    connections.append(connection)
    lock1.release()
    counter1+=1
    if (counter1>counter):
    	threading.Thread(target = naming, args=[connection]).start()
    	#threading.Thread(target = reciever, args=[connection]).start()
    	threading.Thread(target = receive, args=[connection]).start()
    	counter+=1

