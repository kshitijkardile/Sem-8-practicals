"""
Main Demonstration Script

Demonstrates load balancing with multiple algorithms:
- Round Robin
- Least Connections
- IP Hash
- Random Selection
- Weighted Round Robin

Run this script to see the simulation in action.
"""
import time
import random
from server import Server
from client_simulator import Client, RequestSimulator
from load_balancer import LoadBalancer


def print_header(text):
    """Print a formatted header."""
    print("\n" + "╔" + "═" * 78 + "╗")
    print(f"║ {text:^76} ║")
    print("╚" + "═" * 78 + "╝")


def print_subheader(text):
    """Print a formatted subheader."""
    print(f"\n{'─' * 80}")
    print(f"  {text}")
    print(f"{'─' * 80}")


def setup_servers(load_balancer, num_servers=4):
    """Create and add servers to the load balancer."""
    print_subheader(f"Setting up {num_servers} servers...")
    
    servers = []
    for i in range(1, num_servers + 1):
        server = Server(
            server_id=f"Server-{i}",
            host=f"192.168.1.{i}",
            port=8000 + i,
            capacity=10
        )
        # Add weight for weighted round robin (optional)
        server.weight = i  # Server-1 has weight 1, Server-2 has weight 2, etc.
        servers.append(server)
        load_balancer.add_server(server)
    
    return servers


def setup_clients(simulator, num_clients=5):
    """Create and add clients to the simulator."""
    print_subheader(f"Setting up {num_clients} clients...")
    
    clients = []
    for i in range(1, num_clients + 1):
        client = Client(
            client_id=f"Client-{i}",
            ip_address=f"10.0.0.{i}"
        )
        clients.append(client)
        simulator.add_client(client)
        print(f"✓ Added {client}")
    
    return clients


def run_simulation(load_balancer, simulator, num_requests=20, algorithm_name=""):
    """Run a simulation with the given algorithm."""
    print_subheader(f"Running simulation: {algorithm_name}")
    print(f"Processing {num_requests} requests...\n")
    
    # Reset counters
    load_balancer.successful_requests = 0
    load_balancer.failed_requests = 0
    load_balancer.request_log = []
    
    # Reset server counters
    for server in load_balancer.servers:
        server.active_requests = 0
        server.total_requests_handled = 0
        server.request_log = []
    
    # Process requests
    for i in range(1, num_requests + 1):
        request = simulator.generate_request()
        print(f"Request {i:2d}: {request['request_id']} from {request['client_ip']}")
        
        server = load_balancer.distribute_request(request)
        
        if server:
            print(f"          → Routed to {server.server_id}")
        else:
            print(f"          → ❌ DROPPED (no available servers)")
        
        # Simulate some requests completing
        if i % 3 == 0:
            for srv in load_balancer.servers:
                if srv.active_requests > 0:
                    srv.complete_request(None)
        
        time.sleep(0.05)  # Small delay for visibility
    
    # Print final status
    load_balancer.print_status()
    
    # Print distribution statistics
    stats = load_balancer.get_stats()
    print("\n📊 Distribution Statistics:")
    for server_id, count in sorted(stats['server_distribution'].items()):
        percentage = (count / num_requests) * 100 if num_requests > 0 else 0
        print(f"  {server_id:15}: {count:3d} requests ({percentage:5.1f}%)")
    
    return stats


def compare_algorithms():
    """Compare all load balancing algorithms side by side."""
    print_header("LOAD BALANCING ALGORITHM COMPARISON")
    
    algorithms = [
        'round_robin',
        'least_connections',
        'ip_hash',
        'random',
        'weighted_round_robin'
    ]
    
    results = {}
    
    for algorithm in algorithms:
        # Create fresh load balancer and simulator
        lb = LoadBalancer(algorithm=algorithm)
        simulator = RequestSimulator()
        
        # Setup
        setup_servers(lb, num_servers=4)
        setup_clients(simulator, num_clients=5)
        
        # Run simulation
        stats = run_simulation(lb, simulator, num_requests=20, algorithm_name=algorithm.upper())
        results[algorithm] = stats
        
        # Brief pause between simulations
        time.sleep(0.5)
    
    # Print comparison
    print_header("ALGORITHM COMPARISON RESULTS")
    
    print(f"\n{'Algorithm':<25} {'Success':>10} {'Failed':>10} {'Distribution':>40}")
    print("─" * 85)
    
    for algo, stats in results.items():
        algo_display = algo.replace('_', ' ').title()
        distribution = ", ".join([f"{k}:{v}" for k, v in sorted(stats['server_distribution'].items())])
        print(f"{algo_display:<25} {stats['successful_requests']:>10} {stats['failed_requests']:>10} {distribution:>40}")
    
    print("\n" + "═" * 85)


def interactive_demo():
    """Run an interactive demonstration."""
    print_header("INTERACTIVE LOAD BALANCING DEMO")
    
    # Create load balancer
    lb = LoadBalancer(algorithm='round_robin')
    simulator = RequestSimulator()
    
    # Setup servers
    setup_servers(lb, num_servers=4)
    
    # Setup clients
    setup_clients(simulator, num_clients=3)
    
    print_subheader("Starting interactive demo...")
    print("Processing 15 requests with Round Robin algorithm\n")
    
    # Process requests
    for i in range(1, 16):
        request = simulator.generate_request()
        print(f"[{i:2d}] {request['client_ip']} → ", end="")
        
        server = lb.distribute_request(request)
        
        if server:
            print(f"✓ {server.server_id}")
        else:
            print("❌ DROPPED")
        
        # Complete some requests periodically
        if i % 5 == 0:
            for srv in lb.servers:
                srv.active_requests = max(0, srv.active_requests - 2)
            lb.print_status()
            time.sleep(0.3)
    
    # Final statistics
    print_subheader("Final Statistics")
    lb.print_status()


def main():
    """Main entry point."""
    print("\n" + "█" * 80)
    print("█" + " " * 78 + "█")
    print("█" + "  LOAD BALANCING SIMULATOR".center(78) + "█")
    print("█" + "  Demonstrating Multiple Load Balancing Algorithms".center(78) + "█")
    print("█" + " " * 78 + "█")
    print("█" * 80)
    
    print("\nThis simulation demonstrates the following load balancing algorithms:")
    print("  1. Round Robin - Sequential distribution")
    print("  2. Least Connections - Sends to least loaded server")
    print("  3. IP Hash - Consistent hashing based on client IP")
    print("  4. Random - Random server selection")
    print("  5. Weighted Round Robin - Weighted distribution")
    
    # Run comparison of all algorithms
    compare_algorithms()
    
    # Optional: Run interactive demo
    print("\n")
    try:
        choice = input("Run interactive demo? (y/n): ").strip().lower()
        if choice == 'y':
            interactive_demo()
    except:
        pass
    
    print("\n" + "█" * 80)
    print("█" + "  SIMULATION COMPLETE".center(78) + "█")
    print("█" * 80 + "\n")


if __name__ == "__main__":
    main()
