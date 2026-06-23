# -*- coding: utf-8 -*-
"""
@Time ： 2026/6/22 15:01
@Auth ： vincent
@File ：model_client.py
@IDE ：PyCharm
"""
from autogen_ext.models.openai import OpenAIChatCompletionClient
import os

def create_openai_model_client():
    """创建并配置 OpenAI 模型客户端"""
    return OpenAIChatCompletionClient(
        model=os.getenv("LLM_MODEL_ID", "gpt-4o"),
        api_key=os.getenv("LLM_API_KEY"),
        base_url=os.getenv("LLM_BASE_URL", "https://api.openai.com/v1"),
        # ↓↓↓ DeepSeek 不是 OpenAI 官方模型，客户端不认识它的能力，
        #     必须用 model_info 显式告知，否则创建时直接报错。
        model_info={
            "family": "unknown",         # 非 OpenAI 家族，填 unknown
            "vision": False,             # 不支持图像输入
            "function_calling": True,    # 支持函数调用（智能体框架要用到）
            "json_output": True,         # 支持 JSON 输出
            "structured_output": False,  # 不强依赖严格结构化输出
        },
    )
