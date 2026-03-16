from dataclasses import dataclass

from openai import APIConnectionError, APIError, OpenAI

from app.core.exceptions import AppError
from app.core.config import settings


@dataclass(slots=True)
class LocalLLMResponse:
    output_text: str
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int


class OllamaLLMClient:
    def __init__(self) -> None:
        self._client = OpenAI(
            base_url=settings.ollama_base_url,
            api_key=settings.ollama_api_key,
        )
        self.model = settings.ollama_model

    def generate(self, model_input: str) -> LocalLLMResponse:
        try:
            response = self._client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "user",
                        "content": model_input,
                    }
                ],
            )
        except (APIConnectionError, APIError) as exc:
            raise AppError(502, f"Failed to call local Ollama model '{self.model}': {exc}") from exc
        usage = response.usage
        output_text = response.choices[0].message.content or ""

        return LocalLLMResponse(
            output_text=output_text,
            prompt_tokens=usage.prompt_tokens if usage else 0,
            completion_tokens=usage.completion_tokens if usage else 0,
            total_tokens=usage.total_tokens if usage else 0,
        )
