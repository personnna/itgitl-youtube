# IT GIRL YouTube Pipeline 🌸💻

Automated YouTube channel that explains tech concepts simply, with girly analogies.
Posts one video every day at 09:00 UTC. Fully autonomous.

## Stack
- **Claude Haiku** — writes the script (~$0.02/video)
- **Edge-TTS** — free text-to-speech (AriaNeural voice)
- **Pexels API** — free stock images
- **MoviePy + ffmpeg** — assembles the video
- **YouTube Data API v3** — uploads automatically
- **GitHub Actions** — runs the whole thing daily

---

## Setup

### 1. Clone and install
```bash
git clone https://github.com/yourusername/itgirl-youtube
cd itgirl-youtube
pip install -r requirements.txt
```

### 2. Get your API keys

| Key | Where to get |
|-----|-------------|
| `ANTHROPIC_API_KEY` | console.anthropic.com |
| `PEXELS_API_KEY` | pexels.com/api (free) |
| YouTube OAuth | Google Cloud Console |

### 3. YouTube OAuth setup
1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Create a project → Enable **YouTube Data API v3**
3. Create OAuth 2.0 credentials → Download as `client_secrets.json`
4. Run once locally to generate token:
```bash
python upload.py
```
This opens a browser for auth and saves `token.pickle`.

### 4. Add GitHub Secrets
In your repo → Settings → Secrets → Actions:

```
ANTHROPIC_API_KEY    → your Anthropic key
PEXELS_API_KEY       → your Pexels key
YOUTUBE_CLIENT_SECRETS → contents of client_secrets.json
YOUTUBE_TOKEN        → contents of token.pickle (base64 if needed)
```

### 5. Test locally
```bash
python main.py
```

### 6. Push to GitHub
GitHub Actions will run every day at 09:00 UTC automatically.
You can also trigger manually from the Actions tab.

---

## Project Structure
```
itgirl-youtube/
├── main.py              # orchestrates everything
├── generate_script.py   # Claude writes the script
├── tts.py               # Edge-TTS converts to audio
├── fetch_images.py      # Pexels downloads images
├── make_video.py        # MoviePy assembles video
├── upload.py            # YouTube API uploads
├── topics.json          # 100 tech topics
├── progress.json        # tracks which topic is next (auto-updated)
├── requirements.txt
└── .github/
    └── workflows/
        └── daily.yml    # cron job
```

---

## Cost estimate
- Claude Haiku: ~$0.02 per video
- Everything else: free
- **$100 in credits = ~5000 videos = 13+ years of daily content**
