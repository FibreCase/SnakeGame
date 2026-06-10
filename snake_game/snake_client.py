#!/usr/bin/env python3
import socket
import sys
import json

SOCKET_PATH = "/tmp/snake_game.sock"

def send_command(command, use_json=True):
    try:
        client = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        client.connect(SOCKET_PATH)
        
        if use_json:
            request = json.dumps({"command": command})
        else:
            request = command
        
        client.sendall(request.encode('utf-8'))
        response = client.recv(4096).decode('utf-8')
        client.close()
        
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            return response
    except Exception as e:
        return {"success": False, "error": str(e)}

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python snake_client.py <command>")
        print("Commands:")
        print("  up, down, left, right - Control snake direction")
        print("  status - Get basic game status")
        print("  full_status - Get complete game status")
        print("  snake - Get snake body positions")
        print("  food - Get food position")
        print("  step - Execute one game step")
        print("  info - Get game canvas info")
        print("  reset - Reset game")
        sys.exit(1)
    
    command = sys.argv[1]
    response = send_command(command)
    
    if isinstance(response, dict):
        print(json.dumps(response, indent=2))
    else:
        print(response)