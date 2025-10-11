from google import genai
from google.genai import types
from PIL import Image
from io import BytesIO
import os, uuid, dotenv

dotenv.load_dotenv()


def generate_product_description(product_name: str, product_description: str):
    system_prompt = f"""
    Eres un experto en redacción publicitaria y marketing digital especializado en e-commerce.

    Tu tarea es crear descripciones de productos irresistibles a partir de un nombre y una breve descripción que recibirás como entrada.

    Instrucciones:
    - Genera una descripción comercial atractiva, convincente y profesional, optimizada para venta en línea.
    - Enfócate en los beneficios del producto (no solo en las características).
    - Usa un tono emocional, cercano y persuasivo, pero natural (sin exagerar).
    - Incluye una breve introducción que capture la atención, una explicación de valor y un llamado a la acción final.
    - Mantén la descripción entre 100 y 150 palabras.
    - Responde exclusivamente en formato JSON, siguiendo esta estructura exacta:

    {{
      "productName": "[nombre del producto]",
      "productDescription": "[texto generado]"
    }}

    Entrada del usuario:
    Nombre: {product_name}
    Descripción corta: {product_description}

    Ejemplo de salida:
    {{
      "productName": "SmartBottle Pro",
      "productDescription": "Mantente hidratado con estilo gracias a la SmartBottle Pro, la botella inteligente que cuida de ti. Su sensor integrado registra cada sorbo y se sincroniza con tu app móvil para recordarte cuándo beber más agua. Fabricada con materiales ecológicos y diseño elegante, SmartBottle Pro combina salud, tecnología y comodidad. ¡Convierte la hidratación en un hábito inteligente hoy mismo!"
    }}
    """

    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[system_prompt],
    )
    return response.text


def generate_image(product_name: str, product_description: str):
    system_prompt = f"Genera una imagen de {product_name} que refleje su descripción: {product_description}"
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
    response = client.models.generate_content(
        model="gemini-2.5-flash-image-preview",
        contents=[system_prompt],
    )
    filename = f"generated_{uuid.uuid4().hex}.png"
    image_path = f"static/{filename}"
    for part in response.candidates[0].content.parts:
        if part.text is not None:
            print(part.text)
        elif part.inline_data is not None:
            image = Image.open(BytesIO(part.inline_data.data))
            image.save(image_path)
    image_url = f"http://localhost:8000/static/{filename}"
    return image_url
