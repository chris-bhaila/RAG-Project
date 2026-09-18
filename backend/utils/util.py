from langchain_core.prompts import ChatPromptTemplate # pyright: ignore[reportMissingImports]

def augment_messages(user_question, context):

    system_prompt = """
    You are a helpful AI assistant.

    Your job is to answer the user's question ONLY using the information provided in the retrieved context.

    Rules:
    1. You are allowed to greet the user naturally (e.g., "Hello!", "Hi there! How can I help you today?") at the beginning of your response.
    2. Use only the retrieved context to answer the factual parts of the user's question.
    3. If the answer to the question is not present in the context, reply:
    "I couldn't find that information in the provided documents."
    4. Do not make up, guess or use outside knowledge to answer questions.
    5. If multiple pieces of context are provided, combine them to give a complete answer.
    6. Be clear, concise and accurate.
    7. If the user asks a follow-up question, use the previous conversation along with the retrieved context to answer it.
    8. If the context is insufficient to answer the question, clearly state that the information is not available in the provided documents.
    9. You can add preambles like "Based on the provided context, ..." or "According to the documents, ..."

    Always prioritize the retrieved context over any prior knowledge when answering questions.
    """


    question = "What is the expected number of injured people if an earthquake of 1934 magnitude strikes at the present time?"

    prompt = ChatPromptTemplate.from_messages([
        ('system', system_prompt),
        ('human', """Here is the Context: {relevant_docs} Look through it and answer the question: {question}""")
    ])

    return prompt.format_prompt(relevant_docs=context, question=user_question).to_messages()