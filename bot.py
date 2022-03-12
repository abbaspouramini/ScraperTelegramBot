from telegram.ext.updater import Updater
from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext.commandhandler import CommandHandler
from telegram.ext.messagehandler import MessageHandler
from telegram.ext.filters import Filters
from telegram import *
from IMDbScraper import IMDbScraper





#Create Reply Markup Buttons

def CreateButtons(Contents):
    Buttons=[]
    for i in Contents:
        button=[KeyboardButton(i)]
        Buttons.append(button)
    return Buttons


#Bot Token
updater=Updater(token="5273699514:AAFgv0M3bwU3vfle8Q5ForhdL8GldiKKniY")


#Global Variable
##################
SearchByFilmName= "Search by film's name"
Help="Help"
Contact_Us="Contact Us"
Datas=[]
startbuttons=CreateButtons([SearchByFilmName,Help,Contact_Us])
##################

def start(update: Update, context: CallbackContext):

    context.bot.send_message(chat_id=update.effective_chat.id,text="Hello\U0001F44B  \nWelcome to IMDb bot.\nThis bot helps you get the film's information that you want  .\nHelp Button helps you how to use", reply_markup=ReplyKeyboardMarkup(startbuttons,one_time_keyboard=False))


def reply(update:Update,context:CallbackContext):
    user_input=update.message.text

    #Buttons
    if user_input in SearchByFilmName:
        context.bot.send_message(chat_id=update.effective_chat.id,text="Send film's name\U0001F600")
    elif user_input =="Contact Us":
        context.bot.send_message(chat_id=update.effective_chat.id,text="\U00002709Mail:  abbas.pooramini.80@gmail.com\n\U0001F431GitHub:  www.github.com/abbaspouramini\n\U0001F517Linkedin:  www.linkedin.com/in/abbas-pouramini-b1b777211/",reply_markup=ReplyKeyboardMarkup(startbuttons, one_time_keyboard=False))
    elif user_input =="Help":
        context.bot.send_message(chat_id=update.effective_chat.id,text="You can enter a film's title ;\nbot will show a number of films that close to title that you enter and you can select one of them to show it's detail for you.    ",reply_markup=ReplyKeyboardMarkup(startbuttons, one_time_keyboard=False))

    #Scrapping
    elif  ("1." in user_input) or ("2."in user_input) or ("3."in user_input) or ("4."in user_input) or ("5."in user_input) or ("6."in user_input):
        number=int(user_input[0])-1
        caption = Datas[number]['caption']
        photo = Datas[number]["imageurl"]
        Datas.clear()
        context.bot.send_photo(chat_id=update.effective_chat.id, caption=caption, photo=photo , reply_markup=ReplyKeyboardMarkup(startbuttons))
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Wait a few moment \U0001F605")
        Datas.clear()
        scraper = IMDbScraper(user_input)
        if len(scraper.Datas)>0:
            for i in scraper.Datas:
                Datas.append(i)
            Result = scraper.ResultOfSearch()
            buttons = CreateButtons(Result)
            text = "\U0001F3ACList of Results:\n\n"
            for i in Result:
                text += i + "\n"
            context.bot.send_message(chat_id=update.effective_chat.id, text=text,reply_markup=ReplyKeyboardMarkup(buttons,one_time_keyboard=False))

        else:
            context.bot.send_message(chat_id=update.effective_chat.id, text="No results found. Please try again \U0001F62C	 ",reply_markup=ReplyKeyboardMarkup(startbuttons, one_time_keyboard=False))






updater.dispatcher.add_handler(CommandHandler('start',start))
updater.dispatcher.add_handler(MessageHandler(Filters.text,reply))

updater.start_polling()