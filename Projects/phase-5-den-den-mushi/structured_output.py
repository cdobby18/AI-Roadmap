"""Structured output enforcement via Pydantic schemas."""

import json
from typing import Any

from pydantic import BaseModel, ValidationError


class SentimentResult(BaseModel):
    sentiment: str
    confidence: float
    reasoning: str


class ExtractionResult(BaseModel):
    entities: list[dict[str, str]]
    summary: str


def parse_structured(response_text: str, schema: type[BaseModel]) -> dict[str, Any]:
    """Parse LLM response text into a Pydantic model.

    Tries JSON parsing first; falls back to instructing the model
    via the validation error message.
    """
    text = response_text.strip()
    if text.startswith("```"):
        text = text.strip("```json").strip("```").strip()

    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        return {"error": f"Invalid JSON: {text[:200]}", "raw": text}

    try:
        model = schema(**data)
        return model.model_dump()
    except ValidationError as e:
        return {"error": str(e), "raw": text}


EXTRACTION_SCHEMA = ExtractionResult.model_json_schema()
SENTIMENT_SCHEMA = SentimentResult.model_json_schema()
