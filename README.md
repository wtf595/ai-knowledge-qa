# 📚 课程知识库问答助手 (AI Knowledge QA)

一个基于 DeepSeek API 和 Streamlit 构建的本地知识库问答工具。支持上传课程资料，通过 RAG（检索增强生成）流程，利用大模型进行基于资料的问答。

## ✨ 功能特性
- 支持上传 `.txt` 或 `.md` 格式的课程资料。
- 自动对文本进行切分和关键词检索。
- 结合检索到的上下文，调用 DeepSeek 大模型生成回答，减少模型幻觉。
- 提供简洁的 Web 界面，支持文件上传和实时对话。

## 🛠️ 技术栈
- **语言**：Python
- **大模型 API**：DeepSeek API (deepseek-chat)
- **Web 框架**：Streamlit
- **核心流程**：RAG (Retrieval-Augmented Generation)、Prompt Engineering

## 🚀 如何运行

### 1. 克隆项目
```bash
git clone https://github.com/wtf595/ai-knowledge-qa.git
cd ai-knowledge-qa