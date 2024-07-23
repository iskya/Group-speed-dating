import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from discord.ext.commands import Bot
import random
import asyncio

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('GUILD')

class SpeedDatingPool():
    def __init__(self, participants=[]):
        self.participants = participants
        self.ended = True # set to true when speed dating game is ended
        self.channels = []
        self.rounds = None
        self.interval = None
        self.main_channel = None
        self.group_size = None
    
    def reset_pool(self):
        self.participants = []
        self.ended = True
        self.channels = []
        self.rounds = None
        self.interval = None
        self.main_channel = None
    
    def remove_member(self, user):
        if not user:
            return False
    
        for i in range(len(self.participants)):
            if user == self.participants[i]:
                self.participants.pop(i)
                return True
        
        return False
    
    def add_member(self, user):
        if not user:
            return False
        elif user in self.participants:
            return False # user was already in pool
        else:
            self.participants.append(user)
            return True

#IMPORTANT GLOBAL VARIABLES

intents = discord.Intents.default()
intents.message_content = True



pool = SpeedDatingPool()

bot = Bot(command_prefix='!',intents=intents)

''' Bot command: Gets the number of members in a given Voice Channel id.
'''
@bot.command(name='members', help='Número de miembros en el canal con dicho ID')

async def get_members(ctx, channel_id=None):
    if not channel_id:
        await ctx.send('Especifique qué canal desea consultar')
    else:
        channel = bot.get_channel(int(channel_id))
        if not channel:
            await ctx.send('El canal no existe')
            return
        members = channel.members
        await ctx.send('Miembros de este canal: ' + str(len(members)))

''' Bot command: Sends a list of the participants registered in the current game.
'''
@bot.command(name='participants', help='Lista de los participantes en el juego')

async def get_participants(ctx):
    if pool.ended:
        await ctx.send('No hay juego en curso')
        return
    p_string = ''
    for i, p in enumerate(pool.participants):
        if i == len(pool.participants) - 1:
            p_string += p.name
        else:
            p_string += p.name + ', '
    await ctx.send(f'Participantes: {p_string}')

''' Bot command: begins a speed dating group shuffle.
'''
@bot.command(name='begin', help='Inicia el juego con los usuarios del canal de voz especificado (por ID).')

async def begin_shuffle(ctx, channel_id=None):
    # command author + channel
    author = ctx.message.author
    command_channel = ctx.message.channel

    # initialize
    pool.ended = False

    if not channel_id:
        await ctx.send('Por favor, especifica en qué canal te gustaría iniciar el grupo.')
        return
    channel = bot.get_channel(int(channel_id))
    if not channel:
        await ctx.send('El canal no existe')
        return
    pool.main_channel = channel
    pool.participants = channel.members
    
    if not pool_is_valid():
        await ctx.send('Lo siento, se necesitan 4 o más personas para jugar')
        pool.reset_pool() # just in case
        return

