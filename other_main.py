import discord
from discord.ext import commands
import yt_dlp as youtube_dl
import asyncio
import tempfile
import os
import random
import time

# --- Intents ---
intents = discord.Intents(
    guilds=True,
    messages=True,
    message_content=True,
    voice_states=True
)

bot = commands.Bot(command_prefix="!", intents=intents)

# --- yt-dlp setup ---
ytdl_format_options = {
    'format': 'bestaudio/best',
    'quiet': True,
    'noplaylist': True,
    'ignoreerrors': True,
    'no_warnings': True,
    'default_search': 'auto',
}

ffmpeg_options = {'options': '-vn'}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

# --- Bot startup ---
@bot.event
async def on_ready():
    print(f"✅ Bot is online as {bot.user}")

# --- Debug logger ---
folder = r"C:\Users\ReMarkt\PycharmProjects\discord_bot\playlists"  # replace with your folder path
current_list = "NONE"
listening = False
listening_name = "NONE"
leave = False
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    ctx = await bot.get_context(message)
    await bot.process_commands(message)

    global current_list, listening, listening_name, leave
    content = message.content.lower()
    print(message.author.name)
    if message.author.name == "james_vh":
        link = "biggest_boy.webp"
        with open(link, "rb") as f:
            import time
            await message.channel.send("stfu nigger")
            a = 0
            while a < 4:
                a += 1
                await message.channel.send("kys")
                time.sleep(0.1)

    if content == "bas show playlists":
        files = [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]
        string = "your playlists:\n"
        for file in files:
            with open(os.path.join(folder, file), "r", encoding="utf-8") as f:
                am = len(f.readlines())
            string += f"- {file}   {am} songs\n"
        await message.channel.send(string)
        return

    if content.startswith("bas create playlist "):
        name = message.content.removeprefix("bas create playlist ").strip()
        with open(os.path.join(folder, name), "w", encoding="utf-8") as f:
            pass
        await message.channel.send(f"Created a new playlist: '{name}'")
        return

    if content.startswith("bas open "):
        name = message.content.removeprefix("bas open ").strip()
        current_list = name
        songs = ""
        with open(os.path.join(folder, name), "r", encoding="utf-8") as f:
            lines = f.readlines()

            for line in lines:
                l = line.strip().split("@")
                songs += f"- {l[0]}   {l[1]}\n"
        msg = await message.channel.send(
            f"**{name}** {len(lines)} songs:\n{songs}"
        )

        await msg.edit(suppress=True)
        return

    if content == "bas close":
        await message.channel.send(f"Closed **{current_list}**")
        current_list = "NONE"
        return

    if content.startswith("bas play "):
        if current_list == "NONE":
            await message.channel.send("You have to open a playlist first.")
            return

        name = message.content.removeprefix("bas play ").strip()
        with open(os.path.join(folder, current_list), "r", encoding="utf-8") as f:
            lines = f.readlines()
            start = False
            for line in lines:
                l = line.strip().split("@")
                if start and not leave:
                    await play_youtube(ctx, l[1])
                if l[0] == name:
                    await play_youtube(ctx, l[1])
                    start = True
                    print("finished playing")
            if not leave:
                if start:
                    await message.channel.send("Finished playlist")
                else:
                    await message.channel.send("song not found in playlist")
            leave = False
        return
    if content.startswith("bas add song "):
        listening_name = message.content.removeprefix("bas add song ").strip()
        await message.channel.send("paste a youtube link for this song")
        listening = True
        return
    if content.startswith("https://www.youtube.com/watch?v=") and listening and listening_name != "NONE":
        listening = False
        with open(os.path.join(folder, current_list), "a", encoding="utf-8") as f:
            f.write("\n" + listening_name + "@" + message.content)
        await message.channel.send("added **" + listening_name + "** to playlist")
        return

    if content.startswith("bas remove song "):
        name = message.content.removeprefix("bas remove song ").strip()

        if current_list == "NONE":
            await message.channel.send(f"you must open a playlist first")
            return

        playlist_path = os.path.join(folder, current_list)

        # Read all lines
        with open(playlist_path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        # Filter out the song with the given name
        new_lines = [line for line in lines if not line.strip().startswith(name + "@")]

        # Check if any line was actually removed
        if len(new_lines) == len(lines):
            await message.channel.send(f"song **{name}** not found in playlist")
        else:
            # Write the updated playlist back
            with open(playlist_path, "w", encoding="utf-8") as f:
                f.writelines(new_lines)
            await message.channel.send(f"removed **{name}** from playlist")
        return

    if content.startswith("bas?"):
        await message.channel.send("commands:\n"
                                   "- **bas show playlists** shows all of the playlists\n"
                                   "- **bas create playlist ** creates a new playlist\n"
                                   "- **bas open 'playlist name'** opens that playlist\n"
                                   "- **bas close** closes the current playlist\n"
                                   "- **bas play 'song name'** plays the song whit that name\n"
                                   "- **bas add song 'song name'** adds song to the playlist\n"
                                   "- **bas remove song 'song name'** removes song from the playlist\n"
                                   "- **bas link play 'song name'** plays a song directly from a link without playlist\n"
                                   "- **bas get out** makes bas leave\n"
                                   "- **bas skip** skips to the next song\n")
        return

    if content.startswith("bas link play "):
        name = message.content.removeprefix("bas link play ").strip()
        await play_youtube(ctx, name)
        return

    if content.startswith("bas skip"):
        if ctx.voice_client:
            await ctx.voice_client.disconnect()
            await ctx.send("skipping song")
        else:
            await ctx.send("nothing to skip")
        return
    if content.startswith("bas crack "):
        import time
        name = message.content.removeprefix("bas crack ").strip().upper()
        await ctx.send("HOLY FUCK")
        time.sleep(1)
        await ctx.send("IM CUMMING")
        time.sleep(1)
        await ctx.send("HOLY SHIT")
        time.sleep(1)
        await ctx.send(f"YES {name} YESSSSS")
        time.sleep(1)
        return

    if content.startswith("bas get out"):
        if ctx.voice_client:
            leave = True
            await ctx.voice_client.disconnect()
            await ctx.send("man fuck you")
        else:
            await ctx.send("i didn't even do nun")
        return

    if content.startswith("bas shuffle"):
        if current_list == "NONE":
            await ctx.send("open a playlist first")
            return
        with open(os.path.join(folder, current_list), "r", encoding="utf-8") as f:
            lines = f.readlines()
            num_before = -1
            number = random.randint(0, len(lines) - 1)
            while leave == False:
                while num_before == number:
                    number = random.randint(0, len(lines) - 1)
                line = lines[number]
                l = line.strip().split("@")
                await play_youtube(ctx, l[1])
                num_before = number
            leave = False
        return

    if content.startswith("bas pik je die?"):
        sencices = ["ja?",
                    "kom dan",
                    "he",
                    "sukkel",
                    "ja dacht ik al",
                    "afgeragde zwartjoekel",
                    "paashaas schaamhaar verzamalaar",
                    "fucking pap neger",
                    "ja nu jij weer",
                    "volgende keer verkracht ik je helemaal kapot"
                    ]
        import time
        for sen in sencices:
            await message.channel.send(sen)
            time.sleep(1)

    if content.startswith("bas"):
        await message.channel.send("❌ Not a valid command")
        return

    if "ik ben " in message.content.lower():
        m = message.content.lower()
        result = m.split("ik ben ", 1)[1]
        await message.channel.send("hallo " + result)
        return
    if "i am " in message.content.lower():
        m = message.content.lower()
        result = m.split("i am ", 1)[1]
        await message.channel.send("hallo " + result)
        return


# --- Ping test ---
@bot.command()
async def ping(ctx):
    await ctx.send("Pong! Bot is working.")

# --- Play YouTube audio ---
@bot.command()
async def play(ctx):
    if not ctx.author.voice:
        await ctx.send("❌ You need to be in a voice channel first.")
        return

    channel = ctx.author.voice.channel

    # Connect or move the bot
    if ctx.voice_client:
        if ctx.voice_client.channel != channel:
            await ctx.voice_client.move_to(channel)
    else:
        await channel.connect(reconnect=True)

    await ctx.send("Send me the **YouTube link** to play:")

    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel

    try:
        msg = await bot.wait_for('message', check=check, timeout=60)
        url = msg.content.strip()

        # Download audio to a temp file
        with tempfile.TemporaryDirectory() as tmp_dir:
            info = ytdl.extract_info(url, download=True)
            filename = ytdl.prepare_filename(info)
            temp_path = os.path.join(tmp_dir, os.path.basename(filename))
            os.rename(filename, temp_path)

            ctx.voice_client.stop()
            ctx.voice_client.play(
                discord.FFmpegPCMAudio(temp_path, **ffmpeg_options),
                after=lambda e: print(f"Finished playing: {e}") if e else None
            )

            await ctx.send(f"▶ Now playing: {info.get('title', 'Unknown')}")

            # Wait until playback is finished
            while ctx.voice_client.is_playing():
                await asyncio.sleep(1)

    except asyncio.TimeoutError:
        await ctx.send("⏰ You didn’t send a link in time!")
    except Exception as e:
        await ctx.send(f"❌ Error: {e}")

async def play_youtube(ctx, url: str):
    if not ctx.author.voice:
        await ctx.send("❌ You need to be in a voice channel first.")
        return

    channel = ctx.author.voice.channel

    # Connect or move the bot
    if ctx.voice_client:
        if ctx.voice_client.channel != channel:
            await ctx.voice_client.move_to(channel)
    else:
        await channel.connect(reconnect=True)

    try:
        # Download audio to a temp file
        with tempfile.TemporaryDirectory() as tmp_dir:
            info = ytdl.extract_info(url, download=True)
            filename = ytdl.prepare_filename(info)
            temp_path = os.path.join(tmp_dir, os.path.basename(filename))
            os.rename(filename, temp_path)

            ctx.voice_client.stop()
            ctx.voice_client.play(
                discord.FFmpegPCMAudio(temp_path, **ffmpeg_options),
                after=lambda e: print(f"Finished playing: {e}") if e else None
            )

            await ctx.send(f"▶ Now playing: {info.get('title', 'Unknown')}")

            # Wait until playback is finished
            while ctx.voice_client.is_playing():
                await asyncio.sleep(1)

    except Exception as e:
        await ctx.send(f"❌ Error: {e}")
# --- Leave voice channel ---
@bot.command()
async def leaasdve(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.send("✅ Left voice channel")
    else:
        await ctx.send("❌ Not connected.")

# --- Run bot ---
bot.run("bas_MTM5NjUwMjU1MjA2OTAxMzU0NA.GXpI4l.8t_c2-S4qGc6U_VEK7lDqOhBNTogBmB9uDWKzQ")
