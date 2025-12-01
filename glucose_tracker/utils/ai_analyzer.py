import base64
import json
import requests
from django.conf import settings
from django.utils.translation import gettext_lazy as _


def analyze_meal_image(image_file):
    """
    Analyzes a meal image using OpenAI GPT-4 Vision API.
    Returns a dictionary with description, calories, carbs, and components.
    """
    api_key = settings.OPENAI_API_KEY
    if not api_key:
        return {"error": _("OpenAI API key not configured.")}

    # Encode image to base64
    base64_image = base64.b64encode(image_file.read()).decode("utf-8")
    image_file.seek(0)  # Reset file pointer

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
        "model": "gpt-4-turbo",  # Or gpt-4o if available and preferred
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
