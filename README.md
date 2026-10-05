# 📚 课程知识库问答助手 (AI Knowledge QA)

基于 **DeepSeek API + Streamlit** 的 RAG 知识库问答应用：上传课程资料，用自然语言提问，
得到**基于资料、可追溯引用来源**的回答，而不是让大模型自由发挥。

🔗 在线体验：https://liu-ai-agent.streamlit.app

---

## 功能特性

- **资料上传**：支持 `.txt` / `.md` 格式的课程资料。
- **文本切分**：按段落切分；超过 300 字符的长段落再按长度切块（`chunk_size` 可调）。
- **关键词检索**：对问题与每个片段做词项交集打分，取相似度最高的 Top-3 片段作为上下文。
- **Prompt 约束**：明确要求模型「仅依据资料回答；资料中没有答案就直说」，降低幻觉。
- **引用可追溯**：回答下方可展开「查看检索到的资料片段」，核对答案依据。
- **异常提示**：API 调用失败时给出明确错误信息，不会白屏或静默失败。

## 技术栈

| 层 | 选型 |
|---|---|
| 语言 | Python |
| 大模型 | DeepSeek API（`deepseek-chat`） |
| Web 框架 | Streamlit |
| 核心流程 | RAG（Retrieval-Augmented Generation）、Prompt Engineering |
| 依赖管理 | requirements.txt |

## 项目结构

```
ai-knowledge-qa/
├── app.py             # 主程序：文本切分 / 关键词检索 / 调用 DeepSeek / Streamlit 界面
├── test_api.py        # API Key 读取与接口连通性自检脚本
├── requirements.txt   # 依赖：streamlit、openai、python-dotenv
├── .gitignore         # 已忽略 .env、__pycache__ 等
└── README.md
```

## 快速开始

### 1. 克隆项目

```bash
git clone https://github.com/wtf595/ai-knowledge-qa.git
cd ai-knowledge-qa
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 配置 DeepSeek API Key

到 [DeepSeek 开放平台](https://platform.deepseek.com/) 申请 API Key，然后二选一：

**本地开发** —— 在项目根目录新建 `.env`：

```env
DEEPSEEK_API_KEY=sk-你的key
```

**Streamlit Community Cloud** —— 在 App 的 `Settings → Secrets` 中添加：

```toml
DEEPSEEK_API_KEY = "sk-你的key"
```

> ⚠️ `.env` 已被 `.gitignore` 忽略，请勿把 Key 提交到仓库。

### 4. 启动应用

```bash
streamlit run app.py
```

浏览器会自动打开 `http://localhost:8501`。

### 5. 自检（可选）

先用小脚本确认 Key 和网络都没问题：

```bash
python test_api.py
```

会依次输出「读取 API Key → 连接 DeepSeek → 返回内容」的结果。

## 使用说明

1. 上传一份 `.txt` 或 `.md` 资料，页面提示「已加载 N 个文本片段」。
2. 在「请输入问题」中输入问题并回车。
3. 查看回答；点开 **「查看检索到的资料片段」** 核对本次回答实际用到的原文。

## 工作原理

```
上传资料
   ↓  按段落切分（>300 字符再切块）
文本片段列表
   ↓  关键词检索：问题与片段做词项交集打分，取 Top-3
检索到的上下文
   ↓  拼进 Prompt（约束：仅依据资料回答，无答案则明说）
DeepSeek API（temperature=0.2）
   ↓
回答 + 引用片段
```

核心逻辑都在 `app.py` 的三个函数里：`split_text()` → `simple_retrieve()` → `ask_deepseek()`。

## 已知限制

这个项目是一个**最小可用的 RAG 原型**，以下限制是已知的：

- **检索语义泛化弱**：`simple_retrieve()` 用的是词项交集匹配，问题换个说法就可能检索不到
  明明写在资料里的片段（实测中确实出现过检索失败、回答「资料中未找到相关信息」的情况）。
- **没有向量检索与重排序**，Top-K 固定为 3，也没有相似度阈值。
- **无多轮对话**：每次提问相互独立，没有历史上下文。
- **单文件处理**：一次只支持一份 txt/md，不支持 PDF / Word。
- **无鉴权、无限流**，仅适合学习与演示，不要直接用于生产环境。

## 后续计划

- [ ] 用 Embedding + 向量库替换关键词检索，提升语义召回
- [ ] 加入重排序（rerank）与可调 Top-K / 相似度阈值
- [ ] 多轮对话与历史记录
- [ ] 支持 PDF / DOCX 解析
- [ ] 建一套小型评测集，量化不同检索策略下的回答准确率

## License

本项目为学习与课程实践用途，暂未指定开源协议。
