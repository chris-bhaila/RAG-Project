from langchain_core.prompts import ChatPromptTemplate # pyright: ignore[reportMissingImports]

def augment_messages(user_question, context):

    system_prompt = """
    You are a helpful AI assistant.

    Your job is to answer the user's question ONLY using the information provided in the retrieved context.

    Rules:
    1. Use only the retrieved context to answer the question.
    2. If the answer is not present in the context, reply:
    "I couldn't find that information in the provided documents."
    3. Do not make up, guess or use outside knowledge.
    4. If multiple pieces of context are provided, combine them to give a complete answer.
    5. Be clear, concise and accurate.
    6. If the user asks a follow-up question, use the previous conversation along with the retrieved context to answer it.
    7. If the context is insufficient to answer the question, clearly state that the information is not available in the provided documents.
    8. You can add preambles like "Based on the provided context, ..." or "According tot the documents, ..."

    Always prioritize the retrieved context over any prior knowledge.
    """

    question = "What is the expected number of injured people if an earthquake of 1934 magnitude strikes at the present time?"

    prompt = ChatPromptTemplate.from_messages([
        ('system', system_prompt),
        ('human', """Here is the Context: {relevant_docs} Look through it and answer the question: {question}""")
    ])

    return prompt.format_prompt(relevant_docs=context, question=user_question).to_messages()