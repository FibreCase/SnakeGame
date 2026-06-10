# 贪吃蛇游戏 (Snake Game)

一个基于 Python 的贪吃蛇小游戏，支持人类玩家、AI自动控制和Unix socket远程控制。

## 功能特性

- 🎮 **人类玩家模式**：使用键盘方向键控制蛇的移动
- 🤖 **AI自动控制**：内置AI控制器，自动寻找最短路径吃食物
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
    ├── ai_controller.py       # AI自动控制器
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

#### AI自动控制模式

```bash
# 默认AI速度
uv run python main.py --ai

# 自定义AI控制延迟（秒）
uv run python main.py --ai --ai-delay 0.15
```

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
| `status` | 获取游戏状态 | `echo "status" \| nc -U /tmp/snake_game.sock` |
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

def send_command(command):
    client = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    client.connect('/tmp/snake_game.sock')
    client.sendall(command.encode('utf-8'))
    response = client.recv(1024).decode('utf-8')
    client.close()
    return response

print(send_command("status"))  # 输出: score=0,direction=Right,game_over=False
send_command("up")             # 控制蛇向上移动
```

## AI控制器

AI控制器使用曼哈顿距离算法寻找最短路径：

1. **状态获取**：获取蛇的位置、食物位置和游戏状态
2. **安全检测**：排除会导致碰撞的方向
3. **路径选择**：选择距离食物最近的安全方向
4. **自动重置**：游戏结束后自动重新开始

## 技术栈

- Python 3.13
- Tkinter（图形界面）
- Unix Socket（远程控制）
- uv（包管理器）

## 开发

### 添加新功能

1. 修改 `snake_game/snake.py` 添加游戏逻辑
2. 修改 `snake_game/ai_controller.py` 添加AI策略
3. 更新 `snake_game/SOCKET_API.md` 文档

### 测试

```bash
# 运行游戏测试
uv run python main.py --ai

# 测试socket接口
uv run python snake_game/snake_client.py status
```

## 许可证

MIT License

## 作者

FibreCase <fibrecase@163.com>