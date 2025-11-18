# Project Documentation

## Current Project: Hello World

This is a simple Hello World application written in Python.

### Files
- `hello.py` - Main application file that prints "Hello World" to the console

### Running the Application

```bash
python hello.py
```

### Output
```
Hello World
```

## Development History

### Initial Release
- Created basic Python application
- Implemented Hello World functionality
- All code written by AI agents following project rules

## Future Development

This project can evolve in any direction. Future features and functionality will be determined through human-AI collaboration, with all implementation handled by AI agents.

---

*This project follows AI-agent-only development rules. See [README.md](README.md) for details.*


---

## Current Project: Network Traffic Monitor

A real-time network packet analyzer that captures and analyzes network traffic with live statistics and anomaly detection.

### Files

- `network_monitor.py` - Main network monitoring application with packet capture and analysis capabilities

### Features

- **Real-time Packet Capture**: Captures network packets using Scapy
- **Protocol Analysis**: Identifies and counts TCP, UDP, ICMP, and ARP packets
- **Live Statistics Dashboard**: Shows:
  - Protocol distribution with ASCII bar charts
  - Top source IPs ("top talkers")
  - Most accessed destination ports with service identification
  - Recent packet details (last 10)
- **Anomaly Detection**: Flags suspicious IPs based on packet volume
- **Service Port Mapping**: Identifies common services (HTTP, HTTPS, SSH, FTP, etc.)
- **Export Functionality**: Saves analysis results to text file

### Running the Application

**Prerequisites:**
```bash
pip install scapy
```

**Basic Usage (requires admin/root privileges):**
```bash
# Linux/Mac:
sudo python3 network_monitor.py

# Windows (Run PowerShell as Administrator):
python network_monitor.py
```

**Advanced Usage with Filters:**
```python
# Monitor only HTTP traffic
monitor.start(filter_str='tcp port 80')

# Monitor only HTTPS traffic
monitor.start(filter_str='tcp port 443')

# Monitor specific host
monitor.start(filter_str='host 192.168.1.1')

# Monitor specific interface
monitor.start(interface='eth0')
```

### Output

The tool provides:
- Real-time terminal dashboard (updates every 2 seconds)
- Packet rate statistics
- Protocol distribution visualization
- Suspicious activity alerts (⚠️ warnings)
- Exported analysis report (`network_stats.txt`)

### Use Cases

- Network traffic analysis and monitoring
- Detecting unusual network behavior
- Understanding protocol distributions
- Identifying top bandwidth consumers
- Educational tool for learning network protocols
- Basic intrusion detection

### Security Note

This tool requires elevated privileges to capture network packets. Use responsibly and only on networks you own or have permission to monitor.
