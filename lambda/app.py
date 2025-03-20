import os
import requests
import base64
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)

PROMPT_INICIAL = "Actúa como un chatbot en español y Shipibo, brindando recomendaciones sobre embarazo, prevención de enfermedades, cuidado prenatal, alimentación, higiene y vacunación. También puedes analizar imágenes médicas y brindar respuestas breves. Procura que tus respuestas a imágenes sean lo más concisas posibles."

historial_usuarios = {}

def encode(image_url):

    TWILIO_SID = os.getenv("TWILIO_ACCOUNT_SID")
    TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")

    try:
        response = requests.get(image_url, auth=(TWILIO_SID, TWILIO_AUTH_TOKEN))
        print(f"response.status_code: {response.status_code}")

        if response.status_code == 200:
            imagen_base64 = base64.b64encode(response.content).decode("utf-8")
            return f"data:image/jpeg;base64,{imagen_base64}"
        else:
            return f"Error: No se pudo descargar la imagen. Código {response.status_code}"
    except Exception as e:
        return f"Error en la descarga: {str(e)}"


def analize_image(user_id, image_url):

    imagen_base64 = encode(image_url)

    if not imagen_base64:
        return "Error: No se pudo descargar o procesar la imagen."

    try:

        if user_id not in historial_usuarios:
            historial_usuarios[user_id] = [{"role": "system", "content": PROMPT_INICIAL}]

        historial_usuarios[user_id].append({
            "role": "user",
            "content": [
                {"type": "text", "text": "Observa la imagen. Brinda una respuesta bastante breve por favor."},
                {"type": "image_url", "image_url": {"url": imagen_base64}}
            ]
        })

        response = openai.ChatCompletion.create(
            model="gpt-4-turbo",
            messages=historial_usuarios[user_id]
        )

        bot_response = response["choices"][0]["message"]["content"]
        historial_usuarios[user_id].append({"role": "assistant", "content": bot_response})

        print(bot_response)

        return bot_response
    
    except Exception as e:
        return f"Error al analizar la imagen: {str(e)}"

def get_response(user_id, user_message):

    if user_id not in historial_usuarios:
        historial_usuarios[user_id] = [{"role": "system", "content": PROMPT_INICIAL}]

    historial_usuarios[user_id].append({"role": "user", "content": user_message})

    response = openai.ChatCompletion.create(
        model="gpt-4-turbo",
        messages=historial_usuarios[user_id]
    )

    bot_response = response["choices"][0]["message"]["content"]
    historial_usuarios[user_id].append({"role": "assistant", "content": bot_response})

    return bot_response

def divide_message(mensaje, limite=320):
    parts = []
    while len(mensaje) > limite:
        cut = mensaje.rfind("\n", 0, limite)
        if cut == -1:
            cut = limite
        parts.append(mensaje[:cut])
        mensaje = mensaje[cut:].strip()
    parts.append(mensaje)
    return parts

@app.route("/webhook", methods=["POST"])
def webhook():
    user_id = request.values.get("From", "")
    incoming_msg = request.values.get("Body", "").strip()
    media_url = request.values.get("MediaUrl0", None)

    print(f"media_url: {media_url}")

    if media_url:
        response_text = analize_image(user_id, media_url)
    else:
        response_text = get_response(user_id, incoming_msg)
    
    print(response_text)
    resp = MessagingResponse()
    resp.message(response_text)
    return str(resp)


# AWS Lambda adaptation
from mangum import Mangum
lambda_handler = Mangum(app)

# Instead of...

# if __name__ == "__main__":
#     app.run(port=5000, debug=True)
