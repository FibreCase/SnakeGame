import threading
import time
import random

class AIController:
    def __init__(self, game, delay=0.1):
        self.game = game
        self.delay = delay
        self.running = False
        self.thread = None
    
    def start(self):
        self.running = True
        self.thread = threading.Thread(target=self.run, daemon=True)
        self.thread.start()
    
    def stop(self):
        self.running = False
        if self.thread:
            self.thread.join()
    
    def get_state(self):
        return {
            'snake': self.game.snake.copy(),
            'food': self.game.food,
            'direction': self.game.direction,
            'game_over': self.game.game_over,
            'canvas_width': self.game.canvas_width,
            'canvas_height': self.game.canvas_height,
            'cell_size': self.game.cell_size
        }
    
    def calculate_distance(self, pos1, pos2):
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])
    
    def get_valid_directions(self):
        current_dir = self.game.direction
        opposites = {
            'Up': 'Down',
            'Down': 'Up',
            'Left': 'Right',
            'Right': 'Left'
        }
        all_dirs = ['Up', 'Down', 'Left', 'Right']
        return [d for d in all_dirs if d != opposites[current_dir]]
    
    def predict_position(self, direction):
        head_x, head_y = self.game.snake[0]
        cell_size = self.game.cell_size
        
        if direction == 'Right':
            new_x = head_x + cell_size
            new_y = head_y
        elif direction == 'Left':
            new_x = head_x - cell_size
            new_y = head_y
        elif direction == 'Up':
            new_x = head_x
            new_y = head_y - cell_size
        elif direction == 'Down':
            new_x = head_x
            new_y = head_y + cell_size
        
        new_x = (new_x + self.game.canvas_width) % self.game.canvas_width
        new_y = (new_y + self.game.canvas_height) % self.game.canvas_height
        
        return (new_x, new_y)
    
    def is_safe(self, position):
        if position in self.game.snake[1:]:
            return False
        return True
    
    def choose_direction(self):
        if self.game.game_over:
            return None
        
        state = self.get_state()
        head = state['snake'][0]
        food = state['food']
        valid_dirs = self.get_valid_directions()
        
        if not valid_dirs:
            return None
        
        safe_dirs = []
        for d in valid_dirs:
            pos = self.predict_position(d)
            if self.is_safe(pos):
                safe_dirs.append(d)
        
        if not safe_dirs:
            safe_dirs = valid_dirs
        
        best_dir = None
        min_distance = float('inf')
        
        for d in safe_dirs:
            new_head = self.predict_position(d)
            distance = self.calculate_distance(new_head, food)
            if distance < min_distance:
                min_distance = distance
                best_dir = d
        
        if best_dir is None and safe_dirs:
            best_dir = random.choice(safe_dirs)
        
        return best_dir
    
    def run(self):
        while self.running:
            if self.game.game_over:
                time.sleep(0.5)
                self.game.reset_game()
                continue
            
            direction = self.choose_direction()
            if direction:
                self.game.direction = direction
            
            time.sleep(self.delay)