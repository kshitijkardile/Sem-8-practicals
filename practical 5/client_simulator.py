"""
Client Request Simulator Module

Simulates clients sending requests to the load balancer.
"""
import random
import time
import uuid


class Client:
    """Represents a client that sends requests."""
    
    def __init__(self, client_id=None, ip_address=None):
        """
        Initialize a client.
        
        Args:
            client_id: Unique identifier for the client
            ip_address: Client's IP address
        """
        self.client_id = client_id or str(uuid.uuid4())[:8]
        self.ip_address = ip_address or self._generate_random_ip()
        self.request_count = 0
    
    def _generate_random_ip(self):
        """Generate a random IP address for simulation."""
        return f"192.168.{random.randint(1, 255)}.{random.randint(1, 255)}"
    
    def create_request(self, processing_time=None):
        """
        Create a request to send to the load balancer.
        
        Args:
            processing_time: Simulated processing time (random if None)
            
        Returns:
            dict: Request object with metadata
        """
        self.request_count += 1
        
        return {
            'request_id': str(uuid.uuid4())[:12],
            'client_id': self.client_id,
            'client_ip': self.ip_address,
            'timestamp': time.time(),
            'processing_time': processing_time or random.uniform(0.1, 0.5),
            'request_type': random.choice(['GET', 'POST', 'PUT', 'DELETE']),
            'payload_size': random.randint(100, 10000)  # bytes
        }
    
    def __repr__(self):
        return f"Client({self.client_id}): {self.ip_address}"


class RequestSimulator:
    """Simulates multiple clients sending requests."""
    
    def __init__(self):
        self.clients = []
        self.total_requests_generated = 0
    
    def add_client(self, client=None, ip_address=None):
        """
        Add a client to the simulator.
        
        Args:
            client: Client object (creates one if None)
            ip_address: Specific IP address for new client
        """
        if client is None:
            client = Client(ip_address=ip_address)
        self.clients.append(client)
        return client
    
    def generate_request(self, client_index=None, processing_time=None):
        """
        Generate a request from a specific or random client.
        
        Args:
            client_index: Index of client to use (random if None)
            processing_time: Specific processing time
            
        Returns:
            dict: Request object
        """
        if not self.clients:
            raise ValueError("No clients available. Add clients first.")
        
        if client_index is None:
            client = random.choice(self.clients)
        else:
            client = self.clients[client_index % len(self.clients)]
        
        request = client.create_request(processing_time)
        self.total_requests_generated += 1
        
        return request
    
    def generate_batch(self, num_requests, delay=0):
        """
        Generate a batch of requests.
        
        Args:
            num_requests: Number of requests to generate
            delay: Delay between requests (seconds)
            
        Returns:
            list: List of request objects
        """
        requests = []
        for i in range(num_requests):
            request = self.generate_request()
            requests.append(request)
            if delay > 0:
                time.sleep(delay)
        
        return requests
    
    def get_stats(self):
        """Get simulator statistics."""
        return {
            'total_clients': len(self.clients),
            'total_requests_generated': self.total_requests_generated,
            'clients': [
                {
                    'client_id': c.client_id,
                    'ip_address': c.ip_address,
                    'requests_sent': c.request_count
                }
                for c in self.clients
            ]
        }
