import socket
import csv

# Input of tree depth
# Timeout
# Time tbd
# Sample data to send
data = [
    ["Name", "Age", "City"],
    ["Alice", "30", "New York"],
    ["Bob", "25", "Los Angeles"],
    ["Charlie", "35", "Chicago"],
]
# Create a socket object
s = socket.socket()

# Define the server's IP address and port
server_ip = '10.0.0.2'
port = 12345

# Bind to the port
s.bind(('', port))

# Listen for incoming connections
s.listen(5)

print("Server is listening on {}:{}".format(server_ip, port))

while True:
    # Accept a connection from a client
    c, addr = s.accept()
    print("Got connection from {}".format(addr))

    # Convert the data to a CSV-formatted string
    csv_data = "\n".join([",".join(row) for row in data])

    # Send the CSV data to the client
    c.sendall(csv_data.encode())

    # Receive data from the client
    client_data = c.recv(4096).decode()

    # Print the list of names received
    names = client_data.split(',')
    print("Here are the Names:")
    for name in names:
        print(name)

    # Close the connection
    c.close()