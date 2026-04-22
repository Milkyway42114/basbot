import random
import asyncio
import time
import os
from pathlib import Path

import discord
from discord.ext import commands
import functools

# Replace with your bot token
TOKEN = 'MTM5NjUwMjU1MjA2OTAxMzU0NA.GUnBCv.Ca-93t5mU6nm2bxTdKo2CzikSFqN3DPhZ0keOI'

# Set command prefix, e.g. '!' or '?' or ''
intents = discord.Intents.default()
intents.message_content = True  # Required for reading message content

# some vars
surprise_num = 1

bas_enabled = True
f_enabled = True
natuurkunde_enabled = True
can_i = True
ohd_feature = True
thom_feature = True

physics_list = [
    "natuurkunde",
    "physics",
    "hefboom",
    "volt",
    "ampere",
    "kracht",
    "massa",
    "versnelling",
    "energie",
    "vermogen",
    "valversnelling",
    "zwaartekracht",
    "weerstand",
    "stroom",
    "spanning",
    "elektromagnetisme",
    "magnetisme",
    "frequentie",
    "isolator",
    "geleider",
    "gravitatie",
    "momentum",
    "zwaartepunt",
    "dichtheid",
    "quantum",
    "atoom",
    "proton",
    "neutron",
    "elektron"
]

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Bot is online as {bot.user}')

