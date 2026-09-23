from app.config import get_settings
from app.llm.client import build_chat_model


def main() -> None:
    settings = get_settings()
    model = build_chat_model(settings)
    response = model.invoke(
        "用一句话回答：为什么智能合约安全审计需要结合静态分析和大语言模型？"
    )
    print(response.content)


if __name__ == "__main__":
    main()

