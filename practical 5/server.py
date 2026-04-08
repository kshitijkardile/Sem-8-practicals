"""
Server class to simulate backend servers in a load balancing system.
"""
import time
import random


class Server:
    """Represents a backend server that can handle requests."""
    
    def __init__(self, server_id, host, port, capacity=10):
        """
        Initialize a server.
        
        Args:
            server_id: Unique identifier for the server
            host: Server hostname/IP
            port: Server port number
            capacity: Maximum concurrent requests the server can handle
        """
        self.server_id = server_id
        self.host = host
        self.port = port
        self.capacity = capacity
        self.active_requests = 0
        self.total_requests_handled = 0
        self.is_active = True
        self.request_log = []
    
    def handle_request(self, request):
        """
        Process a request if the server has capacity.
        
        Args:
            request: The request object to handle
            
        Returns:
            bool: True if request was accepted, False if server is at capacity
        """
        if not self.is_active:
            return False
        
        if self.active_requests >= self.capacity:
            return False
        
        self.active_requests += 1
        self.total_requests_handled += 1
        
        # Log the request
        self.request_log.append({
            'request_id': request['request_id'],
            'client_ip': request['client_ip'],
            'timestamp': time.time(),
            'processing_time': request.get('processing_time', random.uniform(0.1, 0.5))
        })
        
        return True
    
    def complete_request(self, request_id):
        """
        Mark a request as completed and free up capacity.
        
        Args:
            request_id: ID of the request to complete
        """
        if self.active_requests > 0:
            self.active_requests -= 1
    
    def get_load_percentage(self):
        """Get the current load as a percentage of capacity."""
        if self.capacity == 0:
            return 0
        return (self.active_requests / self.capacity) * 100
    
    def is_overloaded(self):
        """Check if the server is at or near capacity."""
        return self.active_requests >= self.capacity
    
    def toggle_status(self):
        """Toggle server between active and inactive (for simulation)."""
        self.is_active = not self.is_active
    
    def __repr__(self):
        status = "ACTIVE" if self.is_active else "INACTIVE"
        return f"Server({self.server_id}): {self.host}:{self.port} [{status}] - Load: {self.active_requests}/{self.capacity}"
    
    def get_status(self):
        """Get detailed server status."""
        return {
            'server_id': self.server_id,
            'host': self.host,
            'port': self.port,
            'is_active': self.is_active,
            'active_requests': self.active_requests,
            'capacity': self.capacity,
            'load_percentage': self.get_load_percentage(),
            'total_handled': self.total_requests_handled
        }
