# ContentSimilarity应用配置指南

## 一、Chatflow配置步骤

### 1. 当前Chatflow状态

从您提供的截图可以看到，您已经创建了基础的Chatflow，包含：
- 用户输入节点
- LLM节点
- 配置变量节点

### 2. 添加向量数据库查询节点

1. **点击「添加节点」按钮**：在LLM节点右侧，点击「添加节点」
2. **选择「向量数据库查询」节点**：从节点列表中选择此节点
3. **连接节点**：将LLM节点的输出连接到向量数据库查询节点的输入
4. **配置向量数据库连接**：
   - 数据库类型：PostgreSQL
   - 连接URL：`postgresql://postgres:postgres@docker-db-1:5432/dify`
   - 表名：`contents`
   - 向量字段：`embedding`
   - 匹配字段：`content`

### 3. 配置LLM节点

1. **模型选择**：选择适合的LLM模型（如GPT-4或本地模型）
2. **提示词配置**：
   ```
   作为内容相似度匹配助手，您需要：
   1. 理解用户的查询意图
   2. 将查询转换为向量嵌入
   3. 在向量数据库中查找最相似的内容
   4. 返回相似度最高的前5条结果
   
   用户查询：{{user_input}}
   ```

### 4. 配置输出节点

1. **添加「输出」节点**：连接向量数据库查询节点的输出
2. **配置响应模板**：
   ```
   找到以下与您的查询相关的内容：
   
   {% for item in results %}
   1. **{{item.title}}**
      - 话题：{{item.topic}}
      - 相似度：{{item.similarity_score | round(2)}}
      - 内容：{{item.content[:100]}}...
      - 图片：{% if item.images %}{{item.images[0]}}{% else %}无{% endif %}
   {% endfor %}
   
   {% if not results %}
   没有找到相关内容。
   {% endif %}
   ```

## 二、PostgreSQL数据库配置

### 1. 连接数据库

```bash
docker exec -it docker-db-1 psql -U postgres -d dify
```

### 2. 验证contents表结构

```sql
\d contents
```

### 3. 插入测试数据

```sql
-- 插入测试数据
INSERT INTO contents (project_id, topic, title, content, video, images, tags, embedding)
VALUES 
('default', '美妆', '夏日防晒指南', '夏天来了，如何选择适合自己的防晒霜？本文将为您详细介绍...', NULL, '["https://file-box.homeking365.com/69/2025-12-25/185NU-m8kt8GH3QWftefl.jpg?width=1036&height=1274&x-oss-process=image/format,webp/quality,q_20"]', '["防晒", "美妆", "夏日"]', '[0.1, 0.2, 0.3, 0.4, 0.5]'),
('default', '美妆', '口红颜色选择技巧', '不同肤色适合不同的口红颜色，本文将教您如何根据肤色选择...', NULL, '["https://file-box.homeking365.com/69/2025-12-23/fhVngIqaWxZGGFcfD3j2K.jpg?width=1280&height=1588&x-oss-process=image/format,webp/quality,q_20"]', '["口红", "美妆", "颜色选择"]', '[0.2, 0.3, 0.4, 0.5, 0.6]'),
('default', '穿搭', '秋季穿搭灵感', '秋天的穿搭既要保暖又要时尚，本文为您提供10种秋季穿搭...', NULL, '["https://file-box.homeking365.com/69/2025-12-28/PySfSzQpEO3vwZEf0wtcC.jpg?width=640&height=666&x-oss-process=image/format,webp/quality,q_20"]', '["穿搭", "秋季", "时尚"]', '[0.3, 0.4, 0.5, 0.6, 0.7]');
```

## 三、测试应用

1. **点击「部署」按钮**：部署您的Chatflow应用
2. **点击「预览」按钮**：进入预览界面
3. **输入测试查询**：如「夏天如何防晒？」
4. **查看结果**：应用应返回相关的防晒内容

## 四、使用API调用

### 1. 从Dify平台获取API密钥

- 注意：如果在用户菜单中找不到API密钥选项，请联系Dify平台管理员
- 或者使用环境变量中已有的API密钥

### 2. 调用示例

```bash
curl -X POST http://localhost:5001/v1/chat-messages \
  -H "Authorization: Bearer $DIFY_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "夏天如何防晒？", "user": "test_user"}'
```

## 五、注意事项

1. 确保PostgreSQL数据库已启用pgvector扩展（如果使用向量类型）
2. 确保contents表中的embedding字段已正确填充向量值
3. 调整相似度阈值以获得更准确的结果
4. 定期更新向量值以保持内容的时效性

## 六、下一步

- 配置自动向量生成服务
- 添加内容审核机制
- 优化向量生成模型
- 实现内容推荐功能