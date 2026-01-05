# SQL查询节点配置指南

## 一、当前节点属性填写建议

### 1. 数据库属性

数据库属性可以留空，或者填写必要的连接参数。对于PostgreSQL数据库，常用的属性包括：

- `sslmode=disable`：禁用SSL连接（适用于本地开发环境）
- `connect_timeout=30`：设置连接超时时间为30秒

如果您的数据库不需要特殊配置，可以直接留空或填写：

```
sslmode=disable
```

### 2. SQL查询语句

根据您的需求，需要编写一个SQL查询语句来实现内容相似度匹配。由于您当前使用的是SQL查询节点而非向量数据库查询节点，您可以使用以下两种方式：

#### 方式一：使用LIKE子句进行文本匹配

```sql
SELECT 
    id, 
    topic, 
    title, 
    content, 
    video, 
    images, 
    tags, 
    1.0 AS similarity_score
FROM 
    contents
WHERE 
    content LIKE '%' || $query || '%' 
    OR title LIKE '%' || $query || '%' 
    OR topic LIKE '%' || $query || '%'
ORDER BY 
    created_at DESC
LIMIT 5;
```

#### 方式二：使用PostgreSQL的相似性函数（需要pg_trgm扩展）

```sql
SELECT 
    id, 
    topic, 
    title, 
    content, 
    video, 
    images, 
    tags, 
    similarity(content, $query) AS similarity_score
FROM 
    contents
WHERE 
    content % $query
ORDER BY 
    similarity_score DESC
LIMIT 5;
```

### 3. 输出格式

输出格式已设置为`MARKDOWN`，这是合适的，可以保持不变。

## 二、使用向量数据库查询节点的优势

虽然SQL查询节点可以实现简单的内容匹配，但对于真正的相似度匹配，建议使用向量数据库查询节点，因为：

1. 向量匹配更准确，能够理解内容的语义相似性
2. 向量查询性能更好，尤其是在大规模数据上
3. 可以设置相似度阈值，精确控制匹配结果
4. Dify平台提供了专门的向量数据库查询节点，配置更简单

## 三、切换到向量数据库查询节点的步骤

1. **删除当前的SQL查询节点**
2. **添加「向量数据库查询」节点**：从节点列表中选择此节点
3. **配置数据库连接**：使用之前提供的正确连接参数
4. **配置查询参数**：
   - 表名：contents
   - 向量字段：embedding
   - 匹配字段：content
   - 相似度阈值：0.8
   - 返回结果数：5
5. **连接节点**：用户输入 → LLM → 向量数据库查询 → 输出

## 四、注意事项

1. 如果使用SQL查询语句中的`$query`变量，需要确保在LLM节点中正确设置了该变量
2. 如果使用pg_trgm扩展，需要先在数据库中启用该扩展：
   ```sql
   CREATE EXTENSION IF NOT EXISTS pg_trgm;
   ```
3. 定期优化数据库查询性能，尤其是在数据量较大时
4. 考虑添加索引来提高查询速度

## 五、测试SQL查询

在数据库连接成功后，您可以在数据库中测试SQL查询语句，确保其返回正确的结果：

```sql
-- 测试LIKE子句查询
SELECT 
    id, 
    topic, 
    title, 
    content, 
    1.0 AS similarity_score
FROM 
    contents
WHERE 
    content LIKE '%防晒%' 
    OR title LIKE '%防晒%' 
    OR topic LIKE '%防晒%'
ORDER BY 
    created_at DESC
LIMIT 5;
```

## 六、输出格式示例

使用MARKDOWN输出格式，您可以在输出节点中配置以下模板：

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