import openai
import os
from dotenv import load_dotenv

load_dotenv()

def summarize_with_gpt(text, prompt=None):
    from openai import OpenAI
    import os

    api_key = os.getenv("OPENAI_API_KEY")
    client = OpenAI(api_key=api_key)

    # 프롬프트가 없으면 기본 프롬프트 사용
    if prompt is None:
        prompt = f"""
다음 논문을 아래 항목별로 1~2문장씩 요약해줘:

1. 연구 목적
2. 사용된 방법
3. 주요 결과
4. 결론

논문 본문:
{text[:3500]}
"""

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
    )
    return response.choices[0].message.content.strip()