import socket

# Test Data
data = data = [
    ['Age', 'Income', 'Student', 'Credit_Rating', 'BuyComputer'],
    ['Young', 'High', 'No', 'Fair', 'No'],
    ['Young', 'High', 'No', 'Excellent', 'No'],
    ['Young', 'Medium', 'No', 'Fair', 'Yes'],
    ['Young', 'Low', 'Yes', 'Fair', 'Yes'],
    ['Young', 'Low', 'Yes', 'Excellent', 'No'],
    ['Middle', 'Low', 'Yes', 'Excellent', 'Yes'],
    ['Middle', 'High', 'No', 'Fair', 'Yes'],
    ['Middle', 'Low', 'Yes', 'Excellent', 'Yes'],
    ['Middle', 'High', 'Yes', 'Excellent', 'Yes'],
    ['Middle', 'Medium', 'Yes', 'Fair', 'Yes'],
    ['Old', 'Medium', 'Yes', 'Fair', 'Yes'],
    ['Old', 'Medium', 'No', 'Fair', 'Yes'],
    ['Old', 'Medium', 'No', 'Excellent', 'Yes'],
    ['Old', 'High', 'Yes', 'Excellent', 'No'],
]

def send_data(client_socket, data_to_send):
    csv_data = "\n".join([",".join(row) for row in data_to_send])
    client_socket.sendall(csv_data.encode())

# Create a socket object
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Define the server's IP address and port
server_ip = '10.0.0.2'
port = 12345

# Bind to the port
s.bind(('', port))

# Listen for incoming connections
s.listen(5)

print("Server is listening on {}:{}".format(server_ip, port))

def receive_tree(client_socket):
    received_data = client_socket.recv(4096).decode()
    return received_data.split("\n")

# (The part where the server waits for a connection)

while True:
    # Accept a connection from a client
    c, addr = s.accept()
    print("Got connection from {}".format(addr))

    # Send the test data to the client
    send_data(c, data)

    # Receive the serialized tree from the client
    serialized_tree = receive_tree(c)

    print("Serialized Tree received:")
    print(serialized_tree)

    # Close the connection
    c.close()