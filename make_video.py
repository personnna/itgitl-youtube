from moviepy import (
    ImageClip, AudioFileClip, concatenate_videoclips,
    CompositeVideoClip, TextClip, ColorClip
)
from moviepy.video.fx import FadeIn, FadeOut
import os

VIDEO_SIZE = (1920, 1080)
FPS = 24


def make_video(
    image_paths: list,
    audio_path: str,
    title: str,
    output_path: str = "output.mp4"
) -> str:
    print("🎬 Loading audio...")
    audio = AudioFileClip(audio_path)
    total_duration = audio.duration

    time_per_image = total_duration / len(image_paths)

    print(f"🎬 Building {len(image_paths)} image clips ({time_per_image:.1f}s each)...")
    clips = []

    for i, img_path in enumerate(image_paths):
        clip = (
            ImageClip(img_path)
            .with_duration(time_per_image)
            .resized(VIDEO_SIZE)
        )
        if i > 0:
            clip = clip.with_effects([FadeIn(0.5)])
        if i < len(image_paths) - 1:
            clip = clip.with_effects([FadeOut(0.5)])
        clips.append(clip)

    video = concatenate_videoclips(clips, method="compose")

    print("🎬 Rendering...")
    final = video.with_audio(audio)
    final.write_videofile(
        output_path,
        fps=FPS,
        codec="libx264",
        audio_codec="aac",
        logger=None
    )

    print(f"✅ Video saved: {output_path}")
    return output_path
