# A Simple TCP server, used as a warm-up exercise for assignment A3
from socket import *
need_to_run = True
tall = []
for i in range(21):
    tall.append(str(i))

def read_one_line(connection_socket):
    new_line = False
    command = ""
    while not new_line:
        character = connection_socket.recv(1).decode() #Her mottar vi meldinger ved å lytte på tilkoblings porten.
        if character == "\n" or character == "\r":
            new_line = True
        else:
            command += character
    return command

def handle_next_client(connection_socket):
    global need_to_run

    command = ""
    while command == "":
        command = read_one_line(connection_socket)
        if command == "game over":
            need_to_run = False
            respons = "See ya!"
        elif "+" not in command:
            respons = "error: I only do additions."
        elif " " in command:
            respons = "error: No spaces!"
        else:
            j = 0
            numbers = ["", ""]
            for i in range(len(command)):
                if command[i] != "+":
                    numbers[j] += command[i]
                else:
                    j += 1
            if numbers[0] not in tall or numbers[1] not in tall:
                respons = "error: I only do additions with numbers."
            else:
                respons = int(numbers[0]) + int(numbers[1])
    connection_socket.send(str(respons).encode()) #Her sender vi en melding gjennom tilkoblings porten.

def run_server():
    # TODO - implement the logic of the server, according to the protocol.
    # Take a look at the tutorial to understand the basic blocks: creating a listening socket,
    # accepting the next client connection, sending and receiving messages and closing the connection
    print("Starting TCP server...")
    welcome_socket = socket(AF_INET, SOCK_STREAM)
    welcome_socket.bind(("", 5678))
    welcome_socket.listen(1)
    print("Server ready for client connection")

    connection_socket, client_address = welcome_socket.accept() #Serveren prøver å akseptere tilkoblingen forespørt av klienten.
                                                                #Siden .accept funksjonen blir brukt ser vi at dette er en server kode.
    print("Client connected from: ", client_address)

    while need_to_run:
        handle_next_client(connection_socket)

    welcome_socket.close() #Her stenger vi serveren.
    print("Server shutdown")


# Main entrypoint of the script
if __name__ == '__main__':
    run_server()