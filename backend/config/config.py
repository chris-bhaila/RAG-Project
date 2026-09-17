from pathlib import Path
from pydantic import model_validator
from loguru import logger # pyright: ignore[reportMissingImports]
from pydantic_settings import BaseSettings, SettingsConfigDict # pyright: ignore[reportMissingImports]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=Path(__file__).parent / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    PORT: int
    PINECONE_API_KEY: str
    LMSTUDIO_URL: str
    CHAT_MODEL: str
    EMBEDDING_MODEL: str
    LMSTUDIO_API: str
    VECTOR_STORE: str | None = "my_vector_store"
    ENV: str | bool | None = "local"

    @model_validator(mode="after")
    def transform_env_to_bool(self):
        if isinstance(self.ENV, str):
            self.ENV = self.ENV == "dev"
        return self

settings = Settings()

for name, value in settings.dict().items():
    logger.info("Loading the Environment Variable")
    logger.info(f"{name}: {str(value)[:6]}{'*' * (len(str(value)) - 6)}")
    logger.info("=" * 50)
