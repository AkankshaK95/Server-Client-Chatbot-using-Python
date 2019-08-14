#importing system module to use sys.exit to exit the program
import sys
#importing socket module to create the sockets
import socket
#importing threading for multithreading
import threading

# setting up thread locker to lock the state for the thread to avoid inconsistent data while chatting such as lost input if message recieved while typing
lock1 = threading.Lock()

#Asking the user his name and storing it in 'name' vairable
name=raw_input("Enter Your Name-> ")

#Defining function to recieve the messages or broadcasts sent from the other users or server respectiely
def recv_loop(connection):
#Only exicutes loop if true
    while True:
#recieving the message from server (maybe a broadcast or message from another user and storing it in variable 'message'
        message = connection.recv(1024)
#if the server is terminated or client recieves empy response then it will display disconnected as mentioned bellow using if condition checking.
        if not message:
            print "Disconnected"
            return #return function to exit the function
#printing the recieved message or broadcast
        print message

#Setting up trial and catch (exception handling while creating the socket.)(Successfully initializes socket when no error and returns the error with error code if some error(socket.error) happens using the except function (catching the error) with error code stored in parameter list msg with stored error message.
try:
	socket1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error , msg:
    print '[error] Failed To Initialize Client'+'\n'+'Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()#sys.exit() to exit the program

#Prints connecting to server if Socket initializd successfully
print "Connecting to server"

#Connects to the Server Socket using server address and port (change the values when required(ip,port)).
socket1.connect(('127.0.0.1', 7777))

#Sends the clients name to the server.
socket1.send(name)

print "Starting receive thread"
#Starts the recieving thread using dunction receive wit argument connection(basically a socket object or identity or address of each client socket)(always different for individuals)
threading.Thread(target=recv_loop, args=[socket1]).start()

#acquiring the thread lock
lock1.acquire()

#asking the user to enter the recievers name
reciever=raw_input("Enter The Person U Wanna Chat with -> ")

#sends the recievers name to the server
socket1.send(reciever)

#releasing the thread lock
lock1.release()
#starting anoter recieve loop thread this time to continuosly recieve messages.
threading.Thread(target=recv_loop, args=[socket1]).start()
#executes loop when true
while True:
#acquiring connection lock
    lock1.acquire()
#Asking user to inpyt the message.
    message = raw_input('You-> ')
#sending the server modified message
    socket1.send("\n"+name+"-> "+message)
#releasing the thread lock.
    lock1.release()
