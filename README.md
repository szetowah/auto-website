# Auto Website 生成器

## 项目简介
本项目是一个基于 Flask 的自动网站生成服务。用户可以通过 API 提交 HTML 内容，系统会为每份内容生成唯一的静态网站，并可通过唯一链接访问。

## 主要功能
- 提供 `/generate` POST 接口，接收 HTML 内容并生成静态网站。
- 每个网站分配唯一访问路径 `/site/<hash>`。
- 错误处理与日志记录。

## 目录结构
```
├── app.py              # 主应用程序
├── requirements.txt    # Python 依赖
├── Dockerfile          # Docker 构建文件
└── static/             # 生成的网站静态文件目录（自动创建）
```

## 安装与运行
### 1. 本地运行
1. 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```
2. 启动服务：
   ```bash
   python app.py
   ```
3. 默认监听端口：8080

### 2. Docker 运行
1. 构建镜像：
   ```bash
   docker build -t auto-website .
   ```
2. 运行容器：
   ```bash
   docker run -d -p 8080:8080 auto-website
   ```

## API 说明
### 1. 生成网站
- **接口**：`POST /generate`
- **参数**：JSON 格式，包含 `html` 字段（字符串，必填）
- **返回**：生成网站的唯一访问 URL
- **示例**：
  ```bash
  curl -X POST http://localhost:8080/generate \
    -H "Content-Type: application/json" \
    -d '{"html": "<h1>Hello, World!</h1>"}'
  ```

### 2. 访问网站
- **接口**：`GET /site/<hash>`
- **说明**：通过生成的唯一 URL 访问静态网站内容。

## 依赖
- Python 3.10+
- Flask >=2.0.0, <3.0.0

## 注意事项
- `static/` 目录会自动创建，用于存放生成的网站内容。
- 请确保 8080 端口未被占用。

## License
MIT
