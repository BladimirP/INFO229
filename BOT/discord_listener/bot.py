import os

import discord
from dotenv import load_dotenv
from discord.ext import commands
import threading
import pika
import random
import time


time.sleep(5)
############ CONEXION RABBITMQ ##############

HOST = os.environ['RABBITMQ_HOST']
print("rabbit:"+HOST)

connection = pika.BlockingConnection(pika.ConnectionParameters(host=HOST))

channelMQ = connection.channel()

#Creamos el exchange 'cartero' de tipo 'fanout'
channelMQ.exchange_declare(exchange='cartero', exchange_type='topic', durable=True)

#############################################

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

# Globales
bot = commands.Bot(command_prefix='!')
hp_actual = 0
hp_maximo = 0
is_active = False
cebo = 0
cont_atrapados = 0
cont_huidos = 0
cont_debilitados = 0
cont_pokeball = 0
pokemon = []


@bot.event
async def on_ready():
    for guild in bot.guilds:
        if guild.name == GUILD:
            break

    print(
        f'{bot.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})\n'
    )

    members = '\n - '.join([member.name for member in guild.members])
    print(f'Guild Members:\n - {members}')

    for channel in bot.get_all_channels():
        print(channel)
        print(channel.id)

    channel = bot.get_channel(908505071887732768)
    await channel.send('¡¡¡Sean bienvenidos a la Zona Safari!!!')


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    await bot.process_commands(message)

@bot.command(name='safari', help='Caminas en la zona safari hasta encontrar un pokémon salvaje. Ejemplo: !safari')
async def poke(ctx):
    global is_active
    if not (is_active):
        is_active = True

        message =  ctx.message.content
        print("send a new mesage to rabbitmq: "+message)

        channelMQ.basic_publish(exchange='cartero', routing_key="cola", body=message)

    else :
        e = discord.Embed(	title="¡No puedes seguir. Un {p} salvaje te esta bloqueando el camino!".format(p = pokemon[0]),
                      		description="HP: {a}/{h}".format(a= hp_actual, h = hp_maximo))
        e.set_thumbnail(url="{u}".format(u = pokemon[1]))
        await ctx.send(embed=e)
    
@bot.command(name="roca", help='Lanzas una roca dañando al pokémon y haciendolo mas facil de capturar')
async def poke(ctx):
    global is_active
    global hp_maximo
    global hp_actual
    global cebo
    global pokemon
    global cont_huidos
    global cont_debilitados
    if(not is_active):
        await ctx.send("Haz lanzado una roca, pero no habia nadie a quien golpear.")
    else:
        dmg = random.randint(3,9)
        if (hp_actual - dmg <= 0):
            cont_debilitados += 1
            is_active = False
            await ctx.send("Haz lanzado una roca a {n}, ha perdido {d} de HP y se ha debilitado.".format(n=pokemon[0], d=dmg))
        elif (cebo + ((hp_actual - dmg ) / hp_maximo) * 100 <= random.randint(1,100) ):
            cont_huidos += 1
            is_active = False
            await ctx.send("Haz lanzado una roca al Pokémon, pero lo has espantado y ha huido.")
        else:
            hp_actual = hp_actual - dmg
            e = discord.Embed(title = "Haz lanzado una roca a {n}, ha perdido {d} de HP".format(n = pokemon[0], d = dmg), description="HP: {a}/{h}".format(a = hp_actual,h = hp_maximo))
            e.set_thumbnail(url="{u}".format(u = pokemon[1]))
            await ctx.send(embed=e)

@bot.command(name="cebo", help='Lanzas comida al pokémon curandolo y haciendo que sea mas difícil que escape.')
async def poke(ctx):
    global is_active
    global hp_maximo
    global hp_actual
    global cebo
    global pokemon
    print("El hp maximo es {n}".format(n= hp_maximo))
    if (not is_active):
        await ctx.send("No hay a quien lanzarle cebo, no desperdicies la comida.")
    else:
        bait = random.randint(3,9)
        cebo = cebo + bait
        if (hp_actual + bait >= hp_maximo):
            bait = hp_maximo - hp_actual
        hp_actual = hp_actual + bait
        e = discord.Embed(title="Haz lanzado un poco de cebo a {n}, ha restaurado {b} de HP".format(n=pokemon[0], b=bait), description = "HP: {a}/{h}".format(a = hp_actual, h=hp_maximo))
        e.set_thumbnail(url="{u}".format(u = pokemon[1]))
        await ctx.send(embed=e)

