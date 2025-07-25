import pymongo
import os
import pyrogram
import time
from pyrogram.types import Message
from bot.database import setffmpeg, getffmpeg, adduser, uploadtype, setmode, uploadtype1
from .devtools import progress_for_pyrogram
from .ffmpeg import functions, ffmpeg
from bot import bot, Config, LOGS

async def changeffmpeg(bot, message):
    try:
        await adduser(message)
        if len(message.text.split(" ", maxsplit=1)) < 2:
            await message.reply_text("**Please provide an FFmpeg code.**\nExample: `/setcode -c:v libx264 -crf 23 -preset fast`")
            return
        changeffmpeg = message.text.split(" ", maxsplit=1)[1].strip()
        if not changeffmpeg:
            await message.reply_text("**FFmpeg code cannot be empty.**")
            return
        await setffmpeg(message, changeffmpeg)
        LOGS.info(f"Set FFmpeg code for user {message.from_user.id}: {changeffmpeg}")
        escaped_code = Message.escape_markdown(changeffmpeg)
        await message.reply_text(f"**Ꮪuᴄᴄᴇssfully Ꮯhᴀngᴇd Ꭲhᴇ ᎰᎰᎷᏢᎬᏀ-ᏟᏫᎠᎬ Ꭲᴏ**\n```{escaped_code}```")
    except Exception as e:
        LOGS.error(f"Error in changeffmpeg: {e}")
        await message.reply_text(f"**Error:** ```{e}```")

async def changemode(bot, message):
    try:
        if len(message.text.split(" ", maxsplit=1)) < 2:
            await message.reply_text("**Please provide an upload mode.**\nExample: `/setmode video` or `/setmode document`")
            return
        newmode = message.text.split(" ", maxsplit=1)[1].strip().lower()
        if newmode not in ["video", "document"]:
            await bot.send_message(
                text="**Invalid upload mode.**\nUse `video` or `document`.",
                chat_id=message.from_user.id,
                reply_to_message_id=message.id
            )
            return
        await setmode(message, newmode)
        LOGS.info(f"Set upload mode for user {message.from_user.id}: {newmode}")
        await bot.send_message(
            text=f"**Ꮪuᴄᴄᴇssfully Ꮯhᴀngᴇd Ꮜᴩlᴏᴀd Ꮇᴏdᴇ Ꭲᴏ**\n```{newmode}```",
            chat_id=message.from_user.id,
            reply_to_message_id=message.id
        )
    except Exception as e:
        LOGS.error(f"Error in changemode: {e}")
        await bot.send_message(
            text=f"**Error:** ```{e}```",
            chat_id=message.from_user.id,
            reply_to_message_id=message.id
        )

async def get_type(bot, message):
    try:
        LOGS.info(f"get_type called by user {message.from_user.id}")
        upload_type = await uploadtype(message)
        LOGS.info(f"Upload type retrieved: {upload_type}")
        if upload_type:
            escaped_type = Message.escape_markdown(upload_type)
            await bot.send_message(
                text=f"**Ꮜᴩlᴏᴀd Ꮇᴏdᴇ Ꮖs**\n```{escaped_type}```",
                chat_id=message.from_user.id,
                reply_to_message_id=message.id
            )
        else:
            await bot.send_message(
                text="**No upload mode set.**\nUse `/setmode video` or `/setmode document` to set one.",
                chat_id=message.from_user.id,
                reply_to_message_id=message.id
            )
    except Exception as e:
        LOGS.error(f"Error in get_type: {e}")
        await bot.send_message(
            text=f"**Error:** ```{e}```",
            chat_id=message.from_user.id,
            reply_to_message_id=message.id
        )

