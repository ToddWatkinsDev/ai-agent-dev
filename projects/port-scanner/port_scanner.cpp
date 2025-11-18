#include <iostream>
#include <string>
#include <vector>
#include <chrono>
#include <thread>
#include <algorithm>

#ifdef _WIN32
    #include <winsock2.h>
    #include <ws2tcpip.h>
    #pragma comment(lib, "ws2_32.lib")
#else
    #include <sys/socket.h>
    #include <arpa/inet.h>
    #include <netinet/in.h>
    #include <unistd.h>
    #include <netdb.h>
#endif

using namespace std;

class PortScanner {
private:
    string targetHost;
    int startPort;
    int endPort;
    int timeout;
    vector<int> openPorts;
    
    // Common port service mapping
    string getServiceName(int port) {
        switch(port) {
            case 20: return "FTP-Data";
            case 21: return "FTP";
            case 22: return "SSH";
            case 23: return "Telnet";
            case 25: return "SMTP";
            case 53: return "DNS";
            case 80: return "HTTP";
            case 110: return "POP3";
            case 143: return "IMAP";
            case 443: return "HTTPS";
            case 445: return "SMB";
            case 3306: return "MySQL";
            case 3389: return "RDP";
            case 5432: return "PostgreSQL";
            case 8080: return "HTTP-Proxy";
            default: return "Unknown";
        }
    }
    
public:
    // Constructor
    PortScanner(string host, int start, int end, int timeoutMs = 1000) 
        : targetHost(host), startPort(start), endPort(end), timeout(timeoutMs) {
        #ifdef _WIN32
            WSADATA wsaData;
            if (WSAStartup(MAKEWORD(2, 2), &wsaData) != 0) {
                cerr << "WSAStartup failed" << endl;
            }
        #endif
    }
    
    // Destructor
    ~PortScanner() {
        #ifdef _WIN32
            WSACleanup();
        #endif
    }
    
    // Check if a single port is open
    bool isPortOpen(int port) {
        int sock;
        struct sockaddr_in server;
        struct hostent *host;
        
        // Create socket
        sock = socket(AF_INET, SOCK_STREAM, 0);
        if (sock == -1) {
            return false;
        }
        
        // Set timeout
        #ifdef _WIN32
            DWORD timeoutVal = timeout;
            setsockopt(sock, SOL_SOCKET, SO_RCVTIMEO, (char*)&timeoutVal, sizeof(timeoutVal));
            setsockopt(sock, SOL_SOCKET, SO_SNDTIMEO, (char*)&timeoutVal, sizeof(timeoutVal));
        #else
            struct timeval tv;
            tv.tv_sec = timeout / 1000;
            tv.tv_usec = (timeout % 1000) * 1000;
            setsockopt(sock, SOL_SOCKET, SO_RCVTIMEO, &tv, sizeof(tv));
            setsockopt(sock, SOL_SOCKET, SO_SNDTIMEO, &tv, sizeof(tv));
        #endif
        
        // Resolve hostname
        host = gethostbyname(targetHost.c_str());
        if (host == NULL) {
            #ifdef _WIN32
                closesocket(sock);
            #else
                close(sock);
            #endif
            return false;
        }
        
        // Setup server structure
        server.sin_family = AF_INET;
        server.sin_port = htons(port);
        server.sin_addr.s_addr = *(long*)host->h_addr;
        
        // Attempt connection
        bool result = (connect(sock, (struct sockaddr*)&server, sizeof(server)) == 0);
        
        // Close socket
        #ifdef _WIN32
            closesocket(sock);
        #else
            close(sock);
        #endif
        
        return result;
    }
    
    // Perform the scan
    void scan() {
        cout << "\n========================================" << endl;
        cout << "  Network Port Scanner" << endl;
        cout << "  Written by AI Agent (Perplexity)" << endl;
        cout << "========================================" << endl;
        cout << "\nTarget: " << targetHost << endl;
        cout << "Port Range: " << startPort << "-" << endPort << endl;
        cout << "Timeout: " << timeout << "ms" << endl;
        cout << "\nScanning..." << endl;
        cout << "========================================\n" << endl;
        
        auto startTime = chrono::high_resolution_clock::now();
        int totalPorts = endPort - startPort + 1;
        int scanned = 0;
        
        for (int port = startPort; port <= endPort; port++) {
            scanned++;
            
            // Progress indicator
            if (scanned % 100 == 0 || scanned == totalPorts) {
                cout << "Progress: " << scanned << "/" << totalPorts 
                     << " ports scanned\r" << flush;
            }
            
            if (isPortOpen(port)) {
                openPorts.push_back(port);
                cout << "\n[+] Port " << port << " is OPEN"
                     << " (" << getServiceName(port) << ")" << endl;
            }
        }
        
        auto endTime = chrono::high_resolution_clock::now();
        auto duration = chrono::duration_cast<chrono::seconds>(endTime - startTime);
        
        displayResults(duration.count());
    }
    
    // Display scan results
    void displayResults(long scanTime) {
        cout << "\n\n========================================" << endl;
        cout << "  Scan Results" << endl;
        cout << "========================================" << endl;
        cout << "\nTarget Host: " << targetHost << endl;
        cout << "Scan Duration: " << scanTime << " seconds" << endl;
        cout << "Total Ports Scanned: " << (endPort - startPort + 1) << endl;
        cout << "Open Ports Found: " << openPorts.size() << endl;
        
        if (!openPorts.empty()) {
            cout << "\nOpen Ports:\n" << endl;
            cout << "Port\tService" << endl;
            cout << "----\t-------" << endl;
            for (int port : openPorts) {
                cout << port << "\t" << getServiceName(port) << endl;
            }
        } else {
            cout << "\nNo open ports found in the specified range." << endl;
        }
        
        cout << "\n========================================" << endl;
        cout << "\n[!] Warning: Use this tool responsibly and only" << endl;
        cout << "    on systems you own or have permission to test." << endl;
        cout << "========================================\n" << endl;
    }
};

int main() {
    string host;
    int startPort, endPort;
    
    cout << "\n**** Network Port Scanner ****" << endl;
    cout << "Educational tool for network reconnaissance" << endl;
    cout << "Written by an AI agent for security research\n" << endl;
    
    cout << "Enter target host (IP or hostname): ";
    cin >> host;
    
    cout << "Enter start port (e.g., 1): ";
    cin >> startPort;
    
    cout << "Enter end port (e.g., 1024): ";
    cin >> endPort;
    
    // Validate input
    if (startPort < 1 || endPort > 65535 || startPort > endPort) {
        cerr << "\nError: Invalid port range!" << endl;
        cerr << "Ports must be between 1-65535 and start <= end" << endl;
        return 1;
    }
    
    // Create scanner and perform scan
    PortScanner scanner(host, startPort, endPort, 1000);
    scanner.scan();
    
    return 0;
}
