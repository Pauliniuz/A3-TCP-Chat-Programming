# A Simple TCP client, used as a warm-up exercise for socket programming assignment.
# Course IELEx2001, NTNU

import random
import time
from socket import *

# Hostname of the server and TCP port number to use
HOST = "localhost"
PORT = 5678

# The socket object (connection to the server and data excahgne will happen using this variable)
client_socket = None


def connect_to_server(host, port):
    """
    Try to establish TCP connection to the server (the three-way handshake).
    :param host: The remote host to connect to. Can be domain (localhost, ntnu.no, etc), or IP address
    :param port: TCP port to use
    :return: True when connection established, false otherwise
    """
    # The "global" keyword is needed so that this function refers to the globally defined client_socket variable
    global client_socket

    client_socket = socket(AF_INET, SOCK_STREAM)

    # TODO - implement this method
    # Remember to catch all possible exceptions the socket can throw in case you have not worked with exceptions,
    # the syntax is as follows:
    try:
        client_socket.connect((host, port)) # Klienten prøver å koble til serveren gjennom port 5678
                                            # Siden funksjonen .connect blir brukt ser vi at dette er en kilent kode.
        return True
    except IOError as e:
        print("Error happened:", e)
        return False

def close_connection():
    """
    Close the TCP connection to the remote server.
    :return: True on success, false otherwise
    """
    # The "global" keyword is needed so that this function refers to the globally defined client_socket variable
    global client_socket

    # TODO - implement this method
    try:
        client_socket.close() #Her logger vi serveren.
        client_socket = None
        return True
    except:
        return False

def send_request_to_server(request):
    """
    :param request: The request message to send. Do NOT include the newline in the message!
    :return: True when message successfully sent, false on error.
    """
    # The "global" keyword is needed so that this function refers to the globally defined client_socket variable
    # global client_socket No it's not needed when we are just looking at the value of the variable

    # TODO - implement this method
    try:
        request += "\n"
        client_socket.send(request.encode()) #Her sender vi en melding gjennom tilkoblings porten.
        return True
    except:
        return False

def read_response_from_server():
    """
    Wait for one response from the remote server.
    :return: The response received from the server, None on error. The newline character is stripped away
     (not included in the returned value).
    """
    # The "global" keyword is needed so that this function refers to the globally defined client_socket variable
    # global client_socket No it's not needed when we are just looking at the value of the variable
    try:
        respons = client_socket.recv(100).decode() #Her lytter vi etter en respons på tilkoblings porten.
        return respons
    except:
        return None

def run_client_tests():
    """
    Runs different "test scenarios" from the TCP client side
    :return: String message that represents the result of the operation
    """
    print("Simple TCP client started")
    if not connect_to_server(HOST, PORT):
        return "ERROR: Failed to connect to the server"

    print("Connection to the server established")
    a = random.randint(1, 20)
    b = random.randint(1, 20)
    request = str(a) + "+" + str(b)

    if not send_request_to_server(request):
        return "ERROR: Failed to send valid message to server!"

    print("Sent ", request, " to server")
    response = read_response_from_server()
    if response is None:
        return "ERROR: Failed to receive server's response!"

    print("Server responded with: ", response)
    seconds_to_sleep = 2 + random.randint(0, 5)
    print("Sleeping %i seconds to allow simulate long client-server connection..." % seconds_to_sleep)
    time.sleep(seconds_to_sleep)

    request = "bla+bla"
    if not send_request_to_server(request):
        return "ERROR: Failed to send invalid message to server!"

    print("Sent " + request + " to server")
    response = read_response_from_server()
    if response is None:
        return "ERROR: Failed to receive server's response!"

    print("Server responded with: ", response)
    if not (send_request_to_server("game over") and close_connection()):
        return "ERROR: Could not finish the conversation with the server"

    print("Game over, connection closed")
    # When the connection is closed, try to send one more message. It should fail.
    if send_request_to_server("2+2"):
        return "ERROR: sending a message after closing the connection did not fail!"

    print("Sending another message after closing the connection failed as expected")
    return "Simple TCP client finished"


# Main entrypoint of the script
if __name__ == '__main__':
    result = run_client_tests()
    print(result)