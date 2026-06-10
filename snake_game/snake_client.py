#!/usr/bin/env python3
import socket
import sys

SOCKET_PATH = "/tmp/snake_game.sock"

def send_command(command):
    try:
        client = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        client.connect(SOCKET_PATH)
        client.sendall(command.encode('utf-8'))
        response = client.recv(1024).decode('utf-8')
        client.close()
        return response.strip()
    except Exception as e:
        return f"Error: {e}"

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python snake_client.py <command>")
        print("Commands:")
        print("  up, down, left, right - Control snake direction")
        print("  status - Get basic game status")
        print("  full_status - Get complete game status (snake positions, food position)")
        print("  snake - Get snake body positions")
        print("  food - Get food position")
        print("  step - Execute one game step")
        print("  info - Get game canvas info")
        print("  reset - Reset game")
        sys.exit(1)
    
    command = sys.argv[1]
    response = send_command(command)
    print(response)