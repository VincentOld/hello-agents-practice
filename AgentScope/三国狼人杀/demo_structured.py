# -*- coding: utf-8 -*-
"""
对比 demo：同一个问题，普通问法 vs 给“表格”让模型填。
直接看两次返回的东西有什么不同，就明白结构化输出是怎么回事了。
"""
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.environ["LLM_API_KEY"], base_url=os.environ["LLM_BASE_URL"])

question = [{"role": "user", "content": "刘备、曹操、诸葛亮三人里，谁最可疑？"}]

# ========== A) 普通问法：模型回一段自由文本 ==========
a = client.chat.completions.create(model="deepseek-chat", messages=question)
print("========== A 普通问法 ==========")
print("message.content（一段话）:\n", a.choices[0].message.content)
print("\nmessage.tool_calls（是空的）:", a.choices[0].message.tool_calls)


# ========== B) 给一张“表格”让它填：模型回结构化数据 ==========
b = client.chat.completions.create(
    model="deepseek-chat",
    messages=question,
    tools=[{
        "type": "function",
        "function": {
            "name": "answer",
            "description": "回答谁最可疑",
            "parameters": {                       # ← 这就是那张“表格”
                "type": "object",
                "properties": {
                    "most_suspicious": {
                        "type": "string",
                        "enum": ["刘备", "曹操", "诸葛亮"],  # 只能填这三个之一
                    },
                    "reason": {"type": "string"},
                },
                "required": ["most_suspicious", "reason"],
            },
        },
    }],
    tool_choice={"type": "function", "function": {"name": "answer"}},  # 强制必须填表
)
print("\n========== B 给表格让它填 ==========")
print("message.content（这次是空的）:", b.choices[0].message.content)
print("tool_calls[0].arguments（填好的表，JSON 字符串）:")
print("   ", b.choices[0].message.tool_calls[0].function.arguments)
