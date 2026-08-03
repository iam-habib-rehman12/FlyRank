from functools import lru_cache
from os import getenv


class Settings:
    def __init__(self) -> None:
        self.supabase_url = getenv("SUPABASE_URL", "").rstrip("/")
        self.supabase_key = getenv("SUPABASE_KEY", "")

    def validate(self) -> None:
        missing = [
            name
            for name, value in {
                "SUPABASE_URL": self.supabase_url,
                "SUPABASE_KEY": self.supabase_key,
            }.items()
            if not value
        ]
        if missing:
            raise RuntimeError(f"Missing environment variables: {', '.join(missing)}")


@lru_cache
def get_settings() -> Settings:
    return Settings()
