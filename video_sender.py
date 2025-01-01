# New_Tiki_Downloader/video_sender.py (1-35)
import requests
from Downloader import download_instagram_media

async def send_video(update, context):
    url = update.message.text.strip()  # Получаем URL от пользователя

    if not url:
        await update.message.reply_text("Пожалуйста, отправьте ссылку из Instagram.")
        return

    if 'instagram.com' in url:
        await update.message.reply_text("Загрузка медиа из Instagram...")

        try:
            # Получаем все медиафайлы из Instagram
            media_files = await download_instagram_media(url)

            # Отправляем каждый медиафайл пользователю
            for media_url, media_type in media_files:
                response = requests.get(media_url, stream=True)
                if media_type == 'video/mp4':
                    await update.message.reply_video(response.content, caption='Скачано с помощью @nr_downloader_bot')
                else:
                    await update.message.reply_photo(response.content)

        except Exception as e:
            print(f"Произошла ошибка: {str(e)}")

    else:
        await update.message.reply_text(text='Эта ссылка не относится к Instagram!')