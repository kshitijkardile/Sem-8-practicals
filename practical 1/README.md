# Distributed RPC Application - Factorial Calculator

## Overview

This project demonstrates a **distributed computing system using Remote Procedure Call (RPC)** where:

- A **client** submits an integer value to a remote server
- The **server** calculates the factorial of that integer
- The **server** returns the result back to the client

## Architecture

```
┌─────────────────┐         RPC Protocol        ┌──────────────────┐
│                 │         (XMLRPC)            │                  │
│  RPC Client     │◄─────────────────────────►  │  RPC Server      │
│                 │                             │                  │
│ • Submits int n │                             │ • Listens: 9000  │
│ • Receives n!   │                             │ • Calculates n!  │
│                 │                             │ • Returns result │
└─────────────────┘                             └──────────────────┘
```

## Technology Stack

- **Language**: Python 3
- **RPC Framework**: XML-RPC (built-in `xmlrpc` library)
- **Protocol**: HTTP-based XML protocol
- **Server**: SimpleXMLRPCServer
- **Communication**: TCP/IP

## Why XML-RPC?

- **Language-agnostic**: Can be used with multiple programming languages
- **Built-in**: No external dependencies required
- **Lightweight**: Suitable for learning RPC concepts
- **Platform-independent**: Works on Windows, Linux, macOS
- **Easy to debug**: Uses standard HTTP and XML

## Project Structure

```
practical 1/
├── rpc_server.py      # Server implementation
├── rpc_client.py      # Client implementation
├── README.md          # Documentation
└── requirements.txt   # Dependencies (none for this project)
```

## Installation & Setup

### Prerequisites

- Python 3.6 or higher
- No external dependencies (using Python standard library)

### Quick Start

**Step 1: Start the Server**

Open a terminal/PowerShell and run:

```bash
python rpc_server.py
```

Expected output:

```
RPC Server started on localhost:9000
Registered methods:
  - calculate_factorial(n): Calculate factorial of integer n
  - get_server_status(): Get server status
  - echo(message): Echo a test message

Waiting for client requests... Press Ctrl+C to stop
```

**Step 2: Run the Client (in another terminal)**

```bash
# Interactive mode (menu-driven)
python rpc_client.py

# OR Demo mode (with predefined test cases)
python rpc_client.py demo
```

## Usage

### Interactive Mode

When you run the client without arguments, it launches an interactive menu:

```
==================================================
RPC Factorial Client - Interactive Mode
==================================================

Options:
1. Calculate factorial
2. Test server connection
3. List available methods
4. Echo test
5. Exit

Enter your choice (1-5): _
```

**Example Session:**

```
Enter your choice (1-5): 1
Enter an integer to calculate factorial: 5

Sending request: Calculate factorial of 5
Response from server: 5! = 120
```

### Demo Mode

Run the client in demo mode to automatically test all features:

```bash
python rpc_client.py demo
```

This will:

- Test server connection
- List available RPC methods
- Test echo service
- Calculate factorials for: 0, 1, 5, 10, 15, 20
- Test error handling with invalid inputs

## API Reference

### Server Methods

#### `calculate_factorial(n: int) -> int`

Calculates the factorial of a non-negative integer.

**Parameters:**

- `n` (int): Non-negative integer

**Returns:**

- (int): Factorial of n

**Raises:**

- `ValueError`: If n is negative or greater than 10000

**Example:**

```python
result = server.calculate_factorial(5)  # Returns 120
```

#### `get_server_status() -> str`

Returns the current status of the server.

**Returns:**

- (str): Server status message

**Example:**

```python
status = server.get_server_status()
# Returns: "RPC Factorial Server is running and ready to serve requests"
```

#### `echo(message: str) -> str`

Echoes back the message sent by the client (for testing connectivity).

**Parameters:**

- `message` (str): Message to echo

**Returns:**

- (str): Echoed message with "Server received: " prefix

**Example:**

```python
response = server.echo("Hello")
# Returns: "Server received: Hello"
```

## Test Cases & Examples

### Test Case 1: Basic Factorial

```
Input: 5
Expected Output: 120 (5! = 5×4×3×2×1 = 120)
```

### Test Case 2: Edge Cases

```
Input: 0
Expected Output: 1 (0! = 1 by definition)

Input: 1
Expected Output: 1 (1! = 1)
```

### Test Case 3: Larger Numbers

```
Input: 10
Expected Output: 3628800

Input: 20
Expected Output: 2432902008176640000
```

### Test Case 4: Error Handling

```
Input: -5
Expected Output: ValueError - "Factorial is not defined for negative numbers"

Input: 100000
Expected Output: ValueError - "Number is too large (max: 10000)"
```

