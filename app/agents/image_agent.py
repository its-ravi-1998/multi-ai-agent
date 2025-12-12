from huggingface_hub import InferenceClient
import os
from io import BytesIO
import base64

client = InferenceClient(
    model="black-forest-labs/FLUX.1-schnell",
    token=os.getenv("HF_TOKEN", "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")
)


async def image_agent(raw_input: str) -> str:
    """Generate image from text prompt using Hugging Face Inference API."""
    try:
        # Generate image from prompt
        image = client.text_to_image(raw_input)
        
        # Convert image to base64 string for API response
        buffer = BytesIO()
        image.save(buffer, format="PNG")
        image_bytes = buffer.getvalue()
        image_base64 = base64.b64encode(image_bytes).decode("utf-8")
        
        return f"Image generated successfully. Base64 encoded image (first 100 chars): {image_base64[:100]}..."
    except Exception as e:
        return f"Error generating image: {str(e)}"
