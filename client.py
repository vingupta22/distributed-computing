from collections import Counter
import math
import socket 

class TreeNode:
    def __init__(self, attribute=None, label=None):
        self.attribute = attribute
        self.label = label
        self.children = {}

def receive_data(server_socket):
    received_data = server_socket.recv(4096).decode()
    return [row.split(",") for row in received_data.split("\n")]

# Create a socket object
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Define the server's IP address and port
server_ip = '10.0.0.2'
port = 12345

# Connect to the server
s.connect((server_ip, port))

# Receive data from the server (contains the test data)
data = receive_data(s)

def calculate_entropy(data):
    target_labels = [row[-1] for row in data]
    label_counts = {}
    for label in target_labels:
        if label in label_counts:
            label_counts[label] += 1
        else:
            label_counts[label] = 1

    entropy = 0.0
    total_samples = len(target_labels)
    for count in label_counts.values():
        probability = float(count) / total_samples
        entropy -= probability * math.log(probability, 2)

    return entropy

def split_data(data, attribute_index, value):
    return [row for row in data if row[attribute_index] == value]

def create_tree(data, depth):
    root = TreeNode()
    
    if depth <= 0 or not data or len(data[0]) <= 1:
        labels = [row[-1] for row in data]
        root.label = max(set(labels), key=labels.count)
        return root

    if all(row[-1] == data[0][-1] for row in data):
        root.label = data[0][-1]
        return root

    entropy = calculate_entropy(data)
    num_attributes = len(data[0]) - 1

    max_info_gain = 0
    best_attribute = None

    for attribute_index in range(num_attributes):
        values = set([row[attribute_index] for row in data])
        info_gain = 0
        for value in values:
            sub_data = split_data(data, attribute_index, value)
            prob = len(sub_data) / float(len(data))
            info_gain += prob * calculate_entropy(sub_data)
        info_gain = entropy - info_gain

        if info_gain > max_info_gain:
            max_info_gain = info_gain
            best_attribute = attribute_index

    root.attribute = best_attribute

    values = set([row[best_attribute] for row in data])
    for value in values:
        sub_data = split_data(data, best_attribute, value)
        root.children[value] = create_tree(sub_data, depth - 1)

    return root

# (Previous code)

def serialize_tree(root):
    if root:
        serialized = []
        if root.label:
            serialized.append("Label:" + root.label)
        else:
            serialized.append("Attribute:" + str(root.attribute))
            for value, child_node in root.children.items():
                serialized.append(value)
                serialized.extend(serialize_tree(child_node))
        return serialized

decision_tree_depth = 5
tree_root = create_tree(data, decision_tree_depth)

serialized_tree = serialize_tree(tree_root)

# Create a socket object
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Define the server's IP address and port
server_ip = '10.0.0.2'
port = 12345

# Connect to the server
s.connect((server_ip, port))

serialized_tree_str = '\n'.join(serialized_tree)

# Send the serialized tree to the server
s.sendall(serialized_tree_str.encode())

# Close the connection
s.close()



"""
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
"""