import asyncio
import edge_tts
import os


# Nice female English voices for IT GIRL vibe
# Options: "en-US-JennyNeural", "en-US-AriaNeural", "en-GB-SoniaNeural"
VOICE = "en-US-AriaNeural"
RATE = "+0%"    # speech speed, can do +10% to speed up slightly
PITCH = "+0Hz"  # voice pitch


async def _synthesize(text: str, output_path: str):
    communicate = edge_tts.Communicate(text, VOICE, rate=RATE, pitch=PITCH)
    await communicate.save(output_path)


def text_to_speech(script: str, output_path: str = "audio.mp3") -> str:
    """
    Convert script text to mp3 audio.
    Returns path to the audio file.
    """
    asyncio.run(_synthesize(script, output_path))
    print(f"✅ Audio saved: {output_path}")
    return output_path


if __name__ == "__main__":
    test_text = """Hey, have you ever wondered why developers keep talking about Docker? 
    Like, what even is a container? Today I'm going to explain it using something 
    we all understand — a makeup bag. Trust me, it will click instantly."""

    text_to_speech(test_text, "test_audio.mp3")
    print(f"File size: {os.path.getsize('test_audio.mp3')} bytes")
