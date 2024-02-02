import telebot
import config
import random
from telebot import types

client = telebot.TeleBot(config.config['token'])

def coin():
    return random.choice(['Орел', 'Решка'])

def dice_roll():
    return random.randint(1, 6)

def slot_machine():
    symbols = ['🍒', '🍊', '💎']
    result = [random.choice(symbols) for _ in range(3)]
    return result

@client.message_handler(commands=['start'])
def handle_start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Подбросить монетку")
    item2 = types.KeyboardButton("Подбросить кубик")
    item3 = types.KeyboardButton("Случайное число")
    item4 = types.KeyboardButton("Слот-машина")
    
    markup.add(item1, item2, item3, item4)

    client.send_message(message.chat.id, "Добро пожаловать в бот с минииграми!", reply_markup=markup)

@client.message_handler(func=lambda message: message.text == 'Подбросить монетку')
def handle_coin_toss(message):
    result = coin()
    client.send_message(message.chat.id, result)

@client.message_handler(func=lambda message: message.text == 'Подбросить кубик')
def handle_dice_roll(message):
    result = dice_roll()
    client.send_message(message.chat.id, result)

@client.message_handler(func=lambda message: message.text == 'Случайное число')
def handle_random_number(message):
    markup = types.ReplyKeyboardRemove(selective=False)
    client.send_message(message.chat.id, 'Введите число:', reply_markup=markup)
    client.register_next_step_handler(message, process_random_number)

def process_random_number(message):
    num = int(message.text)
    random_number = random.randint(0, num)
    client.send_message(message.chat.id, f'Случайное число от 0 до {num}: {random_number}')
    show_main_buttons(message)

@client.message_handler(func=lambda message: message.text == 'Слот-машина')
def handle_slot_machine(message):
    result = slot_machine()
    client.send_message(message.chat.id, ' '.join(result))
    if result == ['💎', '💎', '💎']:
        client.send_message(message.chat.id, 'Поздравляю, вы победили!')

    show_main_buttons(message)

def show_main_buttons(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Подбросить монетку")
    item2 = types.KeyboardButton("Подбросить кубик")
    item3 = types.KeyboardButton("Случайное число")
    item4 = types.KeyboardButton("Слот-машина")
    
    markup.add(item1, item2, item3, item4)
    
    client.send_message(message.chat.id, "Выберите одну из опций:", reply_markup=markup)

client.polling(non_stop=True, interval=0)
