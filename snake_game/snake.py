import tkinter as tk
import random
import socket
import threading
import os
import json

SOCKET_PATH = "/tmp/snake_game.sock"

class SnakeGame:
    def __init__(self, root, controlled=False):
        self.root = root
        self.root.title("贪吃蛇游戏")
        
        self.canvas_width = 600
        self.canvas_height = 600
        self.cell_size = 20
        self.grid_width = self.canvas_width // self.cell_size
        self.grid_height = self.canvas_height // self.cell_size
        self.speed = 150
        self.controlled = controlled
        
        self.canvas = tk.Canvas(root, width=self.canvas_width, height=self.canvas_height, bg="black")
        self.canvas.pack()
        
        self.score = 0
        self.score_label = tk.Label(root, text=f"分数: {self.score}", font=("Arial", 16), fg="white", bg="black")
        self.score_label.pack(fill=tk.X)
        
        self.reset_game()
        
        self.root.bind("<Key>", self.handle_key)
        
        self.socket_server = threading.Thread(target=self.start_socket_server, daemon=False)
        self.socket_server.start()
        
        if not self.controlled:
            self.game_loop()
    
    def reset_game(self):
        self.snake = [(5, 5), (4, 5), (3, 5)]
        self.direction = "Right"
        self.food = self.generate_food()
        self.score = 0
        self.score_label.config(text=f"分数: {self.score}")
        self.game_over = False
    
    def generate_food(self):
        while True:
            x = random.randint(0, self.grid_width - 1)
            y = random.randint(0, self.grid_height - 1)
            if (x, y) not in self.snake:
                return (x, y)
    
    def draw_snake(self):
        self.canvas.delete("snake")
        snake_length = len(self.snake)
        for i, segment in enumerate(self.snake):
            ratio = i / (snake_length - 1) if snake_length > 1 else 0
            green = int(50 + ratio * 150)
            color = f"#{green:02x}{255:02x}{green:02x}"
            x, y = segment
            self.canvas.create_rectangle(
                x * self.cell_size, y * self.cell_size,
                x * self.cell_size + self.cell_size, y * self.cell_size + self.cell_size,
                fill=color, tags="snake"
            )
    
    def draw_food(self):
        self.canvas.delete("food")
        x, y = self.food
        self.canvas.create_oval(
            x * self.cell_size, y * self.cell_size,
            x * self.cell_size + self.cell_size, y * self.cell_size + self.cell_size,
            fill="red", tags="food"
        )
    
    def move_snake(self):
        head_x, head_y = self.snake[0]
        
        if self.direction == "Right":
            new_head = (head_x + 1, head_y)
        elif self.direction == "Left":
            new_head = (head_x - 1, head_y)
        elif self.direction == "Up":
            new_head = (head_x, head_y - 1)
        elif self.direction == "Down":
            new_head = (head_x, head_y + 1)
        
        if new_head[0] < 0:
            new_head = (self.grid_width - 1, new_head[1])
        elif new_head[0] >= self.grid_width:
            new_head = (0, new_head[1])
        
        if new_head[1] < 0:
            new_head = (new_head[0], self.grid_height - 1)
        elif new_head[1] >= self.grid_height:
            new_head = (new_head[0], 0)
        
        if new_head in self.snake:
            self.game_over = True
            return
        
        self.snake.insert(0, new_head)
        
        if new_head == self.food:
            self.score += 10
            self.score_label.config(text=f"分数: {self.score}")
            self.food = self.generate_food()
        else:
            self.snake.pop()
    
    def handle_key(self, event):
        key = event.keysym
        
        if key == "Right" and self.direction != "Left":
            self.direction = "Right"
        elif key == "Left" and self.direction != "Right":
            self.direction = "Left"
        elif key == "Up" and self.direction != "Down":
            self.direction = "Up"
        elif key == "Down" and self.direction != "Up":
            self.direction = "Down"
    
    def handle_command(self, command):
        try:
            request = json.loads(command)
            cmd = request.get("command", "").lower()
            is_json = True
        except json.JSONDecodeError:
            cmd = command.strip().lower()
            is_json = False
        
        response = {"success": True}
        
        if cmd == "up":
            self.direction = "Up"
            response["message"] = "Direction changed to Up"
        elif cmd == "down":
            self.direction = "Down"
            response["message"] = "Direction changed to Down"
        elif cmd == "left":
            self.direction = "Left"
            response["message"] = "Direction changed to Left"
        elif cmd == "right":
            self.direction = "Right"
            response["message"] = "Direction changed to Right"
        elif cmd == "status":
            response["data"] = {
                "score": self.score,
                "direction": self.direction,
                "game_over": self.game_over
            }
        elif cmd == "reset":
            self.reset_game()
            response["message"] = "Game reset"
        elif cmd == "full_status":
            response["data"] = {
                "score": self.score,
                "direction": self.direction,
                "game_over": self.game_over,
                "snake": self.snake,
                "food": list(self.food)
            }
        elif cmd == "snake":
            response["data"] = {"snake": self.snake}
        elif cmd == "food":
            response["data"] = {"food": list(self.food)}
        elif cmd == "step":
            if not self.game_over:
                self.move_snake()
                self.draw_snake()
                self.draw_food()
                response["message"] = "Step executed"
                response["data"] = {
                    "score": self.score,
                    "direction": self.direction,
                    "game_over": self.game_over,
                    "snake": self.snake,
                    "food": list(self.food)
                }
            else:
                response["success"] = False
                response["error"] = "Game over"
        elif cmd == "next_step":
            if self.controlled:
                if not self.game_over:
                    self.move_snake()
                    self.draw_snake()
                    self.draw_food()
                    response["message"] = "Next step executed"
                    response["data"] = {
                        "score": self.score,
                        "direction": self.direction,
                        "game_over": self.game_over,
                        "snake": self.snake,
                        "food": list(self.food)
                    }
                else:
                    response["success"] = False
                    response["error"] = "Game over"
            else:
                response["success"] = False
                response["error"] = "Not in controlled mode"
        elif cmd == "info":
            response["data"] = {
                "canvas_width": self.canvas_width,
                "canvas_height": self.canvas_height,
                "cell_size": self.cell_size
            }
        else:
            response["success"] = False
            response["error"] = "Unknown command"
        
        return json.dumps(response)
    
    def start_socket_server(self):
        if os.path.exists(SOCKET_PATH):
            os.remove(SOCKET_PATH)
        
        server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind(SOCKET_PATH)
        server.listen(5)
        
        print(f"Unix socket server started at {SOCKET_PATH}")
        
        while True:
            try:
                conn, addr = server.accept()
                try:
                    data = conn.recv(1024).decode('utf-8')
                    if data:
                        response = self.handle_command(data)
                        conn.sendall(response.encode('utf-8'))
                finally:
                    conn.close()
            except Exception as e:
                print(f"Socket error: {e}")
                break
    
    def game_loop(self):
        if not self.game_over:
            self.move_snake()
            self.draw_snake()
            self.draw_food()
            self.root.after(self.speed, self.game_loop)
        else:
            self.canvas.delete(tk.ALL)
            self.canvas.create_text(
                self.canvas_width // 2, self.canvas_height // 2 - 30,
                text=f"游戏结束!", fill="red", font=("Arial", 32)
            )
            self.canvas.create_text(
                self.canvas_width // 2, self.canvas_height // 2 + 20,
                text=f"最终分数: {self.score}", fill="white", font=("Arial", 24)
            )
            self.canvas.create_text(
                self.canvas_width // 2, self.canvas_height // 2 + 70,
                text="按空格键重新开始", fill="gray", font=("Arial", 16)
            )
            self.root.bind("<space>", lambda e: self.reset_game())

if __name__ == "__main__":
    root = tk.Tk()
    game = SnakeGame(root)
    root.mainloop()