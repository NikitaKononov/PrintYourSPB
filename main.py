import os
import subprocess
import telebot
from telebot import types
from PIL import Image
import random

bot = telebot.TeleBot('5682277747:AAGJtSeNqmxpiltlsTyDSE6Wry3i3LFO13U')

@bot.message_handler(commands=["start"])
def start(m, res=False):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Конфетти")
    item2 = types.KeyboardButton("Мозаика")
    item3 = types.KeyboardButton("Принцесса дождя (Леонид Афремов)")
    item4 = types.KeyboardButton("Udnie (Франсис Пикабиа)")
    item5 = types.KeyboardButton("Случайно")
    markup.add(item1)
    markup.add(item2)
    markup.add(item3)
    markup.add(item4)
    markup.add(item5)
    bot.send_message(m.chat.id, 'Нажми:', reply_markup=markup)

def generate(model='candy.pth'):
    fls = os.listdir('places')
    img_dir = 'places/' + random.choice(fls)

    subprocess.run(
        "python fast_neural_style/neural_style/neural_style.py eval --content-image {} --model saved_models/{} "
        "--output-image candy.jpg --cuda 0".format(img_dir, model))

    print(img_dir)

    background = Image.open("candy.jpg").convert('RGBA')
    foreground = Image.open("text.png").convert('RGBA')

    final1 = Image.new("RGBA", background.size)
    final1.paste(background, (0, 0), background)
    final1.paste(foreground, (0, 0), foreground)

    final1.save("test3.png")
    img = open('test3.png', 'rb')\

    return img


@bot.message_handler(content_types=["text"])
def handle_text(message):
    if message.text.strip() == 'Конфетти':
        img = generate('candy.pth')
        bot.send_photo(message.chat.id, img)

    elif message.text.strip().startswith('Мозаика'):
        img = generate('mosaic.pth')
        bot.send_photo(message.chat.id, img)

    elif message.text.strip().startswith('Принцесса'):
        img = generate('rain_princess.pth')
        bot.send_photo(message.chat.id, img)

    elif message.text.strip().startswith('Udnie'):
        img = generate('udnie.pth')
        bot.send_photo(message.chat.id, img)

    elif message.text.strip().startswith('Случайно'):
        models = ['udnie.pth', 'rain_princess.pth', 'mosaic.pth', 'candy.pth']
        model = random.choice(models)
        print(model)
        img = generate(model)
        bot.send_photo(message.chat.id, img)

bot.polling(none_stop=True, interval=0)
