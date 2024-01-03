import telebot
import config
import random
from telebot import types

client = telebot.TeleBot(config.config['token'])

def coin():
    return random.choice(['Орел', 'Решка'])

@client.message_handler(commands=['start'])
def handle_start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Подбросить монетку")
    item2 = types.KeyboardButton("Подбросить кубик")
    item3 = types.KeyboardButton("Рандомное число")
    
    markup.add(item1, item2, item3)

    client.send_message(message.chat.id, "Добро пожаловать в бот с минииграми, выбери необходимое", reply_markup=markup)

@client.message_handler(func=lambda message: message.text == 'Подбросить монетку')
def handle_coin_toss(message):
    result = coin()
    client.send_message(message.chat.id, result)

@client.message_handler(func=lambda message: message.text == 'Подбросить кубик')
def handle_dice_roll(message):
    client.send_message(message.chat.id, random.randint(1, 6))

@client.message_handler(func=lambda message: message.text == 'Рандомное число')
def handle_random_number(message):
    keyboard = types.ReplyKeyboardRemove(selective=False)
    client.send_message(message.chat.id, 'Введите число:', reply_markup=keyboard)
    client.register_next_step_handler(message, process_num_input)

def process_num_input(message):
    if message.text.isdigit():
        num = int(message.text)
        random_number = random.randint(0, num)
        client.send_message(message.chat.id, f'Случайное число от 0 до {num}: {random_number}')

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item = types.KeyboardButton("Меню")
        markup.add(item)
        client.send_message(message.chat.id, "Для возвращения в меню нажмите кнопку", reply_markup=markup)
        client.register_next_step_handler(message, handle_menu)

def handle_menu(message):
    handle_start(message)

client.polling(non_stop=True, interval=0)
