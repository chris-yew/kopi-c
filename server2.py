import telebot
import configparser as cfg 
from vulcan_package import vulcan 

news=vulcan("https://vulcanpost.com/category/news/")

def read_token_from_config_file(config):
        parser=cfg.ConfigParser()
        parser.read(config)
        return parser.get("creds","token")

bot=telebot.TeleBot(token="...")

@bot.message_handler(commands=['news'])
def send_welcome(message):
    for i in news.news_highlight():
        bot.reply_to(message,i)
bot.polling()