## Implementation Details

### Server-Side (rpc_server.py)

**Key Components:**

1. **FactorialService Class**
   - Encapsulates the factorial calculation logic
   - Provides input validation
   - Handles edge cases and errors

2. **SimpleXMLRPCServer**
   - Listens on port 9000
   - Accepts HTTP POST requests
   - Serializes/deserializes data to/from XML
   - Handles multiple client connections

3. **Error Handling**
   - Validates input (must be integer)
   - Checks for negative numbers
   - Limits maximum value to prevent memory issues
   - Returns descriptive error messages

### Client-Side (rpc_client.py)

**Key Components:**

1. **FactorialClient Class**
   - Manages connection to server
   - Sends RPC requests
   - Handles responses
   - Implements error handling

2. **Interactive Mode**
   - Menu-driven interface
   - Continuous operation
   - User-friendly prompts

3. **Demo Mode**
   - Automated testing
   - Demonstrates all features
   - Validates error handling

## How RPC Works - Step by Step

### Request Flow:

1. **Client Call**: `client.request_factorial(5)`
2. **Serialization**: Convert to XML-RPC format
3. **Transport**: Send HTTP POST to http://localhost:9000
4. **Server Parse**: Deserialize XML-RPC request
5. **Execution**: Run `calculate_factorial(5)` on server
6. **Server Response**: Serialize result (120) to XML-RPC
7. **Transport**: Send HTTP response to client
8. **Client Parse**: Deserialize XML-RPC response
9. **Result**: Return 120 to client code

### Example XML-RPC Request:

```xml
<?xml version='1.0'?>
<methodCall>
  <methodName>calculate_factorial</methodName>
  <params>
    <param>
      <value><int>5</int></value>
    </param>
  </params>
</methodCall>
```

### Example XML-RPC Response:

```xml
<?xml version='1.0'?>
<methodResponse>
  <params>
    <param>
      <value><int>120</int></value>
    </param>
  </params>
</methodResponse>
```

## Configuration

### Change Server Port

In `rpc_server.py`, modify the port in the main block:

```python
if __name__ == "__main__":
    start_server(port=9001)  # Change to 9001
```

### Change Server Host

To accept connections from other machines:

```python
if __name__ == "__main__":
    start_server(host='0.0.0.0', port=9000)
```

### Connect to Remote Server

In `rpc_client.py`:

```python
client = FactorialClient(host='192.168.1.100', port=9000)
```

## Troubleshooting

| Issue                    | Cause                             | Solution                                        |
| ------------------------ | --------------------------------- | ----------------------------------------------- |
| "Connection refused"     | Server not running                | Start the server first (`python rpc_server.py`) |
| Port already in use      | Another process on port 9000      | Change port or kill process using port 9000     |
| "Address already in use" | Server crash, socket not released | Wait 30 seconds or use different port           |
| Timeout error            | Server crashed/paused             | Restart the server                              |
| "Not an integer" error   | Sent string instead of int        | Ensure you input a valid integer                |

## Learning Outcomes

After completing this practical, you should understand:

1. **RPC Fundamentals**
   - How remote procedure calls work
   - Client-server communication model
   - Serialization/deserialization

2. **Network Programming**
   - HTTP protocol basics
   - Message passing
   - Error handling in distributed systems

3. **Distributed Systems Concepts**
   - Separation of concerns
   - Network latency and timeouts
   - Fault tolerance

4. **Software Design**
   - Service-oriented architecture
   - Client-server architecture
   - API design

## Advanced Exercises

1. **Add more operations**: Implement GCD, LCM, Prime checking
2. **Security**: Add authentication/authorization
3. **Logging**: Log all client requests server-side
4. **Performance**: Measure RPC overhead vs local computation
5. **Alternative RPC**: Implement using gRPC or sockets
6. **Multi-client**: Test with multiple concurrent clients
7. **Persistence**: Store computation history
8. **Load Balancing**: Implement multiple servers

## References

- [Python xmlrpc Documentation](https://docs.python.org/3/library/xmlrpc.html)
- [XML-RPC Specification](http://xmlrpc.scripting.com/)
- [RPC Concepts](https://en.wikipedia.org/wiki/Remote_procedure_call)
- [Distributed Systems Fundamentals](https://en.wikipedia.org/wiki/Distributed_computing)

## Conclusion

This project provides a practical demonstration of RPC-based distributed computing. The factorial calculation serves as a simple example, but the pattern can be extended to more complex distributed systems.

---

**Author**: Academic Practical Assignment  
**Date**: 2026  
**Language**: Python 3  
**Difficulty**: Beginner to Intermediate
