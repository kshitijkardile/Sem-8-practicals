"""
Load Balancer Module

Distributes incoming requests among backend servers using various algorithms.
"""
import time
import threading
from algorithms import (
    RoundRobin,
    LeastConnections,
    IPHash,
    RandomSelection,
    WeightedRoundRobin
)


class LoadBalancer:
    """Main load balancer that manages servers and distributes requests."""
    
    # Available algorithms
    ALGORITHMS = {
        'round_robin': RoundRobin,
        'least_connections': LeastConnections,
        'ip_hash': IPHash,
        'random': RandomSelection,
        'weighted_round_robin': WeightedRoundRobin
    }
    
    def __init__(self, algorithm='round_robin'):
        """
        Initialize the load balancer.
        
        Args:
            algorithm: Load balancing algorithm to use (default: 'round_robin')
        """
        self.servers = []
        self.algorithm_name = algorithm
        self.algorithm = self._create_algorithm(algorithm)
        self.request_log = []
        self.failed_requests = 0
        self.successful_requests = 0
        self._lock = threading.Lock()
    
    def _create_algorithm(self, algorithm_name):
        """Create an instance of the specified algorithm."""
        if algorithm_name not in self.ALGORITHMS:
            raise ValueError(f"Unknown algorithm: {algorithm_name}. "
                           f"Available: {list(self.ALGORITHMS.keys())}")
        return self.ALGORITHMS[algorithm_name]()
    
    def add_server(self, server):
        """
        Add a server to the pool.
        
        Args:
            server: Server object to add
        """
        self.servers.append(server)
        print(f"✓ Added server: {server}")
    
    def remove_server(self, server_id):
        """
        Remove a server from the pool.
        
        Args:
            server_id: ID of server to remove
        """
        self.servers = [s for s in self.servers if s.server_id != server_id]
        print(f"✗ Removed server: {server_id}")
    
    def set_algorithm(self, algorithm_name):
        """
        Change the load balancing algorithm.
        
        Args:
            algorithm_name: Name of the algorithm to use
        """
        self.algorithm_name = algorithm_name
        self.algorithm = self._create_algorithm(algorithm_name)
        print(f"⟳ Algorithm changed to: {algorithm_name}")
    
    def distribute_request(self, request):
        """
        Distribute a request to an appropriate server.
        
        Args:
            request: Request object to distribute
            
        Returns:
            Server that will handle the request, or None if all servers are busy
        """
        with self._lock:
            selected_server = self.algorithm.select_server(self.servers, request)
            
            if selected_server is None:
                self.failed_requests += 1
                print(f"✗ Request {request['request_id']} FAILED - No available servers")
                return None
            
            # Try to handle the request
            if selected_server.handle_request(request):
                self.successful_requests += 1
                
                # Log the distribution
                self.request_log.append({
                    'request_id': request['request_id'],
                    'client_ip': request['client_ip'],
                    'server_id': selected_server.server_id,
                    'server_address': f"{selected_server.host}:{selected_server.port}",
                    'timestamp': time.time(),
                    'algorithm': self.algorithm_name
                })
                
                return selected_server
            else:
                self.failed_requests += 1
                print(f"✗ Request {request['request_id']} FAILED - Server {selected_server.server_id} at capacity")
                return None
    
    def get_server_status(self):
        """Get status of all servers."""
        return [server.get_status() for server in self.servers]
    
    def get_stats(self):
        """Get load balancer statistics."""
        server_distribution = {}
        for log_entry in self.request_log:
            server_id = log_entry['server_id']
            server_distribution[server_id] = server_distribution.get(server_id, 0) + 1
        
        return {
            'algorithm': self.algorithm_name,
            'total_servers': len(self.servers),
            'active_servers': len([s for s in self.servers if s.is_active]),
            'successful_requests': self.successful_requests,
            'failed_requests': self.failed_requests,
            'total_requests': self.successful_requests + self.failed_requests,
            'server_distribution': server_distribution,
            'servers': self.get_server_status()
        }
    
    def print_status(self):
        """Print current status of all servers."""
        print("\n" + "="*80)
        print(f"Load Balancer Status - Algorithm: {self.algorithm_name}")
        print("="*80)
        
        if not self.servers:
            print("No servers configured!")
            return
        
        for server in self.servers:
            status = "ACTIVE" if server.is_active else "INACTIVE"
            load_bar = self._create_load_bar(server)
            print(f"{server.server_id:15} | {status:8} | Load: {load_bar} | "
                  f"Total: {server.total_requests_handled}")
        
        print("="*80)
        print(f"Successful: {self.successful_requests} | "
              f"Failed: {self.failed_requests} | "
              f"Total: {self.successful_requests + self.failed_requests}")
        print("="*80 + "\n")
    
    def _create_load_bar(self, server, width=20):
        """Create a visual load bar."""
        load_percentage = server.get_load_percentage() / 100
        filled = int(width * load_percentage)
        empty = width - filled
        
        if load_percentage > 0.8:
            char = '█'
        elif load_percentage > 0.5:
            char = '▓'
        else:
            char = '░'
        
        return f"[{char * filled}{' ' * empty}] {server.active_requests:2d}/{server.capacity:2d}"
    
    def simulate_request_completion(self, delay=0.1):
        """
        Simulate completion of active requests (for simulation purposes).
        
        Args:
            delay: Time to wait between completing requests
        """
        for server in self.servers:
            while server.active_requests > 0:
                server.complete_request(None)
                if delay > 0:
                    time.sleep(delay)
