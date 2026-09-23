from langchain_core.language_models import BaseChatModel

from app.config import Settings


def build_chat_model(settings: Settings) -> BaseChatModel:
    provider = settings.llm_provider.strip().lower()

    if provider in {"qwen", "openai", "openai-compatible"}:
        if not settings.llm_model:
            raise ValueError("LLM_MODEL is required for an OpenAI-compatible provider")
        if not settings.llm_api_key:
            raise ValueError("LLM_API_KEY is required for an OpenAI-compatible provider")

        from langchain_openai import ChatOpenAI

        model_kwargs = {
            "model": settings.llm_model,
            "api_key": settings.llm_api_key,
        }
        if settings.llm_base_url:
            model_kwargs["base_url"] = settings.llm_base_url
        return ChatOpenAI(**model_kwargs)

    if provider == "ollama":
        if not settings.llm_model:
            raise ValueError("LLM_MODEL is required for Ollama")

        from langchain_ollama import ChatOllama

        model_kwargs = {
            "model": settings.llm_model,
            "reasoning": False,
            "temperature": 0,
            "num_predict": 512,
        }
        if settings.llm_base_url:
            model_kwargs["base_url"] = settings.llm_base_url
        return ChatOllama(**model_kwargs)

    raise ValueError(
        f"Unsupported LLM_PROVIDER: {settings.llm_provider}. "
        "Use qwen, openai, openai-compatible, or ollama."
    )
