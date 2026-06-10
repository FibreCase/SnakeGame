#!/usr/bin/env python3
import argparse
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'snake_game'))

from snake import SnakeGame, SOCKET_PATH
import tkinter as tk

def main():
    parser = argparse.ArgumentParser(description='贪吃蛇游戏 - 支持AI自动控制')
    parser.add_argument('--ai', action='store_true', help='启用AI自动控制')
    parser.add_argument('--ai-delay', type=float, default=0.1, help='AI控制延迟(秒)')
    parser.add_argument('--human', action='store_true', help='启用人类玩家控制')
    parser.add_argument('--headless', action='store_true', help='无头模式运行(无图形界面)')
    
    args = parser.parse_args()
    
    if args.headless:
        print("无头模式暂未实现，请使用图形界面模式")
        sys.exit(1)
    
    root = tk.Tk()
    game = SnakeGame(root)
    
    if args.ai:
        from ai_controller import AIController
        ai_controller = AIController(game, delay=args.ai_delay)
        ai_controller.start()
    
    root.mainloop()

if __name__ == "__main__":
    main()