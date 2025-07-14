# AI焦点速递 MCP服务

## 服务介绍

AI焦点速递是一个基于MCP（Model Context Protocol）的智能情报收集工具，能够从多个权威信源实时获取AI领域的最新动态，包括学术论文、技术博客和行业新闻。

## 功能特性

- 🔍 **多源搜索**: 支持ArXiv学术论文、顶级公司技术博客、行业新闻网站
- ⏰ **时间筛选**: 支持过去24小时、一周、一月的动态筛选
- �� **智能汇总**: 自动生成结构化的情报报告
- �� **精准匹配**: 基于关键词的精准内容匹配

## 服务配置

```json
{
  "mcpServers": {
    "ai-focus-express": {
      "command": "uvx",
      "args": ["ai-focus-express-mcp"],
      "env": {
        "PYTHONPATH": ".",
        "GRADIO_SERVER_NAME": "0.0.0.0",
        "GRADIO_SERVER_PORT": "7860"
      }
    }
  }
}
```

## 环境变量配置

- `PYTHONPATH`: Python模块搜索路径
- `GRADIO_SERVER_NAME`: Gradio服务器地址
- `GRADIO_SERVER_PORT`: Gradio服务器端口

## 使用方法

1. 启动服务：
   ```bash
   python app.py
   ```

2. 访问Web界面：
   - 打开浏览器访问 `http://localhost:7860`
   - 输入AI相关关键词（如：Mixture of Experts, LLM Agent）
   - 选择时间范围（过去24小时/一周/一月）
   - 点击提交获取情报报告

3. 作为MCP服务调用：
   - 配置MCP客户端连接
   - 通过API调用获取AI领域最新动态

## 依赖安装

```bash
pip install gradio arxiv requests beautifulsoup4 google-search-python python-dateutil
```

## 支持的信源

### 学术论文
- ArXiv (cs.AI, cs.LG, cs.CL)

### 技术博客
- OpenAI Blog
- Google AI Blog  
- Hugging Face Blog

### 行业新闻
- TechCrunch AI

## 开发说明

- `app.py`: 主应用入口，提供Gradio Web界面
- `core_functions.py`: 核心搜索和报告生成逻辑
- `web_utils.py`: 网络爬取和内容解析工具
- `report_generator.py`: 报告格式化和生成
- `sources.json`: 信源配置文件
- `batch_tester.py`: 信源兼容性测试工具

## 许可证

MIT License
