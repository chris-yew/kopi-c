from bot import telegram_chatbot
import telebot
from vulcan_package import vulcan 

news=vulcan("https://vulcanpost.com/category/news/")
bot=telegram_chatbot("config.cfg")
update_id = None

"""def make_reply(msg):
    if msg is not None:
        reply=news.news_highlight()
        for i in range(len(reply)):
            return reply[i]"""


while True:
    updates=bot.get_updates(offset=update_id)
    updates=updates["result"]
    if updates:
        for item in updates:
            update_id=item["update_id"]
            try:
                message=item["message"]["text"]
            except:
                message=None
            from_=item["message"]["from"]["id"]
            for i in news.news_highlight():
            #reply=make_reply(message)
                bot.send_message(i,from_)
         