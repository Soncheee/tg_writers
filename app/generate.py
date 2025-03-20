import logging
import asyncio
from openai import AsyncOpenAI
from config import AI_TOKEN

logger = logging.getLogger(__name__)

client = AsyncOpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=AI_TOKEN,
)

async def ai_generate(text: str, context: list = None) -> tuple[str, list]:
    try:
        logger.info(f"Отправка запроса к модели с текстом: {text}")
        messages = context if context else []
        messages.append({"role": "user", "content": text})
        completion = await client.chat.completions.create(
            model="deepseek/deepseek-chat",
            messages=messages
        )
        logger.info("Ответ от модели получен")
        response = completion.choices[0].message.content
        messages.append({"role": "assistant", "content": response})
        return response, messages
    except Exception as e:
        logger.error(f"Ошибка при запросе к модели: {e}")
        return "Произошла ошибка при генерации ответа. Пожалуйста, попробуйте позже.", context