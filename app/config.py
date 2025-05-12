from pydantic import Field
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    MONGO_URI: str = Field("mongodb://localhost:27017", env="MONGO_URI")
    MONGO_DB: str = Field("family_finance_db", env="MONGO_DB")
    TEST_MONGO_URI: str = Field("mongodb://localhost:27017", env="TEST_MONGO_URI")
    TEST_MONGO_DB: str = Field("test_family_finance_db", env="TEST_MONGO_DB")
    ALLOWED_ORIGINS: list[str] = Field(default_factory=list)

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()