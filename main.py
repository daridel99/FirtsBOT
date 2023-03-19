import os
import discord
from io import BytesIO
from dotenv import load_dotenv
from PIL import Image
import numpy as np
from tensorflow.keras.applications.resnet50 import ResNet50
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.resnet50 import preprocess_input, decode_predictions

load_dotenv()
token = os.environ['Token']


class MyClient(discord.Client):

  async def on_ready(self):
    print(f'{client.user} has connected to Discord!')
    print('Logged on as', self.user)

  async def on_message(self, message):
    #print(message.content)
    # don't respond to ourselves
    if message.author == self.user:
      return

    if message.content == 'comocchi':
      await message.channel.send(
        'https://cdn.discordapp.com/attachments/1078783779885305886/1086799919282667622/Bocchi-the-Rock-350x250.jpg'
      )

    if message.content == 'ah':
      await message.channel.send(
        'https://cdn.discordapp.com/attachments/1078783779885305886/1086803916538253412/bochi_manga.jpg'
      )

    if len(message.attachments) > 0:
      # Cargar la red neuronal pre-entrenada ResNet50
      model = ResNet50(weights='imagenet')
      for attachment in message.attachments:
        if attachment.content_type.startswith('image'):
          image_data = await attachment.read()
          with Image.open(BytesIO(image_data)) as img:
            # Redimensionar la imagen para que tenga un tamaño adecuado para la CNN
            img = img.resize((224, 224))
            # Preprocesar la imagen para que sea compatible con la CNN
            x = preprocess_input(np.array(img, dtype=np.float32))
            # Hacer la predicción con la CNN
            x_ = image.img_to_array(x)
            preds = model.predict(np.array([x_]))
            # Decodificar las predicciones y obtener la etiqueta con mayor probabilidad
            label = decode_predictions(preds, top=3)
            # Verificar si la etiqueta se refiere a comida
            await message.channel.send(
              f"Comocchi esta comiendo {label}, @OneTapKevs#9961 y @cvtvlinv#0535"
            )


intents = discord.Intents.default()
intents.message_content = True
client = MyClient(intents=intents)
client.run(token)