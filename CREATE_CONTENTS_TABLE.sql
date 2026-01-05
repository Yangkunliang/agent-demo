-- 创建contents表
CREATE TABLE IF NOT EXISTS contents (
    id SERIAL PRIMARY KEY,
    project_id VARCHAR(255) NOT NULL DEFAULT 'default',
    topic VARCHAR(255) NOT NULL,
    title VARCHAR(255) NOT NULL,
    content TEXT NOT NULL,
    video VARCHAR(255),
    images JSONB,
    tags JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    embedding vector(1536)
);

-- 创建索引以提高查询性能
CREATE INDEX IF NOT EXISTS idx_contents_topic ON contents(topic);
CREATE INDEX IF NOT EXISTS idx_contents_title ON contents(title);
CREATE INDEX IF NOT EXISTS idx_contents_project_id ON contents(project_id);
CREATE INDEX IF NOT EXISTS idx_contents_created_at ON contents(created_at);

-- 创建向量索引（使用IVFFlat算法，余弦相似度）
CREATE INDEX IF NOT EXISTS idx_contents_embedding ON contents USING ivfflat(embedding vector_cosine_ops);

-- 创建普通文本索引（用于简单匹配）
CREATE INDEX IF NOT EXISTS idx_contents_content ON contents USING GIN(content gin_trgm_ops);
CREATE INDEX IF NOT EXISTS idx_contents_title ON contents USING GIN(title gin_trgm_ops);

-- 创建更新时间的触发器
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_contents_updated_at
BEFORE UPDATE ON contents
FOR EACH ROW
EXECUTE FUNCTION update_updated_at_column();

-- 插入测试数据
INSERT INTO contents (project_id, topic, title, content, video, images, tags)
VALUES 
('default', '美妆', '夏日防晒指南', '夏天来了，如何选择适合自己的防晒霜？本文将为您详细介绍防晒霜的SPF值选择、不同肤质适用的防晒霜类型、正确的涂抹方法以及其他防晒注意事项。', NULL, '["https://file-box.homeking365.com/69/2025-12-25/185NU-m8kt8GH3QWftefl.jpg?width=1036&height=1274&x-oss-process=image/format,webp/quality,q_20"]', '["防晒", "美妆", "夏日"]'),
('default', '美妆', '口红颜色选择技巧', '不同肤色适合不同的口红颜色，本文将教您如何根据肤色选择最适合的口红。包括冷色调肤色、暖色调肤色和中性色调肤色的口红选择建议，以及不同场合的口红搭配技巧。', NULL, '["https://file-box.homeking365.com/69/2025-12-23/fhVngIqaWxZGGFcfD3j2K.jpg?width=1280&height=1588&x-oss-process=image/format,webp/quality,q_20"]', '["口红", "美妆", "颜色选择"]'),
('default', '穿搭', '秋季穿搭灵感', '秋天的穿搭既要保暖又要时尚，本文为您提供10种秋季穿搭风格和搭配技巧。包括层次感穿搭、颜色搭配、材质选择等方面的建议，让您在秋季既舒适又时尚。', NULL, '["https://file-box.homeking365.com/69/2025-12-28/PySfSzQpEO3vwZEf0wtcC.jpg?width=640&height=666&x-oss-process=image/format,webp/quality,q_20"]', '["穿搭", "秋季", "时尚"]'),
('default', '护肤', '敏感肌护理指南', '敏感肌肤需要特别的护理，本文将为您介绍敏感肌的日常护理方法。包括洁面、保湿、防晒等方面的建议，以及如何选择适合敏感肌的护肤品，避免肌肤过敏和刺激。', NULL, '[]', '["敏感肌", "护肤", "护理"]'),
('default', '健康', '秋季养生小常识', '秋季是养生的好时节，本文将为您介绍秋季养生的小常识。包括饮食调理、运动锻炼、作息调整等方面的建议，帮助您在秋季保持健康的身体和良好的精神状态。', NULL, '[]', '["养生", "健康", "秋季"]');

-- 查询表结构，验证创建是否成功
\d contents;

-- 查询插入的数据
SELECT id, topic, title FROM contents;