import json
import os
import requests


# Featherless uses OpenAI-compatible API
FEATHERLESS_API_URL = "https://api.featherless.ai/v1/chat/completions"
# Good free models on Featherless:
MODELS = [
    "TroyDoesAI/Llama-3.1-8B-Instruct",
    "amgadhasan/Llama-3.1-8B-Instruct",
    "meta-llama/Llama-3.1-8B-Instruct",
]


def generate_script(topic: dict) -> dict:
    """
    Takes a topic dict and returns a full video script.
    Uses Featherless AI (OpenAI-compatible, free credits).
    """
    api_key = os.environ["FEATHERLESS_API_KEY"]

    prompt = f"""You are the scriptwriter for "IT GIRL" — a YouTube channel that explains tech concepts 
simply and beautifully, using girly/lifestyle analogies. The vibe is warm, smart, and fun — 
like a knowledgeable friend explaining things over coffee.

Write a YouTube video script for this topic:
- Concept: {topic['concept']}
- Suggested title: {topic['title']}
- Core analogy to use: {topic['analogy']}

Script requirements:
- Duration: ~3-4 minutes when read aloud (~450-550 words)
- Language: English (natural, conversational)
- Start with a hook — a question or surprising fact (first 15 seconds are crucial)
- Use the provided analogy early
- Add 1-2 more girly/lifestyle analogies throughout
- Break into clear sections: Hook → Explain the concept → How it works → Why it matters → Outro
- Outro always ends with: "That's IT GIRL explaining {topic['concept']}. If this clicked for you, subscribe — new tech concept every week. See you next time."
- No markdown formatting in the script itself, just plain text for TTS

Also return:
- A punchy YouTube title (max 60 chars)
- A YouTube description (150-200 words, includes relevant keywords naturally)
- 8-10 tags as a list

Return ONLY a JSON object, no markdown, no extra text:
{{
  "title": "...",
  "script": "...",
  "description": "...",
  "tags": ["tag1", "tag2", ...]
}}"""

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    import time, sys
    last_error = None
    for model in MODELS:
        print(f"  Trying model: {model}", flush=True)
        body = {
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 2000,
            "temperature": 0.7
        }
        for attempt in range(3):
            response = requests.post(FEATHERLESS_API_URL, headers=headers, json=body)
            if response.ok:
                break
            print(f"  Attempt {attempt+1} failed ({response.status_code}): {response.text[:200]}", flush=True)
            if response.status_code == 503:
                time.sleep(10)
            else:
                break
        if response.ok:
            break
        last_error = response
    else:
        last_error.raise_for_status()

    raw = response.json()["choices"][0]["message"]["content"].strip()

    # clean markdown fences if present
    if "```" in raw:
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    raw = raw.strip()

    result = json.loads(raw)
    return result


if __name__ == "__main__":
    with open("topics.json", "r") as f:
        topics = json.load(f)

    topic = topics[0]
    print(f"Generating script for: {topic['concept']}...")
    script_data = generate_script(topic)

    print("\n--- TITLE ---")
    print(script_data["title"])
    print("\n--- SCRIPT (first 300 chars) ---")
    print(script_data["script"][:300])
    print("\n--- TAGS ---")
    print(script_data["tags"])
