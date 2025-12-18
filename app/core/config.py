from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Agente de Captação Estética"
    API_V1_STR: str = "/api/v1"
    DATABASE_URL: str = "sqlite:///./sql_app.db"
    
    # LLM Settings
    LLM_PROVIDER: str = "openrouter"  # openai, openrouter, ollama
    LLM_MODEL: str = "openai/gpt-4o"
    
    # Vision Settings
    VISION_MODEL: str = "openai/gpt-4o" # Modelos que suportam visão
    
    # API Keys
    OPENAI_API_KEY: str = ""
    OPENROUTER_API_KEY: str = ""
    SERPER_API_KEY: str = "" # Chave para busca real no Google/Instagram
    
    # Base URLs
    OPENROUTER_BASE_URL: str = "https://openrouter.ai/api/v1"
    OLLAMA_BASE_URL: str = "http://localhost:11434/v1"

    class Config:
        env_file = ".env"

settings = Settings()