@bot.command(name="pokeball", help='Lanzas una pokeball intentado capturar al pokémon')
async def poke(ctx):
    global is_active
    global hp_maximo
    global hp_actual
    global cebo
    global pokemon
    global cont_pokeball
    global cont_atrapados
    if (not is_active):
        await ctx.send("No hay nadie a quien capturar.")
    elif ( cebo + hp_actual/hp_maximo*100 <= random.randint(1,100) ):
        is_active = False
        await ctx.send("Haz lanzado una Safari Ball... pero {n} se ha liberado y ha HUIDO.".format(n = pokemon[0]))
        cont_pokeball += 1
    elif ( cebo + hp_actual/hp_maximo*100 <= random.randint(1,100) + 10 ):
        is_active = False
        cont_atrapados += 1
        cont_pokeball += 1
        e = discord.Embed(title="Haz lanzado una Safari Ball a {n}... ha sido CAPTURADO!".format(n=pokemon[0]), description = "Los datos de {n} se han enviado al Profesor Vernier.".format(n=pokemon[0]))
        e.set_thumbnail(url="https://images.wikidexcdn.net/mwuploads/wikidex/thumb/a/ac/latest/20090125150731/Safari_Ball_%28Ilustraci%C3%B3n%29.png/225px-Safari_Ball_%28Ilustraci%C3%B3n%29.png")
        await ctx.send(embed=e)
    else:
        cont_pokeball += 1
        e = discord.Embed(title="Haz lanzado una Safari Ball... pero {n} se ha liberado.".format(n=pokemon[0]), description = "HP: {a}/{h}".format(a = hp_actual, h=hp_maximo))
        e.set_thumbnail(url=pokemon[1])
        await ctx.send(embed=e)

@bot.command(name="huir", help="Realizas una maniobra de escape, para perder al pokémon")
async def poke(ctx):
    global is_active
    global pokemon
    global cont_huidos
    if(not is_active):
        await ctx.send("No hay ningun Pokemón del cual huir. Y tristemente no puedes huir de tus responsabilidades")
    else:
        is_active=False
        cont_huidos += 1
        await ctx.send("¡Haz logrado huir exitosamente de {n}. Sigue con tu aventura por la Zona Safari!".format(n = pokemon[0]))

@bot.command(name='profesor', help='Muestra tus estadisticas')
async def poke(ctx):
    global cont_atrapados
    global cont_huidos
    global cont_debilitados
    global cont_pokeball
    total = cont_atrapados+cont_huidos+cont_debilitados
    if (total == 0):
        e = discord.Embed(  title="Hola soy el profesor Vernier y no tengo estadisticas para mostrar", 
                            description = "Sigue tu viaje por la zona zafari")
        e.set_thumbnail(url="https://i.imgur.com/zmlKtko.jpg")
        await ctx.send(embed=e)
    else:
        e = discord.Embed(  title="Hola soy el profesor Vernier y tus estadisticas son:", 
                            description = "Te has escontrado con: {a} pokémon(s)\nHas capturado: {c}\n Han escapado: {e}\n Has debilitado: {d}\n tu ratio de captura es de {p}%".format(a = total, c=cont_atrapados, e=cont_huidos, d=cont_debilitados, p=(cont_atrapados/total)*100))
        e.set_thumbnail(url="https://i.imgur.com/zmlKtko.jpg")
        await ctx.send(embed=e)


@bot.command(name='add-pokemon', help='Permite añadir un nuevo pokemon al safari. Ejemplo: !add-pokemon aron url_imagen 50')
async def poke(ctx):
    message =  ctx.message.content
    name = message.split(" ")
    print("send a new mesage to rabbitmq: "+message)
    channelMQ.basic_publish(exchange='cartero', routing_key="cola", body=message)
    await ctx.send("Los datos de {nom} se han añadido a la Pokedex.".format(nom = name[1]))

############ CONSUMER ###############

import threading
import asyncio

def writer(bot):
    """thread worker function"""
    print('Worker')

    HOST = os.environ['RABBITMQ_HOST']

    connection = pika.BlockingConnection(pika.ConnectionParameters(host=HOST))
    channelMQ = connection.channel()

    channelMQ.exchange_declare(exchange='cartero', exchange_type='topic', durable=True)

    result = channelMQ.queue_declare(queue="discord_writer", exclusive=True, durable=True)
    queue_name = result.method.queue

    channelMQ.queue_bind(exchange='cartero', queue=queue_name, routing_key="discord_writer")

    print(' [*] Waiting for messages. To exit press CTRL+C')

    async def write(message):
        channel = bot.get_channel(908505071887732768)
        message = message.split(' ')
        
        global pokemon
        global hp_actual
        global hp_maximo
        global cebo

        pokemon = [message[0],message[1]]
        hp_maximo = int(float(message[2]))
        hp_actual = hp_maximo
        cebo = 0

        e = discord.Embed(	title="¡Ha aparecido un {p} salvaje!".format(p = message[0]),
                      		description="HP: {a}/{h}".format(a= hp_actual, h = hp_maximo))
        e.set_thumbnail(url="{u}".format(u = message[1]))
        await channel.send(embed=e)

    
    def callback(ch, method, properties, body):
        message=body.decode("UTF-8")
        print(message)

        bot.loop.create_task(write(message))

    channelMQ.basic_consume(
        queue=queue_name, on_message_callback=callback, auto_ack=True)

    channelMQ.start_consuming()

t = threading.Thread(target=writer, args=[bot])
t.start()

########################################
bot.run(TOKEN)