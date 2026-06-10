# 贪吃蛇游戏 (Snake Game)

> 本项目用于学习 Vibe Code，使用 Trae + Qwen3-Coder:30B 开发。

一个基于 Python 的贪吃蛇小游戏，支持人类玩家和Unix socket远程控制。

## 功能特性

- 🎮 **人类玩家模式**：使用键盘方向键控制蛇的移动
- 🔌 **Unix Socket接口**：支持外部程序通过socket控制游戏
- 🎨 **视觉效果**：蛇身显示不同深浅的绿色渐变
- 🔄 **穿墙效果**：蛇撞墙后从另一侧出现
- 📊 **分数系统**：吃到食物获得10分

## 项目结构

```
trae-test/
├── main.py                    # 主入口文件
├── pyproject.toml             # uv配置
├── uv.lock                    # 依赖锁文件
└── snake_game/                # 游戏模块
    ├── snake.py               # 游戏核心逻辑
    ├── snake_client.py        # Socket客户端工具
    └── SOCKET_API.md          # Socket接口文档
```

## 快速开始

### 1. 安装依赖

```bash
# 使用uv初始化环境（已配置）
uv sync
```

### 2. 运行游戏

#### 人类玩家模式

```bash
uv run python main.py
```

使用键盘方向键（↑↓←→）控制蛇的移动。

## 游戏玩法

- 🐍 **目标**：控制蛇吃到红色食物，避免撞到自己
- ⬆️⬇️⬅️➡️ **控制**：使用键盘方向键改变蛇的移动方向
- 🔄 **穿墙**：蛇会从墙壁的另一侧出现
- 🔄 **重置**：游戏结束后按空格键重新开始

## Unix Socket 接口

游戏支持通过Unix socket进行远程控制。

### 连接地址

```
/tmp/snake_game.sock
```

### 支持的命令

| 命令 | 说明 | 示例 |
|------|------|------|
| `up` | 向上移动 | `echo "up" \| nc -U /tmp/snake_game.sock` |
| `down` | 向下移动 | `echo "down" \| nc -U /tmp/snake_game.sock` |
| `left` | 向左移动 | `echo "left" \| nc -U /tmp/snake_game.sock` |
| `right` | 向右移动 | `echo "right" \| nc -U /tmp/snake_game.sock` |
| `status` | 获取基本状态 | `echo "status" \| nc -U /tmp/snake_game.sock` |
| `full_status` | 获取完整状态（蛇身位置、食物位置） | `echo "full_status" \| nc -U /tmp/snake_game.sock` |
| `snake` | 获取蛇身体所有位置 | `echo "snake" \| nc -U /tmp/snake_game.sock` |
| `food` | 获取食物位置 | `echo "food" \| nc -U /tmp/snake_game.sock` |
| `step` | 执行单步运行 | `echo "step" \| nc -U /tmp/snake_game.sock` |
| `info` | 获取画布信息 | `echo "info" \| nc -U /tmp/snake_game.sock` |
| `reset` | 重置游戏 | `echo "reset" \| nc -U /tmp/snake_game.sock` |

### 使用Python客户端

```bash
uv run python snake_game/snake_client.py status
uv run python snake_game/snake_client.py up
uv run python snake_game/snake_client.py reset
```

### 使用示例

```python
import socket
import json

def send_command(command):
    client = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    client.connect('/tmp/snake_game.sock')
    
    # 发送JSON格式请求
    request = json.dumps({"command": command})
    client.sendall(request.encode('utf-8'))
    
    response = client.recv(4096).decode('utf-8')
    client.close()
    
    # 返回JSON解析后的字典
    return json.loads(response)

# 获取状态
result = send_command("full_status")
print(result)
# 输出: {"success": true, "data": {"score": 0, "direction": "Right", "game_over": false, "snake": [[100,100],...], "food": [200,200]}}

# 控制方向
send_command("up")

# 执行单步
result = send_command("step")
print(result["data"]["snake"])
```

### JSON请求格式

```json
{"command": "full_status"}
```

### JSON响应格式

成功响应：
```json
{
  "success": true,
  "message": "Step executed",
  "data": {
    "score": 0,
    "direction": "Right",
    "game_over": false,
    "snake": [[280, 100], [260, 100], [240, 100]],
    "food": [20, 400]
  }
}
```

失败响应：
```json
{
  "success": false,
  "error": "Unknown command"
}
```

## 技术栈

- Python 3.13
- Tkinter（图形界面）
- Unix Socket（远程控制）
- uv（包管理器）

## 开发

### 添加新功能

1. 修改 `snake_game/snake.py` 添加游戏逻辑
2. 更新 `snake_game/SOCKET_API.md` 文档

### 测试

```bash
# 运行游戏测试
uv run python main.py

# 测试socket接口
uv run python snake_game/snake_client.py status
```

## 许可证

MIT License