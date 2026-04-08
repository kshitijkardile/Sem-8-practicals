"""
RPC Client for Remote Factorial Calculation
This client connects to the RPC server and submits requests for factorial calculation.
"""

import xmlrpc.client
import sys


class FactorialClient:
    """Client class to communicate with the RPC server"""
    
    def __init__(self, host='localhost', port=9000):
        """
        Initialize the client with server connection details
        
        Args:
            host: Server host address (default: localhost)
            port: Server port (default: 9000)
        """
        self.server_url = f"http://{host}:{port}"
        try:
            self.server = xmlrpc.client.ServerProxy(self.server_url)
            print(f"Connected to RPC Server at {self.server_url}")
        except Exception as e:
            print(f"Error connecting to server: {e}")
            raise
    
    def request_factorial(self, n):
        """
        Request factorial calculation from the server
        
        Args:
            n: Integer for which factorial is to be calculated
            
        Returns:
            Integer: Factorial of n
        """
        try:
            print(f"\nSending request: Calculate factorial of {n}")
            result = self.server.calculate_factorial(n)
            print(f"Response from server: {n}! = {result}")
            return result
        except xmlrpc.client.Fault as fault:
            print(f"Server returned error: {fault.faultString}")
            return None
        except Exception as e:
            print(f"Error communicating with server: {e}")
            return None
    
    def test_connection(self):
        """Test connection to the server"""
        try:
            status = self.server.get_server_status()
            print(f"Server Status: {status}")
            return True
        except Exception as e:
            print(f"Connection test failed: {e}")
            return False
    
    def echo_test(self, message):
        """Test echo service"""
        try:
            response = self.server.echo(message)
            print(f"Echo response: {response}")
            return response
        except Exception as e:
            print(f"Echo test failed: {e}")
            return None
    
    def get_available_methods(self):
        """List available methods on the server"""
        try:
            methods = self.server.system.listMethods()
            print("\nAvailable RPC methods on server:")
            for method in methods:
                print(f"  - {method}")
            return methods
        except Exception as e:
            print(f"Error listing methods: {e}")
            return None


def interactive_mode(client):
    """Run client in interactive mode"""
    print("\n" + "="*50)
    print("RPC Factorial Client - Interactive Mode")
    print("="*50)
    
    while True:
        print("\nOptions:")
        print("1. Calculate factorial")
        print("2. Test server connection")
        print("3. List available methods")
        print("4. Echo test")
        print("5. Exit")
        
        choice = input("\nEnter your choice (1-5): ").strip()
        
        if choice == '1':
            try:
                n = int(input("Enter an integer to calculate factorial: "))
                client.request_factorial(n)
            except ValueError:
                print("Error: Please enter a valid integer")
        
        elif choice == '2':
            client.test_connection()
        
        elif choice == '3':
            client.get_available_methods()
        
        elif choice == '4':
            message = input("Enter a message to echo: ")
            client.echo_test(message)
        
        elif choice == '5':
            print("Exiting client...")
            break
        
        else:
            print("Invalid choice. Please try again.")


def demo_mode(client):
    """Run client in demo mode with predefined values"""
    print("\n" + "="*50)
    print("RPC Factorial Client - Demo Mode")
    print("="*50)
    
    # Test connection
    print("\nTesting server connection...")
    client.test_connection()
    
    # List available methods
    print("\n" + "-"*50)
    client.get_available_methods()
    
    # Test echo
    print("\n" + "-"*50)
    print("\nTesting echo service...")
    client.echo_test("Hello from RPC Client!")
    
    # Calculate factorials of sample numbers
    print("\n" + "-"*50)
    print("\nCalculating factorials of sample numbers...")
    test_numbers = [0, 1, 5, 10, 15, 20]
    
    for num in test_numbers:
        client.request_factorial(num)
    
    # Test error handling
    print("\n" + "-"*50)
    print("\nTesting error handling...")
    print("\nTest 1: Negative number")
    client.request_factorial(-5)
    
    print("\nTest 2: Very large number")
    client.request_factorial(100000)


if __name__ == "__main__":
    try:
        # Create client instance
        client = FactorialClient(host='localhost', port=9000)
        
        # Check command line arguments
        if len(sys.argv) > 1 and sys.argv[1].lower() == 'demo':
            # Run demo mode
            demo_mode(client)
        else:
            # Run interactive mode
            interactive_mode(client)
    
    except Exception as e:
        print(f"Fatal error: {e}")
        sys.exit(1)
