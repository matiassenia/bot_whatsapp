from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str 
    app_env: str 
    verify_token: str 
    whatsapp_access_token: str 
    whatsapp_phone_number_id: str 
    whatsapp_api_version: str = "v22.0"
    
    model_config = SettingsConfigDict(
        env_file=".env", 
        env_file_encoding="utf-8")
    
settings = Settings()