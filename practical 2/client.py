import xmlrpc.client

# Connect to server
proxy = xmlrpc.client.ServerProxy("http://localhost:8000/")

# Take user input
str1 = input("Enter first string: ")
str2 = input("Enter second string: ")

# Call remote method
result = proxy.concatenate(str1, str2)

# Display result
print("Concatenated String:", result)