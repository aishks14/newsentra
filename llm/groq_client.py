from langchain_groq import ChatGroq


def get_llm(model_name):

    return ChatGroq(
        model=model_name,
        temperature=0.2,
        max_tokens=4096
    )