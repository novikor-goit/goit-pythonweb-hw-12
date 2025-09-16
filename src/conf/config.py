from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    DB_URL: str

    JWT_SECRET: str
    JWT_ALGORITHM: str
    ACCESS_TOKEN_LIFETIME_MINUTES: int
    CRYPT_ALGORITHM: str = "bcrypt"

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()  # type: ignore
for config in [settings]:
    for key, value in config:
        if value is None:
            raise ValueError(f"Missing value for {key} in Settings")
