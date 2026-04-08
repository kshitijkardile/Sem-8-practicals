from xmlrpc.server import SimpleXMLRPCServer

def concatenate(str1, str2):
    print(f"Received from client: '{str1}' and '{str2}'")
    result = str1 + str2
    print(f"Sending result: '{result}'")
    return result

server = SimpleXMLRPCServer(("localhost", 8000))
print("Server is running on port 8000...")

server.register_function(concatenate, "concatenate")

server.serve_forever()