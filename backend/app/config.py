from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    database_url : str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int
    email_host: str
    email_port: int
    email_username: str
    email_password: str
    email_confirmation_hours : int
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

settings = Settings()
