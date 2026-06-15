#!/usr/bin/env python3
import sys
import os
import argparse

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'snake_game'))

from snake import SnakeGame
import tkinter as tk

def main():
    parser = argparse.ArgumentParser(description='贪吃蛇游戏')
    parser.add_argument('--controlled', action='store_true', help='受控模式：只有收到next_step命令时蛇才移动')
    parser.add_argument('--socket', type=str, default='/tmp/snake_game.sock', help='Unix socket路径')
    
    args = parser.parse_args()
    
    root = tk.Tk()
    game = SnakeGame(root, controlled=args.controlled, socket_path=args.socket)
    root.mainloop()

if __name__ == "__main__":
    main()