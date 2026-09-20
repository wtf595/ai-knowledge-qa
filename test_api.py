import os
from openai import OpenAI
from dotenv import load_dotenv

print("1. 开始加载 .env 文件...")
load_dotenv()

api_key = os.getenv("DEEPSEEK_API_KEY")
if api_key:
    print(f"2. API Key 读取成功！(长度: {len(api_key)}, 开头: {api_key[:8]}...)")
else:
    print("2. ❌ 错误：没有读取到 API Key！请检查 .env 文件。")
    exit()

client = OpenAI(
    api_key=api_key,
    base_url="https://api.deepseek.com"
)

print("3. 正在尝试连接 DeepSeek API...")
try:
    resp = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "user", "content": "你好，请回复：API连接成功"}
        ]
    )
    print("4. 连接成功！返回内容如下：")
    print("--------------------------------")
    print(resp.choices[0].message.content)
    print("--------------------------------")
except Exception as e:
    print("4. ❌ API 调用出错！错误信息如下：")
    print(e)