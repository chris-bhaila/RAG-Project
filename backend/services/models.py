from langchain.chat_models import init_chat_model # pyright: ignore[reportMissingImports]
from langchain.messages import HumanMessage, SystemMessage # pyright: ignore[reportMissingImports]
from langchain_openai import OpenAIEmbeddings # pyright: ignore[reportMissingImports]
from config.config import settings

class Model():
    def __init__(self, base_url, api_key):
        self.base_url = base_url
        self.api_key = api_key

    def chatmodel(self, model_name, temp):
        return init_chat_model(
            model=model_name,
            model_provider="openai",
            temperature=temp,
            base_url=self.base_url,
            api_key=self.api_key,
        )

    def embedding_model(self, model_name):
        return OpenAIEmbeddings(
            model=model_name,
            check_embedding_ctx_length=False,
            chunk_size=16,
            base_url=self.base_url,
            api_key=self.api_key,
        )

model_provider = Model(base_url=settings.LMSTUDIO_URL, api_key=settings.LMSTUDIO_API)