# Esperar que el usuario especifique el tamaño del grupo
    await ctx.send('Indique el tamaño del grupo (mínimo 2):')

    def check(m):
        return m.author == author and m.channel == command_channel and m.content.isdigit() and int(m.content) >= 2

    try:
        msg = await bot.wait_for('message', check=check, timeout=60.0)  # Esperar por 60 segundos máximo
        group_size = int(msg.content)
    except asyncio.TimeoutError:
        await ctx.send('Has tardado demasiado en especificar el tamaño del grupo. Configuración del juego cancelada.')
        return
    except ValueError:
        await ctx.send('Entrada no válida. Por favor, especifique un número (mínimo 2). Configuración del juego cancelada.')
        return

    await ctx.send(f'Barajando en grupos de {group_size} participantes. ¡Vamos a la cita rápida! ;)')
    
    
    # Asignar el tamaño del grupo en el pool
    pool.group_size = group_size

    # Llamar a la función de shuffle para empezar el juego
     #await shuffle(ctx, group_size)
    
 # check if next message sent was by the author who sent the original command and in the same channel
    def check(m):
        return m.author == author and m.channel == ctx.message.channel
    
    rounds = 'g' # if 3 or more invalid inputs, exit speed dating start attempt
    fail_count = 0
    while (not rounds.isdigit() and rounds != 'none') and fail_count < 3:
        await ctx.send('Indique el número de rondas. Escribe \'none\' si desea finalizar manualmente las citas durante un número indeterminado de rondas.') # make an option to have no rounds and just use force shuffle
        msg = await bot.wait_for('message', check=check)
        rounds = msg.content
        fail_count += 1

    if fail_count >= 3:
        await ctx.send('Demasiadas entradas no válidas. Por favor, reinicie')
        return
    
    if rounds == 'none':
        rounds_str = 'Unset'
    else:
        rounds_str = rounds
        pool.rounds = int(rounds)

    fail_count = 0 
    time = 'hello'
    while (not time.isdigit() and time != 'none') and fail_count < 3: # while a valid time hasnt been entered
        await ctx.send('Indique el tiempo de duración de las rondas (en segundos). Escriba \'none\' si desea hacerlo manualmente)')
        msg = await bot.wait_for('message', check=check)
        time = msg.content
        fail_count += 1
    
    if fail_count >= 3:
        await ctx.send('Demasiadas entradas no válidas. Por favor, reinicie')
        return
        
    if time == 'none':
        time_str = 'Unset'
    else:
        time_str = time + ' seconds'
        pool.interval = int(time)
    
    await ctx.send(f'Duración de las rondas: {time_str}. Número de rondas: {rounds_str}. ¡Vamos a la cita rápida! ;)') # announcement to start

    if time == 'none':
        await ctx.send('Comenzando ronda #1')
        await shuffle(ctx)
        await ctx.send('Para barajar de nuevo, el autor del comando debe teclear \'!shuffle\' en este canal. Para terminar, escriba \'!end\'.')
    else: # timed shuffles
        minus_15s = pool.interval - 15
        if rounds == 'none':
            print('Número de rondas no establecido.')
            played = 1 # number of rounds played
            while not pool.ended and len(pool.participants) > 3:
                await ctx.send(f'Comenzando la ronda #{played}')
                await shuffle(ctx) 
                await ctx.send('Finalizado el movimiento de participantes. Comenzando cronómetro ahora.')
                played += 1

                # timing
                if pool.interval > 15:
                    await asyncio.sleep(minus_15s)
                    await countdown(ctx, 15)    # countdown last 15 seconds
                else:
                    await countdown(ctx, pool.interval)   # if initial interval <= 15, countdown all of it
        else:
            total_rounds = pool.rounds
            print(f'{total_rounds} rondas con intervalos de {time_str} segundos.')
            while not pool.ended and len(pool.participants) > 3 and pool.rounds > 0: 
                await ctx.send(f'Comenzando ronda #{total_rounds - pool.rounds + 1}')
                await shuffle(ctx)
                await ctx.send('Finalizado el movimiento de participantes. Comenzando cronómetro ahora.')

                # timing
                if pool.interval > 15:
                    await asyncio.sleep(minus_15s)
                    await countdown(ctx, 15)     
                else:
                    await countdown(ctx, pool.interval)       
    
        if not pool.ended: # game wasn't manually ended or # of participants not enough
            await end_game(ctx)


async def countdown(ctx, seconds):
    msg = await ctx.send("¡Advertencia! Tiempo restante: "+ str(seconds) + " segundos.")

    time = int(seconds)
    for x in range(1,time+1):
        await asyncio.sleep(1)
        await msg.edit(content = "¡Advertencia! Tiempo restante: "+ str(time-x) + " segundos.")

    await asyncio.sleep(1)
    await msg.edit(content = 'Ronda terminada.')


''' Returns true if there are 4+ participants, false otherwise.
'''    
def pool_is_valid():
    if len(pool.participants) > 3:
        return True
    return False
        
''' Bot command: force end game.
'''
@bot.command(name='end', help='Finaliza el juego')

async def force_end(ctx):
    if pool.ended:
        await ctx.send('No hay juego en curso.')
    else:
        await end_game(ctx)

''' Housekeeping for ending a game.
'''
async def end_game(ctx):
    if len(pool.participants) <= 3:
        await ctx.send('Finalizado citas rápidas porque se necesitan al menos 4 personas')
    else:
        await ctx.send('¡Las citas rápidas han terminado! Gracias por participar.') 
    
    for p in pool.participants:
        try:
            await p.move_to(pool.main_channel)
        except:
            await ctx.send(f'¡Hola <@{p.id}>! No he podido encontrarte ¡Por favor, vuelve a unirte al canal de voz principal del juego!')
    
    # delete all channels that were created
    for c in pool.channels:
        await c.delete()
    
    pool.reset_pool()
    await ctx.send('Limpieza completada')

''' Bot command: forces a shuffle.
'''
@bot.command(name='shuffle', help='Fuerza a mover aleatoriamente los participantes')