@bot.event
async def on_message(message):
    global f_enabled, bas_enabled, natuurkunde_enabled, physics_list, can_i, ohd_feature, thom_feature
    # Don't respond to the bot itself
    if message.author == bot.user:
        return
    await bot.process_commands(message)


    if message.content == "/features":
        await message.channel.send(""
            "current bas features:\n"
            "- saying 'bas' gives a bassing response\n"
            "- saying anything that has the letter f in it wil send a f student video\n"
            "- /phaeton sends a randomized phaeton GIF\n"
            "- /surprise gives a surprise ;)\n"
            "- /ena shows witch features are enabled\n"
            "- /ena ... inverts the state of the chosen feature\n"
            "- saying anything physics related triggers bas\n"
            "- /natuurkunde list gives all the triger words\n"
            "- saying 'can i' sends a 'can i get euhmmm' GIF\n"
            "- saying 'ohd' or 'obama have dih' in a sentence wil send obama have dih image\n"
            "- saying 'thom' wil say something about thom\n"
            "- saying /p ... wil play a sound in vc")
        return
    if message.content.startswith("/ena"):
        if message.content == "/ena":
            await message.channel.send(""
                "feature state\n"
                "- saying 'bas' feature: " + str(bas_enabled) + "\n"
                "- saying 'f' feature: " + str(f_enabled) + "\n"
                "- saying anything physics related feature: " + str(natuurkunde_enabled) + "\n"
                "- saying 'can i' feature: " + str(can_i) + "\n"
                "- saying 'odh' feature: " + str(ohd_feature) + "\n"
                "- saying 'thom' feature: " + str(thom_feature))
        if message.content.startswith("/ena "):
            msg = message.content[5:]
            if msg == "f":
                f_enabled = not f_enabled
                await message.channel.send("feature: '" + msg + "' = " + str(f_enabled))
                return
            if msg == "bas":
                bas_enabled = not bas_enabled
                await message.channel.send("feature: '" + msg + "' = " + str(bas_enabled))
                return
            if msg == "natuurkunde":
                natuurkunde_enabled = not natuurkunde_enabled
                await message.channel.send("feature: '" + msg + "' = " + str(natuurkunde_enabled))
                return
            if msg == "h":
                can_i = not can_i
                await message.channel.send("feature: '" + msg + "' = " + str(can_i))
                return
            if msg == "ohd":
                ohd_feature = not ohd_feature
                await message.channel.send("feature: '" + msg + "' = " + str(ohd_feature))
                return
            if msg == "thom":
                thom_feature = not thom_feature
                await message.channel.send("feature: '" + msg + "' = " + str(thom_feature))
                return

            await message.channel.send("no feature: '" + msg + "'")
            return
    if message.content == "/natuurkunde list":
        string = "natuurkunde trigger words:\n"
        for word in physics_list:
            string += "- " + word + "\n"
        await message.channel.send(string)
        return

    if "bas" in message.content.lower() and bas_enabled:
        await message.channel.send(f'did someone say bas?!')
        embed = discord.Embed(title="BASSSS!!!")
        embed.set_image(url="https://milkyway42114.github.io/Test/bas.jpg")
        await message.channel.send(embed=embed)

    if message.content == "/phaeton":
        num = random.randint(1, 3)
        link = "https://tenor.com/view/phaeton-gif-11355370918435171378"
        if num == 2 :
            link = "https://tenor.com/view/volkswagen-phaeton-vw-phaeton-phaeton-vw-volkswagen-gif-14216567301389376913"
        if num == 3 :
            link = "https://tenor.com/view/vw-phaeton-gif-3576509804728944999"
        await message.channel.send("THANK God PHAETON🙏🚗❤️THANK God PHAETON🙏❤GUARDIAN ANGEL PHAETON TO EACH OF YOU🙏🚗🖤❤GOD SAVE THE PHAETON🙏🖤❤️THANK YOU FOR OUR PHAETONS🚗")
        await message.channel.send(link)

    if message.content == "/surprise":
        global surprise_num
        num = surprise_num
        surprise_num += 1
        if surprise_num > 5:
            surprise_num = 1
        link = "surprise/" + str(num) + ".mp4"
        with open(link, "rb") as f:
            await message.channel.send("getting your surprise ready...")
            await message.channel.send("pro tip: max ur volume ;)", file=discord.File(f, link))

    if "/credits" in message.content.lower():
        await message.channel.send("Milkyway42114: did everything\nkingseppie1: basted to bas van valen")

    if "/p list" in message.content.lower():
        list = "sounds list:\n"

        for file in Path("sounds").iterdir():
            if file.is_file():
                list += "- " + file.name[:-4] + "\n"



        return await message.channel.send(list)

    if "/p " in message.content.lower():
        if True:

            if not message.author.voice:
                return await message.channel.send("Join VC")

            src = message.content.lower()[3:]
            path_src = f"sounds/{src}.mp3"

            if not os.path.exists(path_src):
                return await message.channel.send("Sound doesn't exist")

            channel = message.author.voice.channel

            # ---- FIX 1: If already connected, reuse the VC ----
            voice_client = message.guild.voice_client

            if voice_client and voice_client.channel != channel:
                await voice_client.disconnect(force=True)
                voice_client = None

            # ---- FIX 2: Safe connect (no double connect) ----
            if not voice_client:
                await asyncio.sleep(1)  # FIX handshake race
                voice_client = await channel.connect(reconnect=False)

            # ---- FIX 3: Stop existing audio ----
            if voice_client.is_playing():
                voice_client.stop()

            source = discord.FFmpegPCMAudio(
                path_src,
                executable="C:/ffmpeg/ffmpeg-7.1.1-essentials_build/bin/ffmpeg.exe"
            )

            # ---- FIX 4: Auto disconnect ----
            def after_playing(error):
                if error:
                    print("Error during playback:", error)
                coro = voice_client.disconnect(force=True)
                asyncio.run_coroutine_threadsafe(coro, bot.loop)

            voice_client.play(source, after=after_playing)

        else:
            await message.channel.send("nice try bucko buddy pal")

    for item in physics_list:
        if item in message.content.lower() and natuurkunde_enabled:
            with open("bas_smal.png", "rb") as img:
                await message.channel.send(item + "? natuurkunde? bas van valen reference!🔥🔥", file=discord.File(img))

    if "ohd" in message.content.lower() or "obama have dih" in message.content.lower():
        if ohd_feature:
            link = "ohd.webp"
            with open(link, "rb") as f:
                await message.channel.send(file=discord.File(f, link))
            return

    if "f" in message.content.lower() and f_enabled:
        with open("f_students/f.mp4", "rb") as f:
            await message.channel.send("f students are inventors🥀", file=discord.File(f, "f_students/f.mp4"))
            return

    if "thom" in message.content.lower() and thom_feature:
        link = "great.jpg"
        link2 = "soft.webp"
        with open(link, "rb") as f:
            await message.channel.send("great guy!, no complaints", file=discord.File(f, link))
        time.sleep(3)
        with open(link2, "rb") as f:
            await message.channel.send("but he is form lagezwaluwe tho...", file=discord.File(f, link2))
        return


    if "euh" in message.content.lower() and can_i and message.content.lower() != "/play phaeton":
        with open("can.gif", "rb") as gif:
            await message.channel.send(file=discord.File(gif, "can.gif"))



@bot.command()
async def join(ctx):
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        await channel.connect()
        await ctx.send(f"Joined {channel}")
    else:
        await ctx.send("You're not in a voice channel!")

@bot.command()
async def leave(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.send("Disconnected")
    else:
        await ctx.send("I'm not in a voice channel!")

@bot.command()
async def play(ctx):
    voice_client = ctx.voice_client

    if not voice_client:
        if ctx.author.voice:
            voice_client = await ctx.author.voice.channel.connect()
        else:
            return await ctx.send("You're not in a voice channel!")

    if voice_client.is_playing():
        voice_client.stop()

    source = discord.FFmpegPCMAudio("phaeton.mp3", executable="C:/ffmpeg/ffmpeg-7.1.1-essentials_build/bin/ffmpeg.exe")
    voice_client.play(source)




bot.run(TOKEN)