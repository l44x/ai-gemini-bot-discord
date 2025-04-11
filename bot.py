from discord import app_commands, Intents, Client, Interaction, Activity, ActivityType
import requests
import json

# Tokens
GEMINI_API_KEYS = [
    'YOU-API-KEY',
    'YOU-API-KEY',
    'YOU-API-KEY',
    'YOU-API-KEY'
]

# Model-Free-GeminiAI
url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"

class Bot(Client):
    def __init__(self, *, intents: Intents):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self) -> None:
        await self.tree.sync(guild=None)

bot = Bot(intents=Intents.default())

@bot.event
async def on_ready():
    await bot.change_presence(activity=Activity(type=ActivityType.playing, name="/help | Hexanot AI"))
    print(f"Logged in as {bot.user.name} - {bot.user.id}")
    print("Bot is ready!")

async def obtener_respuesta_google_ai(mensaje: str):
    for api_key in GEMINI_API_KEYS:  
        try:
            data = {
                "contents": [{
                    "parts": [{
                        "text": mensaje
                    }]
                }]
            }
            response = requests.post(url, params={'key': api_key}, headers={'Content-Type': 'application/json'}, data=json.dumps(data))

            if response.status_code == 200:
                response_data = response.json()
                ai_response = response_data['candidates'][0]['content']['parts'][0]['text']
                return ai_response
            else:
                print(f"Error con el token {api_key}: {response.status_code}, {response.text}")
        except Exception as e:
            print(f"Error con el token {api_key}: {str(e)}")
    return "No se pudo obtener una respuesta de la API de Google AI con ninguno de los tokens disponibles."

@bot.tree.command(name="googleai", description="Habla con Google AI Studio desde el bot.")
@app_commands.describe(mensaje="Mensaje que se enviará a Google AI Studio")
async def googleai(interaction: Interaction, mensaje: str):
    await interaction.response.defer()  
    try:
        respuesta = await obtener_respuesta_google_ai(mensaje)

        # Envía la respuesta fragmentada si es demasiado larga
        MAX_LENGTH = 1900
        partes = [respuesta[i:i+MAX_LENGTH] for i in range(0, len(respuesta), MAX_LENGTH)]
        await interaction.followup.send(f"💬 **Respuesta de Google AI Studio (Parte 1):**\n```\n{partes[0].strip()}\n```")
        for i, parte in enumerate(partes[1:], start=2):
            await interaction.followup.send(f"💬 **Respuesta de Google AI Studio (Parte {i}):**\n```\n{parte}\n```")
    except Exception as e:
        await interaction.followup.send(f"💬 Ha ocurrido un error: {str(e)}")


bot.run("<YOU-TOKEN>")
