from dataclasses import dataclass
from typing import List, Optional

import openai


@dataclass
class LVLMExtractor:
    """Query OpenAI GPT-4-Vision model with images and a prompt."""

    api_key: str
    model_name: str = "gpt-4-vision-preview"

    def __post_init__(self) -> None:
        openai.api_key = self.api_key

    def query(self, base64_frames: List[str], prompt_text: str, max_tokens: int = 2000) -> Optional[str]:
        if not base64_frames:
            raise ValueError("No frames provided to LVLM")

        messages_content = [{"type": "text", "text": prompt_text}]
        for b64_frame in base64_frames:
            messages_content.append({
                "type": "image_url",
                "image_url": {"url": f"data:image/jpeg;base64,{b64_frame}"}
            })

        messages = [{"role": "user", "content": messages_content}]

        try:
            response = openai.chat.completions.create(
                model=self.model_name,
                messages=messages,
                max_tokens=max_tokens,
            )
            return response.choices[0].message.content
        except Exception as exc:  # pylint: disable=broad-except
            print(f"LVLM query failed: {exc}")
            return None
