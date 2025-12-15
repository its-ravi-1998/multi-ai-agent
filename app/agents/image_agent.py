from huggingface_hub import InferenceClient
from io import BytesIO
import base64
from pathlib import Path
from datetime import datetime
from app.config import Settings

# Instantiate settings to read HF token from environment/.env
settings = Settings()

client = InferenceClient(
    model="black-forest-labs/FLUX.1-schnell",
    token=settings.HF_TOKEN,
)


async def image_agent(raw_input: str) -> str:
    """Generate an image from the prompt, save it to disk, and return info."""
    try:
        image = client.text_to_image(raw_input)

        # Save to outputs/images/
        output_dir = Path("outputs/images")
        output_dir.mkdir(parents=True, exist_ok=True)
        filename = f"image_{datetime.utcnow().strftime('%Y%m%d_%H%M%S_%f')}.png"
        file_path = output_dir / filename
        image.save(file_path, format="PNG")

        # Also prepare a short base64 preview
        buffer = BytesIO()
        image.save(buffer, format="PNG")
        image_bytes = buffer.getvalue()
        image_base64 = base64.b64encode(image_bytes).decode("utf-8")

        return (
            f"Image saved at {file_path.resolve()}. "
            f"Preview (first 100 chars base64): {image_base64[:100]}..."
        )
    except Exception as e:
        return f"Error generating image: {str(e)}"