async def force_shuffle(ctx):
    print(pool.ended)
    if pool.ended:
        await ctx.send('No hay juego en curso')
    else:
        if pool.rounds != None and pool.rounds == 0:
            await ctx.send('¡No quedan más rondas!')
            await end_game(ctx)
            return
        await ctx.send('Forzando a los participantes a moverse...')
        if pool.rounds != None:
            await ctx.send(f'Rondas restantes: {pool.rounds - 1}')
        await shuffle(ctx)

''' Shuffles participants into random groups.
'''

''' Bot command: allow users to set the desired group size.
'''                 
@bot.command(name='groupsize', help='Establece el tamaño de los grupos')
async def set_group_size(ctx, size: int):
    if pool.ended:
        await ctx.send('No hay juego en curso.')
        return
    if size <= 1:
        await ctx.send('El tamaño del grupo debe ser de al menos 2.')
        return
    pool.group_size = size
    await ctx.send(f'Tamaño del grupo fijado en: {size}')


async def shuffle(ctx):
    if pool.rounds:
        pool.rounds -= 1
    guild = ctx.guild
    random.shuffle(pool.participants)
    
    # Calculate number of groups needed
    num_participants = len(pool.participants)
    group_size = pool.group_size
    num_groups = (num_participants + group_size - 1) // group_size  # Ceiling division

    # Create groups
    groups = [pool.participants[i * group_size:(i + 1) * group_size] for i in range(num_groups)]
    
    # Handle any leftover participants
    leftover = num_participants % group_size
    if leftover > 0:
        leftover_group = groups.pop()  # Remove and get the last group
        for participant in leftover_group:
            random.choice(groups).append(participant)  # Add to random existing group
    
    for i, group in enumerate(groups):
        channel_name = f'group{i + 1}'  # Channel name for each group
        existing_channel = discord.utils.get(guild.channels, name=channel_name)
        if not existing_channel:
            print(f'Creando un nuevo canal: {channel_name}')
            existing_channel = await guild.create_voice_channel(channel_name)
            pool.channels.append(existing_channel)
        for member in group:
            try:
                await member.move_to(existing_channel)
            except:
                await ctx.send(f'<@{member.id}> No he podido encontrarte ¡Por favor, vuelve a unirte a {channel_name}!')



                
        
''' Bot command: removes participant from pool.
''' 
@bot.command(name='remove', help='Elimina a un miembro de la lista de participantes utilizando el ID de ese miembro')

async def remove_member(ctx, u_id=None):
    if pool.ended:
        await ctx.send('¡No hay juego en curso del que retirarse')
        return

    print('Removiendo...')
    if not u_id:
        await ctx.send('Especifique el miembro que desea eliminar.')
        return
    guild = ctx.guild
    removed_user = await guild.fetch_member(u_id)
    if not removed_user:
        await ctx.send('Envía un ID de usuario válido (el usuario debe pertenecer a este servidor).')
        return
    success = pool.remove_member(removed_user)
    if success:
        print(f'Removed {removed_user}!')
        await ctx.send(f'Participant eliminado <@{u_id}>.')
    else:
        await ctx.send(f'{removed_user.name} ya estaba afuera!')

''' Bot command: adds participant to pool.
'''
@bot.command(name='add', help='Añade un miembro a la lista de participantes utilizando el ID')

async def add_member(ctx, u_id=None):
    if pool.ended:
        await ctx.send('No hay juego en curso al que añadir.')
        return

    print('Añadiendo...')
    if not u_id:
        await ctx.send('Por favor escifica el miembro a añadir!')
        return
    guild = ctx.guild
    added_user = await guild.fetch_member(u_id)
    if not added_user:
        await ctx.send('Por favor introduce un miembro válido')
        return
    success = pool.add_member(added_user)
    if success:
        print(f'Añadido {added_user}!')
        await ctx.send(f'Participant <@{u_id}>! Bienvenidos al juego!')
    else:
        await ctx.send(f'{added_user.name} ya estaba jugando!')

''' Bot command: shutdowns bot.
'''
@bot.command(name='goodbye', help='Cerrar sesión del bot')

async def log_out(ctx):
    await ctx.send('Adiós, ¡gracias por recibirme!')
    await bot.close()

@bot.event
async def on_ready():
    for guild in bot.guilds:
        if guild.name == GUILD:
            break
    print(f'{bot.user} se ha conectado a {guild.name}!')

    # set status
    await bot.change_presence(activity=discord.Game(name="¡Charlemos!"))

bot.run(TOKEN)