async def get_ffmpeg(bot, message):
    try:
        LOGS.info(f"get_ffmpeg called by user {message.from_user.id}")
        ffmpegcodee = await getffmpeg(message)
        LOGS.info(f"Retrieved FFmpeg code for user {message.from_user.id}: {ffmpegcodee}")
        if ffmpegcodee:
            escaped_code = Message.escape_markdown(ffmpegcodee)
            if len(escaped_code) > 4000:
                await bot.send_message(
                    text="**FFmpeg code is too long to display. Sending as a file.**",
                    chat_id=message.from_user.id,
                    reply_to_message_id=message.id
                )
                with open("ffmpeg_code.txt", "w") as f:
                    f.write(ffmpegcodee)
                await bot.send_document(
                    chat_id=message.from_user.id,
                    document="ffmpeg_code.txt",
                    caption="FFmpeg Code",
                    reply_to_message_id=message.id
                )
                os.remove("ffmpeg_code.txt")
            else:
                await bot.send_message(
                    text=f"**ᎰᎰᎷᏢᎬᏀ ᏟᏫᎠᎬ ᏆᏚ**\n```{escaped_code}```",
                    chat_id=message.from_user.id,
                    reply_to_message_id=message.id
                )
        else:
            await bot.send_message(
                text="**No FFmpeg code set.**\nUse `/setcode` to set one, e.g., `/setcode -c:v libx264 -crf 23 -preset fast`.",
                chat_id=message.from_user.id,
                reply_to_message_id=message.id
            )
    except Exception as e:
        LOGS.error(f"Error in get_ffmpeg: {e}")
        await bot.send_message(
            text=f"**Error:** ```{e}```",
            chat_id=message.from_user.id,
            reply_to_message_id=message.id
        )

async def upload_dir(bot, message):
    try:
        u_start = time.time()
        if message.reply_to_message:
            message = message.reply_to_message
        if len(message.text.split(" ", maxsplit=1)) < 2:
            await bot.send_message(
                text="**Please provide a file path.**\nExample: `/uploaddir /path/to/file`",
                chat_id=message.from_user.id,
                reply_to_message_id=message.id
            )
            return
        cmd1 = message.text.split(" ", maxsplit=1)[1].strip()
        replyid = message.id
        if os.path.exists(cmd1):
            xhamster = await bot.send_message(
                text="➣ **Ꮜᴩlᴏᴀding Ꭲhᴇ Ꮩidᴇᴏ** 📁",
                chat_id=message.from_user.id,
                reply_to_message_id=message.id
            )
            await bot.send_document(
                chat_id=message.chat.id,
                document=cmd1,
                caption=os.path.basename(cmd1),
                reply_to_message_id=replyid,
                progress=progress_for_pyrogram,
                progress_args=(bot, "➣ **Ꮜᴩlᴏᴀding Ꭲhᴇ Ꮩidᴇᴏ** 📁", xhamster, u_start)
            )
            await xhamster.delete()
        else:
            await bot.send_message(
                text=f"**File Directory Not Found**\n```{cmd1}```",
                chat_id=message.from_user.id,
                reply_to_message_id=message.id
            )
    except Exception as e:
        LOGS.error(f"Error in upload_dir: {e}")
        await bot.send_message(
            text=f"**Error:** ```{e}```",
            chat_id=message.from_user.id,
            reply_to_message_id=message.id
        )

async def download_dir(bot, message):
    try:
        d_start = time.time()
        if not message.reply_to_message:
            await bot.send_message(
                text="**Reply to a file to download.**",
                chat_id=message.from_user.id,
                reply_to_message_id=message.id
            )
            return
        reply = await bot.send_message(
            text="➣ **Ꭰᴏwnlᴏᴀding Ꭲhᴇ Ꮩidᴇᴏ** 🚴‍♀️",
            chat_id=message.from_user.id,
            reply_to_message_id=message.id
        )
        video = await bot.download_media(
            message=message.reply_to_message,
            file_name=Config.TEMP,
            progress=progress_for_pyrogram,
            progress_args=(bot, "➣ **Ꭰᴏwnlᴏᴀding Ꭲhᴇ Ꮩidᴇᴏ** 🚴‍♀️", reply, d_start)
        )
        escaped_path = Message.escape_markdown(video)
        await reply.edit(f"**Directory Is**\n```{escaped_path}```")
    except Exception as e:
        LOGS.error(f"Error in download_dir: {e}")
        await bot.send_message(
            text=f"**Error:** ```{e}```",
            chat_id=message.from_user.id,
            reply_to_message_id=message.id
        )

