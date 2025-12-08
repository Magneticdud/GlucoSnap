import base64
import json
import requests
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from PIL import Image
import io


def analyze_meal_image(image_file):
    """
    Analyzes a meal image using OpenAI GPT-5.1 Vision API.
    Returns a dictionary with description, calories, carbs, and components.
    """
    api_key = settings.OPENAI_API_KEY
    if not api_key:
        return {"error": _("OpenAI API key not configured.")}

    # Downsample image to 2 megapixels (approx 1600x1200) to reduce token usage
    try:
        # Read the original image
        img = Image.open(image_file)

        # Calculate target dimensions for 2 megapixels (maintaining aspect ratio)
        target_megapixels = 2.0
        original_width, original_height = img.size
        original_aspect = original_width / original_height
        target_width = int((target_megapixels * 1e6 * original_aspect) ** 0.5)
        target_height = int((target_megapixels * 1e6) / target_width)

        # Resize the image using high-quality downsampling
        if original_width > target_width or original_height > target_height:
            img = img.resize((target_width, target_height), Image.Resampling.LANCZOS)

        # Convert to JPEG format with good quality
        output_buffer = io.BytesIO()
        img.save(output_buffer, format='JPEG', quality=85, optimize=True)
        output_buffer.seek(0)

        # Encode the downsized image to base64
        base64_image = base64.b64encode(output_buffer.read()).decode("utf-8")
        output_buffer.seek(0)

    except Exception as e:
        # Fallback to original image if downsizing fails
        base64_image = base64.b64encode(image_file.read()).decode("utf-8")
        image_file.seek(0)

    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"}

    prompt_text = """
    Analyze this food photo and provide:
    1. Detailed description of the meal
    2. Estimated total calories (kcal)
    3. Estimated carbohydrates (grams)
    4. Main components list
    Format as JSON: {description, calories, carbs, components[]}
    """

    payload = {
        "model": "gpt-5.1",  # Updated to GPT-5.1 model
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt_text},
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"},
                    },
                ],
            }
        ],
        "max_tokens": 500,
        "response_format": {"type": "json_object"},
    }

    try:
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=30,
        )
        response.raise_for_status()
        result = response.json()

        content = result["choices"][0]["message"]["content"]
        parsed_content = json.loads(content)

        return parsed_content

    except requests.exceptions.RequestException as e:
        return {"error": f"API Error: {str(e)}"}
    except json.JSONDecodeError:
        return {"error": "Failed to parse AI response."}
    except Exception as e:
        return {"error": f"Unexpected error: {str(e)}"}
