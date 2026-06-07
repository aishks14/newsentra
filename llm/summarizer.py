from langchain_core.prompts import ChatPromptTemplate
from llm.groq_client import get_llm
from llm.prompts import NEWS_SUMMARY_PROMPT


def generate_summary(query, articles, model_name):
    llm = get_llm(
        model_name
    )
    prompt = ChatPromptTemplate.from_template(
        NEWS_SUMMARY_PROMPT
    )

    chain = prompt | llm
    content = "\n\n".join(
            [
                f"""
        Title:
        {article.get('title', '')}

        Description:
        {article.get('description', '')}

        Source:
        {article.get('source', '')}

        Date:
        {
        article.get('publishedAt')
        or
        article.get('pubDate')
        or
        ''
        }
        """
                for article in articles[:40]
            ]
        )

    response = chain.invoke(
        {
            "query": query,
            "articles": content
        }
    )
    
    return response.content