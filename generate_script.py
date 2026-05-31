import json
import os
import requests

GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"


def generate_script(topic: dict) -> dict:
    """
    Takes a topic dict and returns a full video script.
    Uses Featherless AI (OpenAI-compatible, free credits).
    """
    api_key = os.environ["GEMINI_API_KEY"]

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

    body = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"temperature": 0.7, "maxOutputTokens": 2000}
    }

    response = requests.post(
        f"{GEMINI_API_URL}?key={api_key}",
        headers={"Content-Type": "application/json"},
        json=body
    )
    if not response.ok:
        print(f"Gemini error {response.status_code}: {response.text}", flush=True)
    response.raise_for_status()

    raw = response.json()["candidates"][0]["content"]["parts"][0]["text"].strip()

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
