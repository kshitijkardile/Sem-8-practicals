# Load Balancing Simulator

A Python-based simulation of client request distribution among backend servers using multiple load balancing algorithms.

## Features

- **Multiple Load Balancing Algorithms:**
  - Round Robin
  - Least Connections
  - IP Hash
  - Random Selection
  - Weighted Round Robin

- **Server Simulation:**
  - Configurable server capacity
  - Active/Inactive server status
  - Load tracking and monitoring
  - Request handling simulation

- **Client Simulation:**
  - Multiple clients with unique IPs
  - Random request generation
  - Configurable request properties

- **Real-time Monitoring:**
  - Visual load bars
  - Distribution statistics
  - Success/failure tracking
  - Server status reporting

## Project Structure

```
practical 5/
│
├── server.py              # Server class implementation
├── algorithms.py          # Load balancing algorithms
├── client_simulator.py    # Client and request simulation
├── load_balancer.py       # Load balancer implementation
├── main.py               # Main demonstration script
└── README.md             # This file
```

## Algorithm Descriptions

### 1. Round Robin
Distributes requests sequentially across servers in a circular manner.
- **Pros:** Simple, fair distribution
- **Cons:** Doesn't account for server load or capacity differences
- **Use Case:** Homogeneous servers with similar processing times

### 2. Least Connections
Sends requests to the server with the fewest active connections.
- **Pros:** Adapts to varying request processing times
- **Cons:** May overwhelm servers when traffic spikes
- **Use Case:** Varying request durations, dynamic workloads

### 3. IP Hash
Uses client IP address to determine which server handles the request.
- **Pros:** Session affinity (same client → same server)
- **Cons:** Can lead to uneven distribution
- **Use Case:** When session persistence is required

### 4. Random Selection
Randomly selects a server from available servers.
- **Pros:** Simple, no state management needed
- **Cons:** Can lead to uneven distribution
- **Use Case:** Quick implementation, homogeneous servers

### 5. Weighted Round Robin
Like round robin, but servers with higher weights receive more requests.
- **Pros:** Accounts for different server capacities
- **Cons:** Requires manual weight configuration
- **Use Case:** Heterogeneous servers with different capacities

## Installation

No external dependencies required! Uses only Python standard library.

```bash
# Requires Python 3.6+
python --version
```

## Usage

### Run the Full Demo

```bash
python main.py
```

This will:
1. Compare all 5 algorithms side-by-side
2. Show distribution statistics
3. Offer an interactive demo option

### Use Individual Components

```python
from server import Server
from client_simulator import Client, RequestSimulator
from load_balancer import LoadBalancer

# Create load balancer with specific algorithm
lb = LoadBalancer(algorithm='round_robin')

# Add servers
server1 = Server("Server-1", "192.168.1.1", 8001, capacity=10)
lb.add_server(server1)

# Create client simulator
simulator = RequestSimulator()
client = Client("Client-1", "10.0.0.1")
simulator.add_client(client)

# Generate and distribute requests
request = simulator.generate_request()
selected_server = lb.distribute_request(request)

# View statistics
lb.print_status()
stats = lb.get_stats()
```

## Output Example

```
================================================================================
Load Balancer Status - Algorithm: round_robin
================================================================================
Server-1        | ACTIVE   | Load: [░░                  ]  1/10 | Total: 5
Server-2        | ACTIVE   | Load: [░░                  ]  1/10 | Total: 5
Server-3        | ACTIVE   | Load: [░░                  ]  1/10 | Total: 5
Server-4        | ACTIVE   | Load: [░░                  ]  1/10 | Total: 5
================================================================================
Successful: 20 | Failed: 0 | Total: 20
================================================================================

📊 Distribution Statistics:
  Server-1       :   5 requests ( 25.0%)
  Server-2       :   5 requests ( 25.0%)
  Server-3       :   5 requests ( 25.0%)
  Server-4       :   5 requests ( 25.0%)
```

## Customization

### Change Algorithm

```python
lb.set_algorithm('least_connections')
```

### Add Server with Custom Weight

```python
server = Server("Server-1", "192.168.1.1", 8001, capacity=10)
server.weight = 5  # Higher weight = more requests
lb.add_server(server)
```

### Simulate Server Failure

```python
server.toggle_status()  # Deactivate server
```

### Generate Batch Requests

```python
requests = simulator.generate_batch(num_requests=50, delay=0.1)
for request in requests:
    lb.distribute_request(request)
```

## Architecture

```
┌─────────────┐
│   Clients   │
└──────┬──────┘
       │ Requests
       ▼
┌─────────────────┐
│ Load Balancer   │
│  (Algorithm)    │
└──────┬──────────┘
       │ Distributes
       ▼
┌──────────┐  ┌──────────┐  ┌──────────┐
│ Server 1 │  │ Server 2 │  │ Server 3 │
└──────────┘  └──────────┘  └──────────┘
```

## Key Classes

- **Server:** Represents a backend server with capacity tracking
- **Client:** Represents a client that generates requests
- **RequestSimulator:** Manages multiple clients and request generation
- **LoadBalancer:** Central component that distributes requests
- **LoadBalancingAlgorithm:** Abstract base for all algorithms

## License

Educational use - Free to modify and distribute
