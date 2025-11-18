"""
Real-Time Network Traffic Analyzer
Captures packets, analyzes protocols, and visualizes traffic patterns
"""

from scapy.all import sniff, IP, TCP, UDP, ICMP, ARP
from collections import defaultdict, deque
import threading
import time
from datetime import datetime
import os

class NetworkMonitor:
    def __init__(self, max_packets=1000):
        self.packets = deque(maxlen=max_packets)
        self.protocol_stats = defaultdict(int)
        self.ip_stats = defaultdict(int)
        self.port_stats = defaultdict(int)
        self.suspicious_ips = set()
        self.running = False
        self.start_time = None
        
    def analyze_packet(self, packet):
        """Analyze individual packet for interesting data"""
        packet_info = {
            'timestamp': datetime.now().strftime('%H:%M:%S'),
            'protocol': 'Unknown',
            'src': 'N/A',
            'dst': 'N/A',
            'length': len(packet)
        }
        
        # IP Layer analysis
        if IP in packet:
            packet_info['src'] = packet[IP].src
            packet_info['dst'] = packet[IP].dst
            self.ip_stats[packet[IP].src] += 1
            
            # Check for potential port scanning (simple heuristic)
            if self.ip_stats[packet[IP].src] > 100:
                self.suspicious_ips.add(packet[IP].src)
        
        # Protocol identification
        if TCP in packet:
            packet_info['protocol'] = 'TCP'
            packet_info['sport'] = packet[TCP].sport
            packet_info['dport'] = packet[TCP].dport
            self.port_stats[packet[TCP].dport] += 1
            self.protocol_stats['TCP'] += 1
            
        elif UDP in packet:
            packet_info['protocol'] = 'UDP'
            packet_info['sport'] = packet[UDP].sport
            packet_info['dport'] = packet[UDP].dport
            self.port_stats[packet[UDP].dport] += 1
            self.protocol_stats['UDP'] += 1
            
        elif ICMP in packet:
            packet_info['protocol'] = 'ICMP'
            self.protocol_stats['ICMP'] += 1
            
        elif ARP in packet:
            packet_info['protocol'] = 'ARP'
            self.protocol_stats['ARP'] += 1
        
        self.packets.append(packet_info)
        return packet_info
    
    def packet_handler(self, packet):
        """Callback for each captured packet"""
        if self.running:
            self.analyze_packet(packet)
    
    def display_stats(self):
        """Display real-time statistics"""
        while self.running:
            os.system('cls' if os.name == 'nt' else 'clear')
            
            elapsed = time.time() - self.start_time
            print("=" * 80)
            print(f"{'NETWORK TRAFFIC MONITOR':^80}")
            print("=" * 80)
            print(f"Running for: {elapsed:.1f}s | Packets captured: {len(self.packets)}")
            print(f"Rate: {len(self.packets)/elapsed:.2f} packets/sec\n")
            
            # Protocol distribution
            print("PROTOCOL DISTRIBUTION:")
            print("-" * 40)
            total = sum(self.protocol_stats.values())
            if total > 0:
                for proto, count in sorted(self.protocol_stats.items(), key=lambda x: x[1], reverse=True):
                    bar = '█' * int((count/total) * 30)
                    print(f"{proto:8s} | {bar:30s} {count:5d} ({count/total*100:5.1f}%)")
            
            # Top talkers
            print("\nTOP SOURCE IPs:")
            print("-" * 40)
            for ip, count in sorted(self.ip_stats.items(), key=lambda x: x[1], reverse=True)[:5]:
                suspicious = " ⚠️ SUSPICIOUS" if ip in self.suspicious_ips else ""
                print(f"{ip:15s} : {count:5d} packets{suspicious}")
            
            # Top destination ports
            print("\nTOP DESTINATION PORTS:")
            print("-" * 40)
            for port, count in sorted(self.port_stats.items(), key=lambda x: x[1], reverse=True)[:5]:
                service = self.get_service_name(port)
                print(f"Port {port:5d} ({service:10s}) : {count:5d} packets")
            
            # Recent packets
            print("\nRECENT PACKETS (Last 10):")
            print("-" * 80)
            print(f"{'Time':10s} {'Proto':8s} {'Source':17s} {'Destination':17s} {'Length':8s}")
            print("-" * 80)
            for pkt in list(self.packets)[-10:]:
                print(f"{pkt['timestamp']:10s} {pkt['protocol']:8s} {pkt['src']:17s} {pkt['dst']:17s} {pkt['length']:8d}")
            
            print("\n" + "=" * 80)
            print("Press Ctrl+C to stop monitoring...")
            
            time.sleep(2)
    
    def get_service_name(self, port):
        """Map common ports to service names"""
        services = {
            20: 'FTP-DATA',
            21: 'FTP',
            22: 'SSH',
            23: 'TELNET',
            25: 'SMTP',
            53: 'DNS',
            80: 'HTTP',
            110: 'POP3',
            143: 'IMAP',
            443: 'HTTPS',
            445: 'SMB',
            3306: 'MySQL',
            3389: 'RDP',
            5432: 'PostgreSQL',
            8080: 'HTTP-ALT'
        }
        return services.get(port, 'Unknown')
    
    def start(self, interface=None, filter_str=None):
        """Start packet capture"""
        self.running = True
        self.start_time = time.time()
        
        # Start display thread
        display_thread = threading.Thread(target=self.display_stats, daemon=True)
        display_thread.start()
        
        print(f"Starting packet capture on interface: {interface or 'default'}")
        print("Initializing... This requires admin/root privileges!")
        
        try:
            # Start sniffing (this blocks)
            sniff(prn=self.packet_handler, iface=interface, filter=filter_str, store=False)
        except KeyboardInterrupt:
            print("\n\nStopping capture...")
            self.running = False
        except PermissionError:
            print("\n⚠️  Permission denied! Run with sudo/administrator privileges:")
            print("   Linux/Mac: sudo python3 network_monitor.py")
            print("   Windows: Run as Administrator")
    
    def export_stats(self, filename='network_stats.txt'):
        """Export statistics to file"""
        with open(filename, 'w') as f:
            f.write("Network Traffic Analysis Report\n")
            f.write("=" * 50 + "\n\n")
            f.write(f"Total packets: {len(self.packets)}\n")
            f.write(f"Duration: {time.time() - self.start_time:.2f}s\n\n")
            
            f.write("Protocol Distribution:\n")
            for proto, count in self.protocol_stats.items():
                f.write(f"  {proto}: {count}\n")
            
            f.write("\nSuspicious IPs:\n")
            for ip in self.suspicious_ips:
                f.write(f"  {ip} ({self.ip_stats[ip]} packets)\n")
        
        print(f"\n✅ Stats exported to {filename}")


def main():
    print("""
    ╔═══════════════════════════════════════╗
    ║   Real-Time Network Traffic Monitor   ║
    ╚═══════════════════════════════════════╝
    
    This tool captures and analyzes network packets.
    Requires administrative/root privileges!
    """)
    
    monitor = NetworkMonitor()
    
    # You can specify interface and BPF filter
    # Examples:
    #   monitor.start(interface='eth0')
    #   monitor.start(filter_str='tcp port 80')
    #   monitor.start(filter_str='host 192.168.1.1')
    
    try:
        monitor.start()
    finally:
        monitor.export_stats()


if __name__ == '__main__':
    main()
