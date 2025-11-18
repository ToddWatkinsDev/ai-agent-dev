#!/usr/bin/env python3
import socket
import subprocess
import sys

def get_network_stats():
    """Get network traffic statistics"""
    try:
        if sys.platform == 'win32':
            result = subprocess.run(['netstat', '-s'], capture_output=True, text=True)
        else:
            result = subprocess.run(['netstat', '-s'], capture_output=True, text=True)
        return result.stdout
    except Exception as e:
        return f"Error: {str(e)}"

def display_network_info():
    """Display network information"""
    print("="*50)
    print("Network Monitor - AI Agent Written")
    print("="*50)
    print(get_network_stats())

if __name__ == "__main__":
    display_network_info()
