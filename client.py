import socket

# Create a socket object
s = socket.socket()

# Define the server's IP address and port
server_ip = '10.0.0.2'
port = 12345

# Connect to the server
s.connect((server_ip, port))

# Receive data from the server
data = s.recv(4096).decode()

# Split the CSV data into rows
rows = data.split("\n")
for row in rows:
    columns = row.split(",")
    print(columns)

# Extract the first column of data
first_column = [row.split(",")[0] for row in rows]

# Convert the first column data to a comma-separated string
first_column_data = ",".join(first_column)

# Send the first column data back to the server
s.sendall(first_column_data.encode())

# Close the connection
s.close()
