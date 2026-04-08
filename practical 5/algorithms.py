"""
Load Balancing Algorithms Module

Implements various load balancing algorithms:
- Round Robin
- Least Connections
- IP Hash
- Random
- Weighted Round Robin
"""
import random
import hashlib
from abc import ABC, abstractmethod


class LoadBalancingAlgorithm(ABC):
    """Abstract base class for load balancing algorithms."""
    
    @abstractmethod
    def select_server(self, servers, request=None):
        """
        Select a server from the pool.
        
        Args:
            servers: List of available Server objects
            request: The request being processed (may be None for some algorithms)
            
        Returns:
            Server object or None if no server is available
        """
        pass


class RoundRobin(LoadBalancingAlgorithm):
    """
    Round Robin Algorithm: Distributes requests sequentially across servers.
    Simple and ensures equal distribution.
    """
    
    def __init__(self):
        self.current_index = 0
    
    def select_server(self, servers, request=None):
        active_servers = [s for s in servers if s.is_active and not s.is_overloaded()]
        
        if not active_servers:
            return None
        
        server = active_servers[self.current_index % len(active_servers)]
        self.current_index = (self.current_index + 1) % len(active_servers)
        
        return server


class LeastConnections(LoadBalancingAlgorithm):
    """
    Least Connections Algorithm: Sends requests to the server with fewest active connections.
    Good for varying request processing times.
    """
    
    def select_server(self, servers, request=None):
        active_servers = [s for s in servers if s.is_active and not s.is_overloaded()]
        
        if not active_servers:
            return None
        
        # Select server with minimum active requests
        return min(active_servers, key=lambda s: s.active_requests)


class IPHash(LoadBalancingAlgorithm):
    """
    IP Hash Algorithm: Uses client IP to determine which server handles the request.
    Ensures session affinity (same client → same server).
    """
    
    def select_server(self, servers, request=None):
        active_servers = [s for s in servers if s.is_active and not s.is_overloaded()]
        
        if not active_servers:
            return None
        
        if request is None or 'client_ip' not in request:
            # Fallback to round robin if no IP available
            return active_servers[0]
        
        # Hash the client IP to determine server
        ip_hash = int(hashlib.md5(request['client_ip'].encode()).hexdigest(), 16)
        server_index = ip_hash % len(active_servers)
        
        return active_servers[server_index]


class RandomSelection(LoadBalancingAlgorithm):
    """
    Random Algorithm: Randomly selects a server from available servers.
    Simple but can lead to uneven distribution.
    """
    
    def select_server(self, servers, request=None):
        active_servers = [s for s in servers if s.is_active and not s.is_overloaded()]
        
        if not active_servers:
            return None
        
        return random.choice(active_servers)


class WeightedRoundRobin(LoadBalancingAlgorithm):
    """
    Weighted Round Robin: Like round robin but servers have weights.
    Higher weight servers get more requests.
    """
    
    def __init__(self):
        self.current_index = 0
        self.current_weight = 0
    
    def _get_gcd(self, a, b):
        """Calculate greatest common divisor."""
        while b:
            a, b = b, a % b
        return a
    
    def _get_max_weight(self, servers):
        """Get maximum weight from servers."""
        return max([getattr(s, 'weight', 1) for s in servers], default=1)
    
    def _get_gcd_of_weights(self, servers):
        """Get GCD of all server weights."""
        weights = [getattr(s, 'weight', 1) for s in servers]
        if not weights:
            return 1
        gcd = weights[0]
        for w in weights[1:]:
            gcd = self._get_gcd(gcd, w)
        return gcd
    
    def select_server(self, servers, request=None):
        active_servers = [s for s in servers if s.is_active and not s.is_overloaded()]
        
        if not active_servers:
            return None
        
        max_weight = self._get_max_weight(active_servers)
        gcd_weight = self._get_gcd_of_weights(active_servers)
        
        while True:
            self.current_index = (self.current_index + 1) % len(active_servers)
            
            if self.current_index == 0:
                self.current_weight = self.current_weight - gcd_weight
                if self.current_weight <= 0:
                    self.current_weight = max_weight
                    if self.current_weight == 0:
                        return None
            
            server = active_servers[self.current_index]
            server_weight = getattr(server, 'weight', 1)
            
            if server_weight >= self.current_weight:
                return server
