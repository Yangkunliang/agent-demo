# AI智能助理启动指南

本指南将帮助您在电脑开机后，正确启动Dify服务器和haokang-agent应用程序。

## 一、系统环境

- **操作系统**：macOS
- **终端**：Terminal或iTerm2
- **Docker**：用于启动Dify服务器

## 二、启动顺序

建议按照以下顺序启动应用程序：

1. 启动Docker
2. 启动Dify服务器
3. 启动haokang-agent后端服务
4. 启动haokang-agent前端HTTP服务器

## 三、详细启动步骤

### 1. 启动Docker

Docker是运行Dify服务器的必要条件。

**操作步骤**：
1. 点击Dock栏中的Docker图标，或从Launchpad中启动Docker
2. 等待Docker完全启动（Docker图标变为绿色）

### 2. 启动Dify服务器

Dify服务器提供了大模型集成和向量检索功能。

**操作步骤**：
1. 打开终端（Terminal）
2. 进入Dify项目目录：
   ```bash
   cd /Users/yangkl/trae-project/dify-main/docker
   ```
3. 启动Dify服务器：
   ```bash
   docker-compose up -d
   ```
4. 等待约30秒，确保Dify服务器完全启动，可以通过 
   ``` bash
   http://localhost:3000/ 
   ```
访问Dify控制台

5. 验证Dify服务器是否正常运行：
   ```bash
   curl -I http://localhost:5001
   ```
   如果返回`HTTP/1.1 200 OK`，则表示Dify服务器已成功启动

### 3. 启动haokang-agent后端服务

haokang-agent后端服务提供了聊天接口。

**操作步骤**：
1. 打开新的终端窗口
2. 进入haokang-agent项目目录：
   ```bash
   cd /Users/yangkl/trae-project/dify-demo/haokang-agent
   ```
3. 启动后端服务：
   ```bash
   uvicorn src.app:app --host 127.0.0.1 --port 8001 --reload
   ```
4. 等待服务启动，当看到类似`Uvicorn running on http://127.0.0.1:8001`的输出时，表示后端服务已成功启动

### 4. 启动haokang-agent前端HTTP服务器

前端HTTP服务器用于提供静态文件访问。

**操作步骤**：
1. 打开新的终端窗口
2. 进入前端项目目录：
   ```bash
   cd /Users/yangkl/trae-project/dify-demo
   ```
3. 启动HTTP服务器：
   ```bash
   python3 -m http.server 8080 --directory /Users/yangkl/trae-project/dify-demo/haokang-agent/frontend
   ```
4. 当看到类似`Serving HTTP on 0.0.0.0 port 8080 (http://0.0.0.0:8080/) ...`的输出时，表示前端服务器已成功启动

## 四、访问应用程序

所有服务启动成功后，您可以通过以下方式访问应用程序：

- **前端界面**：在浏览器中输入 `http://localhost:8080/chat.html`
- **后端API**：`http://localhost:8001/v1/chat/completions`
- **Dify控制台**：`http://localhost:5001`

## 五、环境变量配置

如果您需要配置环境变量，可以在启动服务前设置，或修改项目中的`.env`文件。

### 主要环境变量

1. **Dify相关**：
   - `DIFY_API_KEY`：Dify API密钥
   - `DIFY_APP_ID`：Dify应用ID
   - `DIFY_API_URL`：Dify API地址（默认：http://localhost:5001）

2. **haokang-agent相关**：
   - `MODEL`：使用的模型名称（默认：haokang-agent）
   - `PORT`：后端服务端口（默认：8001）

## 六、关闭服务

### 1. 关闭haokang-agent前端HTTP服务器

在前端HTTP服务器所在的终端窗口中，按下 `Ctrl + C`

### 2. 关闭haokang-agent后端服务

在后端服务所在的终端窗口中，按下 `Ctrl + C`

### 3. 关闭Dify服务器

在Dify项目目录中执行：
```bash
docker-compose down
```

### 4. 关闭Docker

点击Docker图标，选择"Quit Docker Desktop"

## 七、故障排除

### 1. Dify服务器启动失败

- **问题**：Docker未完全启动
  **解决方法**：等待Docker完全启动后再尝试启动Dify服务器

- **问题**：端口被占用
  **解决方法**：检查端口5001是否被占用，使用`lsof -i :5001`查看，并关闭占用该端口的进程

### 2. haokang-agent后端服务启动失败

- **问题**：缺少依赖包
  **解决方法**：安装所需的依赖包
  ```bash
  pip install -r requirements.txt
  ```

- **问题**：环境变量未配置
  **解决方法**：检查并配置必要的环境变量

### 3. 前端无法访问

- **问题**：前端服务器未启动
  **解决方法**：确保前端HTTP服务器正在运行

- **问题**：端口被占用
  **解决方法**：检查端口8080是否被占用，使用`lsof -i :8080`查看，并关闭占用该端口的进程

### 4. 聊天功能无法使用

- **问题**：Dify服务器未启动
  **解决方法**：确保Dify服务器正在运行

- **问题**：API密钥或应用ID错误
  **解决方法**：检查并修正环境变量中的DIFY_API_KEY和DIFY_APP_ID

## 八、快捷启动脚本

为了方便启动，您可以创建一个快捷启动脚本：

### 1. 创建启动脚本

```bash
# 打开终端
cd /Users/yangkl/trae-project/dify-demo/haokang-agent

# 创建启动脚本
touch start_all.sh
chmod +x start_all.sh
```

### 2. 编辑脚本内容

```bash
#!/bin/bash

echo "Starting Dify server..."
curl -I http://localhost:5001 > /dev/null 2>&1
if [ $? -ne 0 ]; then
    echo "Dify server is not running. Please start Docker and Dify server first."
    exit 1
fi

echo "Starting haokang-agent backend service..."
cd /Users/yangkl/trae-project/dify-demo/haokang-agent
python3 -m uvicorn src.app:app --host 127.0.0.1 --port 8001 --reload &
BACKEND_PID=$!

echo "Starting haokang-agent frontend HTTP server..."
cd /Users/yangkl/trae-project/dify-demo
python3 -m http.server 8080 --directory /Users/yangkl/trae-project/dify-demo/haokang-agent/frontend &
FRONTEND_PID=$!

echo "All services started successfully!"
echo "Backend PID: $BACKEND_PID"
echo "Frontend PID: $FRONTEND_PID"
echo "You can access the application at http://localhost:8080/chat.html"
```

### 3. 使用脚本启动

```bash
./start_all.sh
```

## 九、更新记录

- **2026-01-03**：初始版本

## 十、联系方式

如有问题，请联系技术支持。

---

祝您使用愉快！