async def sample(bot, message):
    try:
        if not message.reply_to_message:
            await bot.send_message(
                text="**Reply to a video file.**",
                chat_id=message.from_user.id,
                reply_to_message_id=message.id
            )
            return
        d_start = time.time()
        reply = await bot.send_message(
            text="**➣ Downloading Ꭲhᴇ Ꮩidᴇᴏ** 🚴‍♀️",
            chat_id=message.from_user.id,
            reply_to_message_id=message.id
        )
        video = await bot.download_media(
            message=message.reply_to_message,
            file_name=Config.TEMP,
            progress=progress_for_pyrogram,
            progress_args=(bot, "➣ **Ꭰᴏwnlᴏᴀding Ꭲhᴇ Ꮩidᴇᴏ** 🚴‍♀️", reply, d_start)
        )
        if not video:
            await reply.edit("**Failed to download video.**")
            return
        path, filename = os.path.split(video)
        output_filename = f"{filename}_sample.mkv"
        await reply.edit("**Generating Sample**")
        sample = await functions.sample(filepath=video, output=output_filename)
        if not sample:
            await reply.edit("**Failed to generate sample.**")
            os.remove(video)
            return
        caption = f"{filename} SAMPLE"
        await upload_handle(bot, message, sample, filename, caption, reply)
        os.remove(video)
        os.remove(sample)
        await reply.delete()
    except Exception as e:
        LOGS.error(f"Error in sample: {e}")
        await bot.send_message(
            text=f"**Error:** ```{e}```",
            chat_id=message.from_user.id,
            reply_to_message_id=message.id
        )

async def vshots(bot, message):
    try:
        if not message.reply_to_message:
            await message.reply_text("**Reply to a video file.**")
            return
        if len(message.text.split(" ", maxsplit=1)) < 2:
            await message.reply_text("**Please provide the number of screenshots.**\nExample: `/vshots 5`")
            return
        cmd1 = message.text.split(" ", maxsplit=1)[1].strip()
        try:
            cmd1 = int(cmd1)
        except ValueError:
            await message.reply_text("**Number of screenshots must be an integer.**")
            return
        if cmd1 > 30:
            await message.reply_text("**Maximum 30 screenshots allowed.**")
            return
        if cmd1 < 1:
            await message.reply_text("**Number of screenshots must be at least 1.**")
            return
        d_start = time.time()
        reply = await bot.send_message(
            text="**Downloading Video**",
            chat_id=message.from_user.id,
            reply_to_message_id=message.id
        )
        video = await bot.download_media(
            message=message.reply_to_message,
            file_name=Config.TEMP,
            progress=progress_for_pyrogram,
            progress_args=(bot, "**Downloading Video**", reply, d_start)
        )
        if not video:
            await reply.edit("**Failed to download video.**")
            return
        for x in range(1, cmd1 + 1):
            ss = await functions.screenshot(filepath=video)
            if not ss:
                await reply.edit(f"**Failed to generate screenshot {x}.**")
                continue
            u_start = time.time()
            await reply.edit(f"**Uploading Photo {x}**")
            await bot.send_photo(
                chat_id=message.from_user.id,
                photo=str(ss),
                caption=f"Screenshot {x}",
                progress=progress_for_pyrogram,
                progress_args=(bot, f"**Uploading Photo {x}**", reply, u_start)
            )
            os.remove(ss)
        os.remove(video)
        await reply.delete()
    except Exception as e:
        LOGS.error(f"Error in vshots: {e}")
        await message.reply_text(f"**Error:** ```{e}```")

