from moviepy.editor import (
    ImageClip, AudioFileClip, concatenate_videoclips,
    CompositeVideoClip, TextClip, ColorClip
)
from moviepy.video.fx.fadein import fadein
from moviepy.video.fx.fadeout import fadeout
import os


# IT GIRL brand colors
PINK = (242, 196, 208)       # #F2C4D0 blush
BLACK = (13, 13, 13)         # #0D0D0D noir
WHITE = (255, 255, 255)

VIDEO_SIZE = (1920, 1080)    # 1080p landscape for YouTube
FPS = 24


def make_video(
    image_paths: list[str],
    audio_path: str,
    title: str,
    output_path: str = "output.mp4"
) -> str:
    """
    Assembles a video from images + audio with IT GIRL branding.
    Images cycle through for the duration of the audio.
    """
    print("🎬 Loading audio...")
    audio = AudioFileClip(audio_path)
    total_duration = audio.duration

    # time per image (cycle through images evenly)
    time_per_image = total_duration / len(image_paths)

    print(f"🎬 Building {len(image_paths)} image clips ({time_per_image:.1f}s each)...")
    clips = []

    for i, img_path in enumerate(image_paths):
        clip = (
            ImageClip(img_path)
            .set_duration(time_per_image)
            .resize(VIDEO_SIZE)
        )

        # subtle fade between images
        if i > 0:
            clip = clip.fx(fadein, duration=0.5)
        if i < len(image_paths) - 1:
            clip = clip.fx(fadeout, duration=0.5)

        clips.append(clip)

    # concatenate all image clips
    video = concatenate_videoclips(clips, method="compose")

    # add semi-transparent brand overlay at bottom
    overlay_height = 80
    overlay = (
        ColorClip(size=(VIDEO_SIZE[0], overlay_height), color=BLACK)
        .set_opacity(0.55)
        .set_position(("left", VIDEO_SIZE[1] - overlay_height))
        .set_duration(total_duration)
    )

    # brand label bottom left
    brand_text = (
        TextClip(
            "IT GIRL",
            fontsize=28,
            color="white",
            font="Helvetica-Bold",
            kerning=4
        )
        .set_position((40, VIDEO_SIZE[1] - 55))
        .set_duration(total_duration)
    )

    # assemble final video
    print("🎬 Compositing...")
    final = CompositeVideoClip([video, overlay, brand_text])
    final = final.set_audio(audio)

    print(f"🎬 Rendering to {output_path}...")
    final.write_videofile(
        output_path,
        fps=FPS,
        codec="libx264",
        audio_codec="aac",
        temp_audiofile="temp_audio.m4a",
        remove_temp=True,
        logger=None  # suppress verbose output
    )

    print(f"✅ Video saved: {output_path}")
    return output_path


if __name__ == "__main__":
    # quick test — needs real images and audio
    import glob
    images = sorted(glob.glob("images/*.jpg"))
    if images and os.path.exists("audio.mp3"):
        make_video(images, "audio.mp3", "Docker Explained", "test_output.mp4")
    else:
        print("Run fetch_images.py and tts.py first to generate test files.")
