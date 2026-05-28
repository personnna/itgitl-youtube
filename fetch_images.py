import requests
import os
from pathlib import Path


IMAGES_DIR = "images"

# Pixabay — completely free, no card needed
# Get key at: https://pixabay.com/api/docs/ (instant, free)
PIXABAY_API_URL = "https://pixabay.com/api/"


def fetch_images(topic: dict, count: int = 6) -> list[str]:
    """
    Fetch relevant images from Pixabay for a given topic.
    Returns list of local image file paths.
    """
    Path(IMAGES_DIR).mkdir(exist_ok=True)

    api_key = os.environ["PIXABAY_API_KEY"]

    # build search query
    query = topic["concept"] + " " + " ".join(topic["tags"][:2])

    params = {
        "key": api_key,
        "q": query,
        "image_type": "photo",
        "orientation": "horizontal",
        "category": "science,technology,computer",
        "per_page": count,
        "safesearch": "true"
    }

    response = requests.get(PIXABAY_API_URL, params=params)
    response.raise_for_status()
    data = response.json()

    hits = data.get("hits", [])

    # fallback to generic tech query if no results
    if not hits:
        params["q"] = "technology computer programming"
        params.pop("category", None)
        response = requests.get(PIXABAY_API_URL, params=params)
        data = response.json()
        hits = data.get("hits", [])

    image_paths = []
    for i, photo in enumerate(hits[:count]):
        img_url = photo["largeImageURL"]
        img_path = os.path.join(IMAGES_DIR, f"img_{i}.jpg")

        img_response = requests.get(img_url)
        with open(img_path, "wb") as f:
            f.write(img_response.content)

        image_paths.append(img_path)
        print(f"  📸 Downloaded image {i+1}/{min(count, len(hits))}")

    print(f"✅ {len(image_paths)} images saved to /{IMAGES_DIR}")
    return image_paths


if __name__ == "__main__":
    topic = {
        "concept": "Docker",
        "tags": ["docker", "devops", "containers"]
    }
    paths = fetch_images(topic)
    print(paths)
