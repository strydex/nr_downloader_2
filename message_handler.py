from validators import url
from video_sender import send_video


async def message_handler(update, context):
    text = update.message.text
    user = update.effective_user

    if url(text):
        await send_video(update,context)

    else:
        await context.bot.send_message(text="<b>Пожалуйста, пришлите ссылку на видео.</b>", chat_id=user.id, parse_mode='HTML')

