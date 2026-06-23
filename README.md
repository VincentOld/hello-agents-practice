# Hello-Agents 实践

跟着 [datawhalechina/Hello-Agents](https://github.com/datawhalechina/Hello-Agents) 教程做的练习仓库，顺便练 Git 与 Python 环境管理。

## AutoGen：多智能体软件开发团队

`AutoGen/比特币价格/` 复现了教程中的案例——让 4 个智能体（产品经理、工程师、代码审查员、用户代理）通过轮流对话协作，开发一个“实时比特币价格”Web 应用。

| 文件 | 说明 |
| --- | --- |
| `output.py` | 成品：Streamlit 网页，显示比特币实时价格与 24 小时涨跌 |
| `autogen_software_team.py` | 多智能体团队主程序（RoundRobinGroupChat 轮流对话） |
| `model_client.py` | LLM 客户端，走 OpenAI 兼容接口（这里接 DeepSeek） |
| `.env.example` | 环境变量模板，复制为 `.env` 后填入自己的 key |

## 运行

需要 Python 3.10+。

```powershell
# 创建并激活虚拟环境（Windows PowerShell）
py -3.10 -m venv .venv
.\.venv\Scripts\Activate.ps1

# 安装依赖
pip install streamlit requests autogen-agentchat "autogen-ext[openai]" python-dotenv
```

**只看成品网页**（不需要 API key）：

```powershell
streamlit run AutoGen/比特币价格/output.py
```

**运行多智能体团队**（需要 LLM key）：先把 `AutoGen/比特币价格/.env.example` 复制为 `.env` 并填入 key，再：

```powershell
cd AutoGen/比特币价格
python autogen_software_team.py
```

## 备注

- 默认使用 [DeepSeek](https://platform.deepseek.com)（OpenAI 兼容接口）；换其他模型只需改 `.env` 里的 `LLM_BASE_URL` / `LLM_MODEL_ID`。
- 使用非 OpenAI 官方模型时，`OpenAIChatCompletionClient` 需要传 `model_info` 声明模型能力，见 `model_client.py`。
