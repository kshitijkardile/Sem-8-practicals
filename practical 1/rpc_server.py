"""
RPC Server for Factorial Calculation
This server listens for client requests and calculates factorials.
"""

from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
import math

class FactorialService:
    """Service class that provides factorial calculation"""
    
    def calculate_factorial(self, n):
        """
        Calculate factorial of a given number
        
        Args:
            n: Integer for which factorial is to be calculated
            
        Returns:
            Integer: Factorial of n
            
        Raises:
            ValueError: If n is negative or not an integer
        """
        # Validate input
        if not isinstance(n, int):
            raise ValueError("Input must be an integer")
        
        if n < 0:
            raise ValueError("Factorial is not defined for negative numbers")
        
        if n > 10000:
            raise ValueError("Number is too large (max: 10000)")
        
        # Calculate factorial
        try:
            result = math.factorial(n)
            return result
        except Exception as e:
            raise ValueError(f"Error calculating factorial: {str(e)}")
    
    def get_server_status(self):
        """
        Returns the status of the server
        
        Returns:
            String: Status message
        """
        return "RPC Factorial Server is running and ready to serve requests"
    
    def echo(self, message):
        """
        Echo service to test connectivity
        
        Args:
            message: Message to echo back
            
        Returns:
            String: Echoed message
        """
        return f"Server received: {message}"


def start_server(host='localhost', port=9000):
    """
    Start the RPC server
    
    Args:
        host: Server host address (default: localhost)
        port: Server port (default: 9000)
    """
    # Create server
    server = SimpleXMLRPCServer((host, port),
                               requestHandler=SimpleXMLRPCRequestHandler,
                               allow_none=True)
    
    # Register the service
    service = FactorialService()
    server.register_instance(service)
    
    # Enable introspection
    server.register_introspection_functions()
    
    print(f"RPC Server started on {host}:{port}")
    print("Registered methods:")
    print("  - calculate_factorial(n): Calculate factorial of integer n")
    print("  - get_server_status(): Get server status")
    print("  - echo(message): Echo a test message")
    print("\nWaiting for client requests... Press Ctrl+C to stop")
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer shutdown initiated...")
        server.server_close()
        print("Server stopped")


if __name__ == "__main__":
    start_server()
