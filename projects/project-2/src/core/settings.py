from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    app_name: str = "Compliance Checker API - Project 2"
    app_env: str = Field(default="dev")

    azure_openai_endpoint: str = Field(alias="AZURE_OPENAI_ENDPOINT")
    azure_openai_key: str = Field(alias="AZURE_OPENAI_KEY")
    azure_openai_api_version: str = Field(alias="AZURE_OPENAI_API_VERSION")
    azure_deployment_name: str = Field(alias="AZURE_DEPLOYMENT_NAME")

    vector_db_path: str = Field(default="./data/output/chroma_db")
    collection_name: str = Field(default="compliance_policies")
    embedding_model_name: str = Field(default="sentence-transformers/all-MiniLM-L6-v2")

    chunk_size: int = Field(default=800)
    chunk_overlap: int = Field(default=120)
    retrieval_top_k: int = Field(default=8)
    rerank_top_k: int = Field(default=4)


settings = Settings()