from pydantic import BaseModel
import os
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseModel):
    env: str = os.getenv("ENV", "dev")
    database_url: str = os.getenv("DATABASE_URL")

    github_token: str | None = os.getenv("GITHUB_TOKEN")
    github_default_owner: str | None = os.getenv("GITHUB_DEFAULT_OWNER")
    github_default_repo: str | None = os.getenv("GITHUB_DEFAULT_REPO")


settings = Settings()
