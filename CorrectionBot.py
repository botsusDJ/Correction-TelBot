from spellchecker import SpellChecker
import telebot

spell = SpellChecker(language="en")
token = "TOKEN"
bot = telebot.TeleBot(token)

@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.chat.id, "This is a bot that corrects errors in the text that you write to it, in order to learn commands, type /help.")

@bot.message_handler(commands=["help"])
def help_message(message):
    bot.send_message(message.chat.id, "Write something to the bot. It correct the text\n/changelan and language code(like 'en') to change language.") 


@bot.message_handler(commands=["changelan"])
def change(message):
    try:
        global spell
        lang = "".join(message.text.split("/changelan ")).lower()
        spell = SpellChecker(language=f"{lang}")
    except ValueError:
        bot.send_message(message.chat.id, "Type language code(like 'en').")

@bot.message_handler(content_types=["text"])
def correct(message):
    text = message.text
    misspelled = spell.unknown(text.split())
    hasError = False

    response_text = ""
    for word in misspelled:
        corrected_word = spell.correction(word)

        if corrected_word != word:
            if corrected_word == None:
                response_text += f"No correction was found for the word '{word}'.\n"
                hasError = True
            else:
                response_text += f"You may have meant '{corrected_word}' instead of '{word}'.\n"
                hasError = True

    
    if hasError == False:
        bot.send_message(message.chat.id, "Everything is right👍.")    
    else:
        bot.send_message(message.chat.id, f"{response_text}")



bot.infinity_polling()