async def upload_handle(bot, message, filepath, filename, caption, reply):
    try:
        if not os.path.exists(filepath):
            await bot.send_message(
                text="**File Not Found. Unable to Upload.**",
                chat_id=message.from_user.id,
                reply_to_message_id=message.id
            )
            return
        mode = await uploadtype(message)
        LOGS.info(f"Uploading file {filepath} in mode {mode} for user {message.from_user.id}")
        if mode == "video":
            u_start = time.time()
            thumb = await functions.screenshot(filepath)
            if not thumb:
                await reply.edit("**Failed to generate thumbnail.**")
                return
            width, height = await ffmpeg.resolution(filepath)
            duration2 = await ffmpeg.duration(filepath)
            s = await bot.send_video(
                video=filepath,
                chat_id=message.from_user.id,
                supports_streaming=True,
                file_name=filename,
                thumb=thumb,
                duration=duration2,
                width=width,
                height=height,
                caption=caption,
                reply_to_message_id=message.id,
                progress=progress_for_pyrogram,
                progress_args=(bot, "➣ **Ꮜᴩlᴏᴀding Ꭲhᴇ Ꮩidᴇᴏ** 🚴‍♀️", reply, u_start)
            )
            os.remove(thumb)
            await s.forward(Config.LOG_CHANNEL)
        elif mode == "document":
            u_start = time.time()
            s = await bot.send_document(
                document=filepath,
                chat_id=message.from_user.id,
                force_document=True,
                file_name=filename,
                caption=caption,
                reply_to_message_id=message.id,
                progress=progress_for_pyrogram,
                progress_args=(bot, "➣ **Ꮜᴩlᴏᴀding Ꭲhᴇ Ꮩidᴇᴏ** 🚴‍♀️", reply, u_start)
            )
            await s.forward(Config.LOG_CHANNEL)
        else:
            await bot.send_message(
                text="**Invalid upload mode set.**\nUse `/setmode video` or `/setmode document`.",
                chat_id=message.from_user.id,
                reply_to_message_id=message.id
            )
    except Exception as e:
        LOGS.error(f"Error in upload_handle: {e}")
        await bot.send_message(
            text=f"**Error:** ```{e}```",
            chat_id=message.from_user.id,
            reply_to_message_id=message.id
        )

async def upload_handle1(bot, from_user_id, filepath, filename, caption, reply, reply_to_message):
    try:
        if not os.path.exists(filepath):
            await bot.send_message(
                text="**File Not Found. Unable to Upload.**",
                chat_id=from_user_id,
                reply_to_message_id=reply_to_message
            )
            return
        mode = await uploadtype1(from_user_id)
        LOGS.info(f"Uploading file {filepath} in mode {mode} for user {from_user_id}")
        if mode == "document":
            u_start = time.time()
            s = await bot.send_document(
                document=filepath,
                chat_id=from_user_id,
                force_document=True,
                file_name=filename,
                caption=caption,
                reply_to_message_id=reply_to_message,
                progress=progress_for_pyrogram,
                progress_args=(bot, "➣ **Ꮜᴩlᴏᴀding Ꭲhᴇ Ꮩidᴇᴏ** 🚴‍♀️", reply, u_start)
            )
            await s.forward(Config.LOG_CHANNEL)
        elif mode == "video":
            u_start = time.time()
            thumb = await functions.screenshot(filepath)
            if not thumb:
                await reply.edit("**Failed to generate thumbnail.**")
                return
            width, height = await ffmpeg.resolution(filepath)
            duration2 = await ffmpeg.duration(filepath)
            s = await bot.send_video(
                video=filepath,
                chat_id=from_user_id,
                supports_streaming=True,
                file_name=filename,
                thumb=thumb,
                duration=duration2,
                width=width,
                height=height,
                caption=caption,
                reply_to_message_id=reply_to_message,
                progress=progress_for_pyrogram,
                progress_args=(bot, "➣ **Ꮜᴩlᴏᴀding Ꭲhᴇ Ꮩidᴇᴏ** 🚴‍♀️", reply, u_start)
            )
            os.remove(thumb)
            await s.forward(Config.LOG_CHANNEL)
        else:
            await bot.send_message(
                text="**Invalid upload mode set.**\nUse `/setmode video` or `/setmode document`.",
                chat_id=from_user_id,
                reply_to_message_id=reply_to_message
            )
    except Exception as e:
        LOGS.error(f"Error in upload_handle1: {e}")
        await bot.send_message(
            text=f"**Error:** ```{e}```",
            chat_id=from_user_id,
            reply_to_message_id=reply_to_message
                                             )
