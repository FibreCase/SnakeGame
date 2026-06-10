# 贪吃蛇游戏 Unix Socket 控制接口

## 概述
本游戏提供Unix socket接口，允许其他程序通过socket命令控制游戏。

## Socket 配置
- **Socket 路径**: `/tmp/snake_game.sock`
- **协议**: Unix Domain Socket (AF_UNIX)
- **类型**: Stream (SOCK_STREAM)

## 支持的命令

### 1. 方向控制
```
up     - 向上移动
down   - 向下移动
left   - 向左移动
right  - 向右移动
```

### 2. 游戏状态
```
status - 获取当前游戏状态
        返回格式: score=分数,direction=方向,game_over=是否结束
```

### 3. 游戏控制
```
reset  - 重置游戏
```

## 使用方法

### 方法1: 使用 netcat (nc)
```bash
echo "status" | nc -U /tmp/snake_game.sock
echo "up" | nc -U /tmp/snake_game.sock
echo "down" | nc -U /tmp/snake_game.sock
```

### 方法2: 使用 Python 客户端
```bash
# 查看帮助
python snake_client.py

# 获取状态
python snake_client.py status

# 控制方向
python snake_client.py up
python snake_client.py down
python snake_client.py left
python snake_client.py right

# 重置游戏
python snake_client.py reset
```

### 方法3: 在 Python 代码中使用
```python
import socket

SOCKET_PATH = "/tmp/snake_game.sock"

def send_command(command):
    client = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    client.connect(SOCKET_PATH)
    client.sendall(command.encode('utf-8'))
    response = client.recv(1024).decode('utf-8')
    client.close()
    return response.strip()

# 使用示例
print(send_command("status"))
send_command("up")
send_command("right")
send_command("reset")
```

## 示例程序

### 自动化控制示例
```python
import socket
import time

def auto_play():
    client = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    client.connect("/tmp/snake_game.sock")
    
    commands = ["right", "down", "left", "up"]
    for cmd in commands:
        client.sendall(cmd.encode('utf-8'))
        response = client.recv(1024).decode('utf-8')
        print(f"Sent: {cmd}, Response: {response}")
        time.sleep(0.5)
    
    client.close()

if __name__ == "__main__":
    auto_play()
```

### 监控游戏状态
```python
import socket
import time

def monitor_game():
    client = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    client.connect("/tmp/snake_game.sock")
    
    while True:
        client.sendall(b"status")
        response = client.recv(1024).decode('utf-8')
        print(f"Game status: {response}")
        time.sleep(1)
    
    client.close()

if __name__ == "__main__":
    monitor_game()
```

## 注意事项

1. **游戏窗口**: 确保游戏窗口保持打开状态，关闭窗口会终止socket服务器
2. **并发连接**: socket服务器支持多个并发连接
3. **命令格式**: 命令不区分大小写，但建议使用小写
4. **错误处理**: 如果连接失败，请检查游戏是否正在运行

## 故障排除

### Socket 文件不存在
```bash
# 检查游戏是否在运行
ps aux | grep snake.py

# 检查socket文件
ls -la /tmp/snake_game.sock
```

### 连接被拒绝
```bash
# 重启游戏
pkill -f "snake.py"
uv run python snake.py
```

## 技术细节

- 使用Python的`threading`模块在独立线程中运行socket服务器
- socket服务器是守护线程，在游戏关闭时自动终止
- 每个连接处理完成后立即关闭
- 命令响应是同步的，客户端会等待服务器响应
