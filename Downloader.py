import instaloader

# Функция для загрузки медиафайлов из Instagram
async def download_instagram_media(url):
    loader = instaloader.Instaloader()

    # Функция для получения поста по URL
    shortcode = url.split("/")[-2]  # Извлечение shortcode из URL
    post = instaloader.Post.from_shortcode(loader.context, shortcode)

    media_files = []

    if post.typename == "GraphSidecar":  # Тип медиа - карусель
        for node in post.get_sidecar_nodes():
            if node.is_video:
                media_files.append((node.video_url, 'video/mp4'))
            else:
                media_files.append((node.display_url, 'image/jpeg'))
    else:  # Одиночный медиафайл (изображение или видео)
        if post.is_video:
            media_files.append((post.video_url, 'video/mp4'))
        else:
            media_files.append((post.url, 'image/jpeg'))

    return media_files