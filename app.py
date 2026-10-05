import os
from openai import OpenAI
import streamlit as st

# 优先从 Streamlit Secrets 读取，本地开发时回退到环境变量
try:
    api_key = st.secrets["DEEPSEEK_API_KEY"]
except (KeyError, FileNotFoundError):
    api_key = os.getenv("DEEPSEEK_API_KEY")

client = OpenAI(
    api_key=api_key,
    base_url="https://api.deepseek.com"
)

# 1. 文本切分函数
def split_text(text, chunk_size=300):
    paragraphs = [p.strip() for p in text.split("\n") if p.strip()]
    chunks = []
    for p in paragraphs:
        if len(p) <= chunk_size:
            chunks.append(p)
        else:
            for i in range(0, len(p), chunk_size):
                chunks.append(p[i:i + chunk_size])
    return chunks

# 2. 简单关键词检索函数
def simple_retrieve(query, chunks, top_k=3):
    query_terms = set(re.findall(r"[\w\u4e00-\u9fa5]+", query.lower()))
    scored = []
    for c in chunks:
        c_terms = set(re.findall(r"[\w\u4e00-\u9fa5]+", c.lower()))
        score = len(query_terms & c_terms)
        if score > 0:
            scored.append((score, c))
    scored.sort(key=lambda x: x[0], reverse=True)
    return [c for _, c in scored[:top_k]] or chunks[:top_k]

# 3. 调用 DeepSeek API 生成回答
def ask_deepseek(question, context):
    prompt = f"""你是一个课程知识库问答助手。请根据以下资料回答问题。
如果资料中没有答案，请说“资料中未找到相关信息”，不要编造。

资料：
{context}

问题：{question}
回答："""
    resp = client.chat.completions.create(
        model="deepseek-chat",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
    )
    return resp.choices[0].message.content

# 4. Streamlit 网页界面
st.set_page_config(page_title="课程知识库问答助手", page_icon="📚")
st.title("📚 课程知识库问答助手")

uploaded = st.file_uploader("上传课程资料（txt/md）", type=["txt", "md"])

if uploaded:
    text = uploaded.read().decode("utf-8")
    chunks = split_text(text)
    st.success(f"已加载 {len(chunks)} 个文本片段")

    question = st.text_input("请输入问题：")
    if question:
        context = "\n\n".join(simple_retrieve(question, chunks))
        with st.spinner("正在检索资料并生成回答..."):
            try:
                answer = ask_deepseek(question, context)
                st.markdown("### 回答")
                st.write(answer)
                with st.expander("查看检索到的资料片段"):
                    st.write(context)
            except Exception as e:
                st.error(f"调用API出错: {e}")
