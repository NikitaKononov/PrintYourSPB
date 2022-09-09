import subprocess
import telebot
from telebot import types
from PIL import Image

bot = telebot.TeleBot('5682277747:AAGJtSeNqmxpiltlsTyDSE6Wry3i3LFO13U')

@bot.message_handler(commands=["start"])
def start(m, res=False):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Конфетти")
    item2 = types.KeyboardButton("Мозаика")
    item3 = types.KeyboardButton("Принцесса дождя (Леонид Афремов)")
    item4 = types.KeyboardButton("Udnie (Франсис Пикабиа)")
    markup.add(item1)
    markup.add(item2)
    markup.add(item3)
    markup.add(item4)
    bot.send_message(m.chat.id, 'Нажми:', reply_markup=markup)


@bot.message_handler(content_types=['photo'])
def photo(message):
     fileID = message.photo[-1].file_id
     file_info = bot.get_file(fileID)
     downloaded_file = bot.download_file(file_info.file_path)
     with open("image.jpg", 'wb') as new_file:
         new_file.write(downloaded_file)


@bot.message_handler(content_types=["text"])
def handle_text(message):
    if message.text.strip() == 'Конфетти':
        subprocess.run("python fast_neural_style/neural_style/neural_style.py eval --content-image isak.jpg --model saved_models/candy.pth --output-image candy.jpg --cuda 0")
        background = Image.open("candy.jpg").convert('RGBA')
        foreground = Image.open("text.png").convert('RGBA')

        final1 = Image.new("RGBA", background.size)
        final1.paste(background, (0, 0), background)
        final1.paste(foreground, (0, 0), foreground)

        final1.save("test3.png")
        img = open('test3.png', 'rb')
        bot.send_photo(message.chat.id, img)

    elif message.text.strip().startswith('Мозаика'):
        subprocess.run(
            "python fast_neural_style/neural_style/neural_style.py eval --content-image isak.jpg --model saved_models/mosaic.pth --output-image mosaic.jpg --cuda 0")
        img = open('mosaic.jpg', 'rb')
        bot.send_photo(message.chat.id, img)

    elif message.text.strip().startswith('Принцесса'):
        subprocess.run(
            "python fast_neural_style/neural_style/neural_style.py eval --content-image isak.jpg --model saved_models/rain_princess.pth --output-image rain.jpg --cuda 0")
        img = open('rain.jpg', 'rb')
        bot.send_photo(message.chat.id, img)

    elif message.text.strip().startswith('Udnie'):
        subprocess.run(
            "python fast_neural_style/neural_style/neural_style.py eval --content-image isak.jpg --model saved_models/udnie.pth --output-image udnie.jpg --cuda 0")
        img = open('udnie.jpg', 'rb')
        bot.send_photo(message.chat.id, img)
    # Отсылаем юзеру сообщение в его чат
    # bot.send_message(message.chat.id, answer)

bot.polling(none_stop=True, interval=0)
