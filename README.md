# ecosystem_telegram

`ecosystem_telegram` это платформа для работы экосистемы из каналов для размещения контента 
и ботов с настройки для генерации и автопостинга материалоа
книги, статьи, цитаты, новости, мемы, картинки, объявления по работе и прочее


## Использование репозитория GitHub

```bash
git clone https://github.com/YuranIgnatenko/ecosystem_telegram.git
cd ecosystem_telegram
pip install -r requirements.
```

## Настройка платформы

```ini
# создание файла конфигурации
# или измените файл configure.ini
# и сохраните с именем config.ini
code config.ini # nano config.ini

# Пример структуры содержимого
# глобальные настройки
[global]
api_hash = your_api_hash
api_id = your_api_id
delay_seconds = 5
count_last_messages = 50
count_posting_images = 6
count_posting_memes = 5
schedule_posting = 10:00,01:55,01:56,02:04,02:05,02:06,02:07

# настройки каждого бота индивидуально
[cms_bot]
token = your_token_cms_bot
channel_chat_id = your_channel_chat_id_cms_bot

[images_bot]
status = False
channel_name = channel images
channel_chat_id = your_channel_chat_id_images_bot
token = your_token_images_bot
namefile_temp_downloaded = _temp_downloaded_images.jpg

[news_bot]
status = False
channel_name = channel news
channel_chat_id = your_channel_chat_id_news_bot
token = your_token_news_bot
namefile_temp_downloaded = _temp_downloaded_news.jpg
urls_channels = https://t.me/channel_url_1::0,
				https://t.me/channel_url_2::0,
				https://t.me/channel_url_3::0


[works_bot]
status = False
channel_name = channel works
channel_chat_id = your_channel_chat_id_works_bot
token = your_token_works_bot
urls_channels = https://t.me/channel_url_1::0,
				https://t.me/channel_url_2::0,
				https://t.me/channel_url_3::0,
				https://t.me/channel_url_4::0,
				https://t.me/channel_url_5::0

[books_bot]
status = False
channel_name = channel books
channel_chat_id = your_channel_chat_id_books_bot
token = your_token_books_bot
urls_channels = https://t.me/channel_url_1::0,
				https://t.me/channel_url_2::0,
				https://t.me/channel_url_3::0

#

```


## Заруск

```bash
python main.py
```

