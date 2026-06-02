# ─── app/config.py ────────────────────────────────────────────────────────────
# Loads environment variables from the .env file into a typed Settings object.
# Using pydantic-settings means every variable is validated at startup —
# the app will refuse to run if a required variable is missing.
#
# TODO: Import BaseSettings from pydantic_settings and Field from pydantic
#
# TODO: Create a Settings class that extends BaseSettings with these fields:
#       - database_url: str
#       - secret_key: str
#       - algorithm: str
#       - access_token_expire_minutes: int
#       - marine_username: str
#       - marine_password: str
#
#       Hint: inside the class, add a model_config = SettingsConfigDict(env_file=".env")
#             this tells pydantic-settings where to read values from
#
# TODO: Create a single settings instance at the bottom of this file
#       so every other module can import it: from app.config import settings
