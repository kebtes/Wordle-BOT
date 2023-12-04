from config import BOT_TOKEN
import telebot
from telebot import types
from util import Util

bot = telebot.TeleBot(BOT_TOKEN)
util = Util()

word = ""
game_history = []

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    start = types.InlineKeyboardButton("Start 🟩🟨⬛", callback_data="start_game")
    markup.add(start)

    bot.reply_to(message, "Hello there, let's play Wordle 😊, click 𝗦𝘁𝗮𝗿𝘁 to begin!", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "start_game")
def start_game(callback):
    global attempt 
    global word
    global game_history

    game_history = []
    attempt = 6
    
    chat_id = callback.message.chat.id
    word = util.generate_word().strip().lower()
    # print(word)
    bot.send_message(chat_id, "Game started! Guess the word by entering a 5 character long word.")

    def score_print(lst):
        output = ""
        for score in lst:
            output += " ".join(score) + "\n"
        return output
    
    @bot.message_handler(func=lambda message: message.chat.id == chat_id)
    def handle_guess(message):
        markup_2 = types.InlineKeyboardMarkup(row_width=1)
        play_again = types.InlineKeyboardButton("Play Again", callback_data="start_game")
        markup_2.add(play_again)
        
        global attempt
        global game_history

        output = [util.wrong_word] * 5
        guess = message.text.strip().lower()

        if len(guess) != len(word):
            bot.send_message(chat_id, "Please enter a word with the correct length.")
            return
        
        attempt -= 1
        
        for index, char in enumerate(guess):
            if char == word[index]:
                output[index] = util.correct_place
            elif char in word:
                output[index] = util.wrong_place

        game_history.append(output)

        if guess == word:
            game_history_output = score_print(game_history)
            bot.send_message(chat_id, f"😃🥳 You guessed the word correctly.\n"
                             f"Trials: {6 - attempt}")
            bot.send_message(chat_id, game_history_output, reply_markup=markup_2)
            attempt = 6
            return
        
        bot.send_message(chat_id, " ".join(output))

        if attempt <= 0:
            game_history_output = score_print(game_history)
            bot.send_message(chat_id, f"Game over! The word was '{word}'.")
            bot.send_message(chat_id, f"Trials: {6 - attempt}")
            bot.send_message(chat_id, game_history_output, reply_markup=markup_2)
            attempt = 6
            game_history = []

while True:
    try:
        bot.polling()
    except:
        pass

