import sys
from types import ModuleType
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

if "openai" not in sys.modules:
    openai_stub = ModuleType("openai")
    openai_stub.AsyncOpenAI = object
    openai_stub.pydantic_function_tool = object

    openai_types = ModuleType("openai.types")
    openai_types_chat = ModuleType("openai.types.chat")
    openai_types_chat.ChatCompletionFunctionToolParam = object

    class _ChatCompletionChunk:
        def model_dump_json(self) -> str:
            return "{}"

    openai_types_chat.ChatCompletionChunk = _ChatCompletionChunk

    openai_types.chat = openai_types_chat
    openai_stub.types = openai_types

    sys.modules["openai"] = openai_stub
    sys.modules["openai.types"] = openai_types
    sys.modules["openai.types.chat"] = openai_types_chat

if "fastmcp" not in sys.modules:
    fastmcp_stub = ModuleType("fastmcp")
    fastmcp_stub.Client = object
    sys.modules["fastmcp"] = fastmcp_stub

if "yaml" not in sys.modules:
    yaml_stub = ModuleType("yaml")

    def _safe_load_stub(*args, **kwargs):
        return {}

    yaml_stub.safe_load = _safe_load_stub
    sys.modules["yaml"] = yaml_stub

if "envyaml" not in sys.modules:
    config_data = {
        "openai": {
            "api_key": "test",
            "base_url": "https://example.com",
            "model": "gpt",
            "max_tokens": 1000,
            "temperature": 0.5,
            "proxy": "",
        },
        "tavily": {"api_key": "test", "api_base_url": "https://example.com"},
        "elastic": {
            "elastic_timeout": 30,
            "know2_api_base_url": "https://know-two-api-dev.yakov.partners",
            "know2_auth_login_username": "user",
            "know2_auth_login_password": "pass",
        },
    }

    class EnvYAML(dict):
        def __init__(self, *_args, **_kwargs):
            super().__init__(config_data)

    envyaml_stub = ModuleType("envyaml")
    envyaml_stub.EnvYAML = EnvYAML
    sys.modules["envyaml"] = envyaml_stub

if "jambo" not in sys.modules:
    jambo_stub = ModuleType("jambo")
    jambo_stub.SchemaConverter = object
    sys.modules["jambo"] = jambo_stub

if "tavily" not in sys.modules:
    tavily_stub = ModuleType("tavily")
    tavily_stub.AsyncTavilyClient = object
    sys.modules["tavily"] = tavily_stub
