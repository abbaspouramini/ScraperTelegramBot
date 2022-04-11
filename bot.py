from telegram.ext.updater import Updater
from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext.commandhandler import CommandHandler
from telegram.ext.messagehandler import MessageHandler
from telegram.ext.filters import Filters
from telegram import *
from IMDbScraper import IMDbScraper
import pandas as pd
import  enum


class CurrentMode(enum.Enum):
    search=0
    select=1
    any=2

class Bot():
    def __init__(self):
        self.SearchByFilmName = "Search by film's name"
        self.Help = "Help"
        self.Contact_Us = "Contact Us"
        self.Datas = []
        self.Mode = CurrentMode.any
        self.startbuttons = self.CreateButtons([self.SearchByFilmName, self.Help, self.Contact_Us])

        # Bot Token
        self.updater = Updater(token="5273699514:AAFgv0M3bwU3vfle8Q5ForhdL8GldiKKniY")

    #Save Search History
    def SaveHistory(self,ID,datas):
        Table=pd.DataFrame(datas)
        Table.to_csv(path_or_buf=f"./Datas/{ID}.csv",mode='a')

    #Find
    def SearchHistory(self,ID,Title):
        Table=pd.read_csv(filepath_or_buffer=f"./Datas/{ID}.csv")
        Result=Table.where(Table['title']==Title)
        if Result==None:
            return None
        else:
            return Result


    #Create Reply Markup Buttons

    def CreateButtons(self,Contents):
        Buttons=[]
        for i in Contents:
            button=[KeyboardButton(i)]
            Buttons.append(button)
        return Buttons






    def start(self,update: Update, context: CallbackContext):

        context.bot.send_message(chat_id=update.effective_chat.id,text="Hello\U0001F44B  \nWelcome to IMDb bot.\nThis bot helps you get the film's information that you want  .\nHelp Button helps you how to use", reply_markup=ReplyKeyboardMarkup(self.startbuttons,one_time_keyboard=False))


    def reply(self,update:Update,context:CallbackContext):
        user_input=update.message.text

        #Buttons
        if user_input in self.SearchByFilmName:
            context.bot.send_message(chat_id=update.effective_chat.id,text="Send film's name\U0001F600")
            self.Mode=CurrentMode.search
        elif user_input ==self.Contact_Us and self.Mode==CurrentMode.any:
            context.bot.send_message(chat_id=update.effective_chat.id,text="\U00002709Mail:  abbas.pooramini.80@gmail.com\n\U0001F431GitHub:  www.github.com/abbaspouramini\n\U0001F517Linkedin:  www.linkedin.com/in/abbas-pouramini-b1b777211/",reply_markup=ReplyKeyboardMarkup(self.startbuttons, one_time_keyboard=False))
        elif user_input ==self.Help and self.Mode==CurrentMode.any:
            context.bot.send_message(chat_id=update.effective_chat.id,text="You can enter a film's title ;\nbot will show a number of films that close to title that you enter and you can select one of them to show it's detail for you.    ",reply_markup=ReplyKeyboardMarkup(self.startbuttons, one_time_keyboard=False))

        #Scrapping

        ## Show Final Result
        elif self.Mode==CurrentMode.select:
            number=int(user_input[0])-1
            caption = self.Datas[number]['caption']
            photo = self.Datas[number]["imageurl"]
            Data_to_save={
                'title':self.Datas[number]['title'],
                'product year':self.Datas[number]['product year'],
                'caption':caption,
                'imageurl':photo
            }
            self.SaveHistory(update.effective_chat.id,Data_to_save)
            self.Datas.clear()
            self.Mode = CurrentMode.any
            context.bot.send_photo(chat_id=update.effective_chat.id, caption=caption, photo=photo , reply_markup=ReplyKeyboardMarkup(self.startbuttons))

        ## Find Film Information
        elif self.Mode==CurrentMode.search:
            #find_from_csv=SearchHistory(update.effective_chat.id,)
            context.bot.send_message(chat_id=update.effective_chat.id, text="Wait a few moment \U0001F605")
            self.Datas.clear()
            scraper = IMDbScraper(user_input)
            if len(scraper.Datas)>0:
                for i in scraper.Datas:
                    self.Datas.append(i)
                Result = scraper.ResultOfSearch()
                buttons = self.CreateButtons(Result)
                text = "\U0001F3ACList of Results:\n\n"
                for i in Result:
                    text += i + "\n"
                self.Mode = CurrentMode.select
                context.bot.send_message(chat_id=update.effective_chat.id, text=text,reply_markup=ReplyKeyboardMarkup(buttons,one_time_keyboard=False))

            else:
                self.Mode = CurrentMode.any
                context.bot.send_message(chat_id=update.effective_chat.id, text="No results found. Please try again \U0001F62C	 ",reply_markup=ReplyKeyboardMarkup(self.startbuttons, one_time_keyboard=False))





#set updaters
bot=Bot()
bot.updater.dispatcher.add_handler(CommandHandler('start',bot.start))
bot.updater.dispatcher.add_handler(MessageHandler(Filters.text,bot.reply))

bot.updater.start_polling()
