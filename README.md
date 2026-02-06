# RFP Filler Agent - AI驱动的投标/问卷自动填充工具

<div align="center">

[![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-green.svg)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![ mise ](https://img.shields.io/badge/mise-2026.2.4-FF85A2)](https://mise.jdx.dev/)
[![ uv ](https://img.shields.io/badge/uv-0.10.0-6BF17A)](https://github.com/astral-sh/uv)

**中文文档** | [English](#english)

</div>

---

## 中文文档

一个基于 AI 的 B2B 问卷自动填充 Agent，专门用于处理投标安全问卷、RFP 标书等重复性高、枯燥的 Excel 填写工作。

**核心价值**：节省销售/售前 80% 的填写时间，高客单价（$50/份 或 $500/月订阅）。

### 核心特性

- ✅ 自动扫描 Excel 中的问题单元格
- ✅ 基于知识库智能匹配答案
- ✅ 标记不确定答案供人工复核
- ✅ 保持 Excel 格式不变
- ✅ 批量处理支持
- ✅ RESTful API 接口
- ✅ Redis 缓存支持（可选）
- ✅ 完整的 Swagger UI 文档

### 技术栈

- **后端**: FastAPI (Python 3.12+)
- **Agent 框架**: PydanticAI
- **数据库**: Supabase (PostgreSQL)
- **LLM 接入**: OpenRouter (支持 Claude/GPT/Gemini)
- **Excel 处理**: openpyxl, pandas
- **工具管理**: mise (Python 版本) + uv (依赖管理)

### 快速开始

#### 前置要求

- Python 3.12+
- [mise](https://mise.jdx.dev/) - 系统工具管理器
- [uv](https://github.com/astral-sh/uv) - Python 包管理器
- [Supabase](https://supabase.com/) - PostgreSQL 数据库（可选）
- OpenRouter API Key: [获取密钥](https://openrouter.ai/)

#### 安装步骤

```bash
# 1. 克隆仓库
git clone https://github.com/Desperado1001/rfp-filler-agent.git
cd rfp-filler-agent

# 2. 安装系统工具和依赖
mise install
uv sync

# 3. 安装 Playwright 浏览器
uv run playwright install chromium
```

#### 配置环境变量

```bash
# 复制环境变量模板
cp .env.example .env

# 编辑配置
nano .env  # 填入 OpenRouter 和 Supabase 密钥
```

#### 启动服务

```bash
# 后端
uv run python main.py

# 服务将在 http://localhost:8000 启动
```

#### 访问 API 文档

启动后，访问 http://localhost:8000/docs 查看 Swagger UI 文档。

### 使用示例

#### 1. 导入示例知识库

```bash
curl -X POST http://localhost:8000/api/knowledge/import-sample
```

响应：
```json
{
  "message": "已导入 8 条示例知识",
  "count": 8
}
```

#### 2. 上传并填写问卷

```bash
# 1. 上传 Excel 文件
curl -X POST "http://localhost:8000/api/upload" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@your_questionnaire.xlsx"

响应：
{
  "message": "文件上传成功",
  "file_path": "temp/your_questionnaire.xlsx",
  "filename": "your_questionnaire.xlsx"
}

# 2. 自动填写
curl -X POST "http://localhost:8000/api/fill" \
  -H "Content-Type: application/json" \
  -d '{
    "file_path": "temp/your_questionnaire.xlsx"
  }'

响应：
{
  "task_id": "abc123",
  "status": "completed",
  "filled_cells": [...],
  "output_file": "temp/your_questionnaire_filled.xlsx"
}
```

#### 3. 下载填写后的文件

```bash
curl "http://localhost:8000/api/download/your_questionnaire_filled.xlsx" -o output.xlsx
```

### 项目结构

```
rfp-filler-agent/
├── main.py                 # FastAPI 主程序
├── agent.py               # RFP 填充 Agent 核心逻辑
├── excel_handler.py       # Excel 读写处理
├── rag_service.py         # RAG 知识库服务
├── llm_service.py         # LLM 调用服务
├── models.py              # 数据模型定义
├── generate_test_data.py  # 生成测试数据
├── 7-Day-Plan.md        # 7 天获客计划
├── .env.example           # 环境变量模板
├── pyproject.toml        # uv 项目配置
├── .mise.toml             # mise 工具版本配置
└── README.md              # 本文件
```

### API 端点

| 方法 | 路径 | 描述 |
|------|--------|--------|
| POST | `/api/upload` | 上传 Excel 文件 |
| POST | `/api/fill` | 自动填写问卷 |
| GET | `/api/products` | 获取产品列表 |
| GET | `/api/products/{id}` | 获取单个产品详情 |
| POST | `/api/knowledge` | 添加知识条目 |
| POST | `/api/knowledge/batch` | 批量添加知识 |
| GET | `/api/knowledge` | 列出知识库 |
| POST | `/api/knowledge/import-sample` | 导入示例数据 |
| POST | `/api/test` | 测试知识库查询 |
| GET | `/api/download/{filename}` | 下载文件 |
| GET | `/docs` | Swagger UI 文档 |

### 商业模式

1. **按份付费**: $50/份问卷
2. **订阅制**: $500/月无限使用
3. **企业版**: 私有化部署 $5000+

### 路线图

- [x] MVP 核心功能
- [x] API 接口
- [x] Excel 处理
- [x] RAG 知识库
- [x] Swagger 文档
- [x] 7 天获客计划
- [ ] 前端界面（Next.js + Tailwind）
- [ ] 用户认证和授权
- [ ] 使用量计费
- [ ] WebSocket 实时进度推送

### 贡献

欢迎提交 Issue 和 Pull Request！

### License

MIT

---

<a name="english"></a>

## English Documentation

An AI-powered B2B questionnaire auto-fill Agent, specifically designed for handling repetitive and tedious Excel form-filling tasks such as bidding security questionnaires and RFP proposals.

**Core Value**: Save sales/pre-sales teams 80% of form-filling time with high pricing ($50 per document or $500/month subscription).

### Features

- ✅ Auto-scan question cells in Excel files
- ✅ Intelligent answer matching based on knowledge base
- ✅ Mark uncertain answers for manual review
- ✅ Preserve original Excel formatting
- ✅ Batch processing support
- ✅ RESTful API endpoints
- ✅ Redis caching support (optional)
- ✅ Complete Swagger UI documentation

### Tech Stack

- **Backend**: FastAPI (Python 3.12+)
- **Agent Framework**: PydanticAI
- **Database**: Supabase (PostgreSQL)
- **LLM Integration**: OpenRouter (supports Claude/GPT/Gemini)
- **Excel Processing**: openpyxl, pandas
- **Tool Management**: mise (Python versions) + uv (dependency manager)

### Quick Start

#### Prerequisites

- Python 3.12+
- [mise](https://mise.jdx.dev/) - System tool manager
- [uv](https://github.com/astral-sh/uv) - Python package manager
- [Supabase](https://supabase.com/) - PostgreSQL database (optional)
- OpenRouter API Key: [Get API Key](https://openrouter.ai/)

#### Installation

```bash
# 1. Clone repository
git clone https://github.com/Desperado1001/rfp-filler-agent.git
cd rfp-filler-agent

# 2. Install system tools and dependencies
mise install
uv sync

# 3. Install Playwright browser
uv run playwright install chromium
```

#### Environment Configuration

```bash
# Copy environment variable template
cp .env.example .env

# Edit configuration
nano .env  # Fill in OpenRouter and Supabase keys
```

#### Start Service

```bash
# Backend
uv run python main.py

# Service will start at http://localhost:8000
```

#### Access API Documentation

After starting, visit http://localhost:8000/docs to view Swagger UI documentation.

### Usage Examples

#### 1. Import Sample Knowledge Base

```bash
curl -X POST http://localhost:8000/api/knowledge/import-sample
```

Response:
```json
{
  "message": "已导入 8 条示例知识",
  "count": 8
}
```

#### 2. Upload and Auto-fill Questionnaire

```bash
# 1. Upload Excel file
curl -X POST "http://localhost:8000/api/upload" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@your_questionnaire.xlsx"

Response:
{
  "message": "文件上传成功",
  "file_path": "temp/your_questionnaire.xlsx",
  "filename": "your_questionnaire.xlsx"
}

# 2. Auto-fill
curl -X POST "http://localhost:8000/api/fill" \
  -H "Content-Type: application/json" \
  -d '{
    "file_path": "temp/your_questionnaire.xlsx"
  }'

Response:
{
  "task_id": "abc123",
  "status": "completed",
  "filled_cells": [...],
  "output_file": "temp/your_questionnaire_filled.xlsx"
}
```

#### 3. Download Filled File

```bash
curl "http://localhost:8000/api/download/your_questionnaire_filled.xlsx" -o output.xlsx
```

### Project Structure

```
rfp-filler-agent/
├── main.py                 # FastAPI main program
├── agent.py               # RFP filler agent core logic
├── excel_handler.py       # Excel read/write processing
├── rag_service.py         # RAG knowledge base service
├── llm_service.py         # LLM calling service
├── models.py              # Data model definitions
├── generate_test_data.py  # Generate test data
├── 7-Day-Plan.md        # 7-day customer acquisition plan
├── .env.example           # Environment variable template
├── pyproject.toml        # uv project configuration
├── .mise.toml             # mise tool version config
└── README.md              # This file
```

### API Endpoints

| Method | Path | Description |
|--------|-------|-------------|
| POST | `/api/upload` | Upload Excel file |
| POST | `/api/fill` | Auto-fill questionnaire |
| GET | `/api/products` | Get product list |
| GET | `/api/products/{id}` | Get single product details |
| POST | `/api/knowledge` | Add knowledge entry |
| POST | `/api/knowledge/batch` | Batch add knowledge |
| GET | `/api/knowledge` | List knowledge base |
| POST | `/api/knowledge/import-sample` | Import sample data |
| POST | `/api/test` | Test knowledge base query |
| GET | `/api/download/{filename}` | Download file |
| GET | `/docs` | Swagger UI documentation |

### Business Model

1. **Per-Document**: $50 per questionnaire
2. **Subscription**: $500/month unlimited usage
3. **Enterprise**: Private deployment $5000+

### Roadmap

- [x] MVP core features
- [x] API endpoints
- [x] Excel processing
- [x] RAG knowledge base
- [x] Swagger documentation
- [x] 7-day acquisition plan
- [ ] Frontend UI (Next.js + Tailwind)
- [ ] User authentication and authorization
- [ ] Usage billing
- [ ] WebSocket real-time progress push

### Contributing

Issues and Pull Requests are welcome!

### License

MIT

---

<div align="center">

Made with ❤️ for efficient B2B workflows

</div>
