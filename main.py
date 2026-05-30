import json
import os
import shutil
from pathlib import Path
from dotenv import load_dotenv

from generate_script import generate_script
from tts import text_to_speech
from fetch_images import fetch_images
from make_video import make_video
from upload import upload_video

load_dotenv()

TOPICS_FILE = "topics.json"
PROGRESS_FILE = "progress.json"   # tracks which topic is next
OUTPUT_DIR = "output"


def load_topics() -> list[dict]:
    with open(TOPICS_FILE, "r") as f:
        return json.load(f)


def get_next_topic(topics: list[dict]) -> tuple[int, dict]:
    """Returns (index, topic) for the next topic to process."""
    progress = {}
    if os.path.exists(PROGRESS_FILE):
        with open(PROGRESS_FILE, "r") as f:
            progress = json.load(f)

    next_index = progress.get("next_index", 0)

    # wrap around if we've done all topics
    if next_index >= len(topics):
        next_index = 0

    return next_index, topics[next_index]


def save_progress(next_index: int):
    with open(PROGRESS_FILE, "w") as f:
        json.dump({"next_index": next_index}, f)


def cleanup_temp_files():
    """Remove temp files after upload."""
    for f in ["audio.mp3", "temp_audio.m4a"]:
        if os.path.exists(f):
            os.remove(f)
    if os.path.exists("images"):
        shutil.rmtree("images")


def run():
    print("🌸 IT GIRL YouTube Pipeline — Starting\n")

    Path(OUTPUT_DIR).mkdir(exist_ok=True)

    # 1. pick next topic
    topics = load_topics()
    index, topic = get_next_topic(topics)
    print(f"📌 Topic #{topic['id']}: {topic['concept']}\n")

    # 2. generate script with Claude
    print("✍️  Generating script...")
    script_data = generate_script(topic)
    print(f"   Title: {script_data['title']}")

    # 3. text to speech
    print("\n🎙️  Converting to audio...")
    audio_path = text_to_speech(script_data["script"], "audio.mp3")

    # 4. fetch images
    print("\n🖼️  Fetching images...")
    image_paths = fetch_images(topic, count=6)

    # 5. make video
    print("\n🎬  Assembling video...")
    video_path = os.path.join(OUTPUT_DIR, f"video_{topic['id']}.mp4")
    make_video(image_paths, audio_path, script_data["title"], video_path)

    # 6. upload to YouTube
    print("\n📤  Uploading to YouTube...")
    video_id = upload_video(
        video_path=video_path,
        title=script_data["title"],
        description=script_data["description"],
        tags=script_data["tags"] + ["IT GIRL", "tech explained", "developer"],
        privacy="public"
    )

    # 7. save progress
    save_progress(index + 1)

    # 8. cleanup
    cleanup_temp_files()

    print(f"\n✅ Done! Video live: https://youtube.com/watch?v={video_id}")
    print(f"   Next up: Topic #{topics[index + 1]['id'] if index + 1 < len(topics) else 1}")


if __name__ == "__main__":
    run()
