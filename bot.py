from bot_token import TOKEN
import disnake as discord
from disnake.ext import commands
import tensorflow as tf
from tensorflow import keras
import numpy as np

intents = discord.Intents.all()
bot = commands.Bot(intents=intents, command_prefix='$')

model = keras.models.load_model('./mental_health_status.h5')

@bot.event
async def on_ready():
    print(f'{bot.user} is now running')

@bot.command()
async def predict(ctx):
    try:
        await ctx.send('React to each of the following questions')
        paramters = []
        reactions = ['✅', '❌']

        with open('questions.txt', 'r') as file:
            questions = file.readlines()

        for question in questions:
            message = await ctx.send(question)
            for reaction in reactions:
                await message.add_reaction(reaction)

            def check(reaction, user):
                return user == ctx.author and str(reaction.emoji) in reactions and reaction.message == message

            reaction, user = await bot.wait_for('reaction_add', check=check)
            if str(reaction.emoji) == '✅':
                paramters.append(1)
            else:
                paramters.append(0)
            
            # print(paramters)

        paramters = np.array(paramters).reshape(1, -1)
        prediction = model.predict(paramters).argmax(axis=1)[0]
        # print('Prediction ' + str(prediction))
        
        diagnosis = ''
        if prediction == 0:
            diagnosis = 'Anxiety'
        elif prediction == 1:
            diagnosis = 'Depression'
        elif prediction == 2:
            diagnosis = 'Lonliness'
        elif prediction == 3:
            diagnosis = 'Normal'
        elif prediction == 4:
            diagnosis = 'Stress'
        await ctx.send(f'You may have the following: {diagnosis}')
    except Exception as e:
        print(e)

bot.run(TOKEN)