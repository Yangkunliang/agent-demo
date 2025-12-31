# 智能体本地部署方案

## 1. 环境准备

### 1.1 系统要求
- **操作系统**：Ubuntu 22.04+ / Windows 10/11 (WSL2) / macOS
- **硬件配置**：至少4核CPU、16GB内存、50GB磁盘空间

### 1.2 安装Docker和Docker Compose

#### Ubuntu/Debian
```bash
# 更新包列表
sudo apt update

# 安装必要的依赖
sudo apt install -y apt-transport-https ca-certificates curl software-properties-common

# 添加Docker官方GPG密钥
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

# 添加Docker仓库
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# 安装Docker
sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin

# 验证Docker安装
sudo docker --version
sudo docker compose version

# 将当前用户添加到docker组（可选，避免每次使用sudo）
sudo usermod -aG docker $USER
newgrp docker
```

#### macOS
1. 访问 [Docker官网](https://www.docker.com/) 下载Docker Desktop for Mac
2. 双击安装包，按照提示完成安装
3. 启动Docker Desktop
4. 打开终端，验证安装：
   ```bash
   docker --version
   docker compose version
   ```

#### Windows (WSL2)
1. 启用WSL2功能
2. 安装Ubuntu子系统
3. 访问 [Docker官网](https://www.docker.com/) 下载Docker Desktop for Windows
4. 安装并配置Docker Desktop，启用WSL2集成
5. 在Ubuntu终端中验证安装：
   ```bash
   docker --version
   docker compose version
   ```

## 2. Dify平台部署

### 2.1 克隆Dify仓库
```bash
# 创建工作目录
mkdir -p /opt/dify
sudo chmod -R 777 /opt/dify

# 克隆Dify源码
cd /opt/dify
git clone https://github.com/langgenius/dify.git
```

### 2.2 配置环境变量
```bash
# 进入Dify目录
cd /opt/dify

# 复制环境变量模板
cp .env.example .env

# 编辑环境变量（可选，根据需要修改）
vi .env
```

### 2.3 启动Dify服务
```bash
# 启动所有服务（包括中间件）
docker compose up -d

# 查看服务状态
docker compose ps
```

### 2.4 初始化Dify
```bash
# 等待服务启动完成（约30秒）
sleep 30

# 执行初始化命令
docker compose exec api python manage.py init
```

### 2.5 访问Dify平台
- 打开浏览器，访问 `http://localhost:3000`
- 使用初始化时设置的用户名和密码登录

## 3. 中间件配置（可选，如需自定义）

### 3.1 查看默认中间件
Dify默认使用Docker Compose启动以下中间件：
- PostgreSQL (数据库)
- Redis (缓存)
- Elasticsearch (向量搜索)
- MinIO (对象存储)

### 3.2 自定义中间件配置
如需使用外部中间件，可修改 `.env` 文件：

```bash
# 数据库配置
DB_HOST=your-postgres-host
DB_PORT=5432
DB_USER=your-postgres-user
DB_PASSWORD=your-postgres-password
DB_NAME=dify

# Redis配置
REDIS_HOST=your-redis-host
REDIS_PORT=6379
REDIS_PASSWORD=your-redis-password

# Elasticsearch配置
ELASTICSEARCH_HOST=your-es-host
ELASTICSEARCH_PORT=9200
ELASTICSEARCH_USERNAME=your-es-username
ELASTICSEARCH_PASSWORD=your-es-password
```

## 4. 智能体配置导入

### 4.1 登录Dify平台
1. 打开浏览器，访问 `http://localhost:3000`
2. 使用用户名和密码登录

### 4.2 创建Agent
1. 点击左侧菜单栏的 "Agents"
2. 点击 "创建Agent"
3. 选择 "基于配置文件创建"
4. 上传我们的 `agent_config.yml` 文件
5. 点击 "下一步"

### 4.3 配置环境变量
在Agent配置页面，设置以下环境变量：

```bash
HAOKANG_API_BASE_URL=https://api.haokang.com  # API基础URL
HAOKANG_API_KEY=your-api-key  # API密钥
OPENAI_API_KEY=your-openai-key  # OpenAI API密钥
```

### 4.4 测试Agent
1. 点击 "测试" 按钮
2. 输入测试消息，验证Agent功能
   - "上次服务的笔记是什么？"
   - "我有哪些订单？"
   - "我想修改订单order_123的时间为2023-11-02 14:00"

### 4.5 发布Agent
1. 测试通过后，点击 "发布"
2. 选择发布环境（开发/生产）
3. 点击 "确认发布"

## 5. 集成到系统

### 5.1 获取Agent API密钥
1. 在Dify平台，进入Agent详情页面
2. 点击 "API密钥"
3. 点击 "生成新密钥"
4. 复制生成的API密钥

### 5.2 配置后端
在后端服务中，配置Dify Agent的API地址和密钥：

```bash
# Dify Agent配置
DIFY_AGENT_URL=http://localhost:3000
DIFY_AGENT_API_KEY=your-agent-api-key
```

### 5.3 开发集成代码
在后端中，添加调用Dify Agent的代码：

```python
import requests
import json

def call_dify_agent(user_id, user_input):
    """调用Dify Agent获取响应"""
    url = f"{DIFY_AGENT_URL}/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {DIFY_AGENT_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "haokang-agent",  # Agent名称
        "messages": [
            {
                "role": "user",
                "content": user_input
            }
        ],
        "user": user_id
    }
    
    response = requests.post(url, headers=headers, json=data)
    return response.json()
```

## 6. 监控与维护

### 6.1 查看日志
```bash
# 查看所有服务日志
docker compose logs

# 查看特定服务日志
docker compose logs api  # 查看API服务日志
docker compose logs web  # 查看前端服务日志
```

### 6.2 停止和重启服务
```bash
# 停止所有服务
docker compose down

# 重启所有服务
docker compose restart
```

### 6.3 更新Dify
```bash
# 进入Dify目录
cd /opt/dify

# 拉取最新代码
git pull

# 停止并更新服务
docker compose down
docker compose pull
docker compose up -d
```

## 7. 常见问题排查

### 7.1 服务启动失败
```bash
# 查看详细日志
docker compose logs -f
```

### 7.2 无法访问Dify平台
- 检查服务是否正常运行：`docker compose ps`
- 检查端口是否被占用：`netstat -tlnp | grep 3000`
- 检查防火墙设置

### 7.3 数据库连接失败
- 检查环境变量配置
- 检查PostgreSQL服务状态：`docker compose logs postgres`

### 7.4 Agent响应缓慢
- 检查LLM API密钥是否正确
- 检查网络连接
- 调整LLM模型参数（降低temperature，减少max_tokens）

## 8. 性能优化建议

1. **增加资源分配**：根据实际负载调整Docker容器的CPU和内存限制
2. **优化数据库**：为PostgreSQL添加索引，定期清理无用数据
3. **使用Redis集群**：在生产环境中使用Redis集群提高缓存性能
4. **优化LLM调用**：
   - 减少每次调用的token数量
   - 使用适当的temperature值
   - 考虑使用本地部署的LLM模型
5. **启用CDN**：为静态资源启用CDN加速

## 9. 安全建议

1. **设置强密码**：为Dify管理员账户设置强密码
2. **启用HTTPS**：在生产环境中启用HTTPS
3. **限制访问IP**：使用防火墙限制Dify平台的访问IP
4. **定期备份数据**：定期备份PostgreSQL数据库和Elasticsearch索引
5. **更新Dify版本**：及时更新Dify到最新版本，修复安全漏洞
6. **使用环境变量管理密钥**：避免在代码中硬编码API密钥和密码

## 10. 扩展建议

1. **添加更多意图**：根据业务需求，扩展意图识别模型
2. **集成更多工具**：添加更多业务API和知识库
3. **优化响应模板**：根据用户反馈，优化响应内容
4. **添加多轮对话支持**：支持更复杂的对话场景
5. **添加情感分析**：识别用户情绪，提供更个性化的服务
6. **添加A/B测试**：测试不同配置的效果，优化智能体性能

---

## 部署验证

完成部署后，使用以下命令验证服务状态：

```bash
# 查看服务状态
docker compose ps

# 验证API服务
curl -X GET http://localhost:8000/health

# 验证前端服务
curl -I http://localhost:3000
```

如果所有服务都正常运行，您可以开始使用智能体了！