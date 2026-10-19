import json
from pathlib import Path

from pydantic import BaseModel, ConfigDict, Field, field_validator


class Settings(BaseModel):
    model_config = ConfigDict(extra="forbid")

    model_name: str = Field(min_length=1)
    batch_size: int = Field(gt=0, strict=True)
    device: str
    @field_validator("model_name")
    @classmethod
    def validate_model_name(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("Model name cannot be blank")
        return value

def load_settings(path: Path) -> Settings:
    with path.open("r", encoding="utf-8") as file:
        data = json.load(file)

    return Settings.model_validate(data)
