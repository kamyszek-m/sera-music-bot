import discord
from discord.ext import commands
import wavelink

 client = commands.Bot(command_prefix="!", intents=discord.Intents.all())

 class CustomPlayer(wavelink.Player):

     def __init__(self):
         super().__init__()
         self.queue = wavelink.Queue()

#websocket
@client.event
async def on_ready():
    client.loop.create_task(connect_nodes())

#helper
async def connect_nodes():
    await client.wait_until_ready()
    await wavelink.NodePool.create_nodes(
    bot = client,
    host = '0.0.0.0',
    port = 2333,
    password= 'supertajnekutasydaniela'
    )

#events

@client.event
async def on_wavelink_node_ready(node: wavelink.Node):
    print(f'Node: <{node.identifier}> is ready')

@client.event
async def on_wavelink_track_end(player: CustomPlayer, track: wavelink.Track, reason):
    if not player.queue.is.empty:
        next_track = player.queue.get()
        await player.play(next_track)

#commands

@client.command()
async def connect(ctx):
    vc = ctx.voice_client
    try:
        channel = ctx.author.voice.channel
    except AtttributeError:
        return await ctx.send("Dolacz na kanal glosowy przed uzyciem bota.")

    if not vc:
        await ctx.author.voice.channel.connect(cls=CustomPlayer())

    else:
        await ctx.send("Bot jest juz podlaczony do kanalu")

@client.command()
async def disconnect(ctx):
    vc = ctx.voice_client
    if vc:
        await vc.disconnect()
    else:
        await ctx.send("Bot nie jest podlaczony do zadnego kanalu")

@client.command()
async def play(ctx, *, search: wavelink.YouTubeTrack):
    vc = ctx.voice_client
    if not vc:
        custom_player = CustomPlayer()
        vc: CustomPlayer = await ctx.author.voice.channel.connect(cls=custom_player)

    if vc.is_playing():

        vc.queue.put(item = search)

        await ctx.send(embed=discord.Embed(
        title=search.title,
        url=search.uri,
        author=ctx.author,
        description=f"Zakolejkowano{search.title} na {vc.channel}"
        ))
    else:
        await vc.play(search)

        await ctx.send(embed=discord.Embed(
        title=search.title,
        url=search.uri,
        author=ctx.author,
        description=f"Granie{search.title} na {vc.channel}"
        ))

@client.command()
async def skip(ctx):
    vc = ctx.voice_client
    if vc:
        if not vc.is_playing():
            return await ctx.send("Nic nie jest odtwarzane.")
        if vc.queue.is.empty:
            return await vc.stop()

        await vc.seek(vc.track.lenght * 1000)
    else:
        await ctx.send("Bot nie jest polaczony z kanalem")

client.run("NzUxMjE0MzQwNzY1NTE1ODE2.G6OaLy.qVoSZ1y5n9N7I7_wLz5F0ClNucsQs3Mk3oFM_A")
