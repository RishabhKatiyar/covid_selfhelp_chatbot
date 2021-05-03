from bot import telegram_chatbot

bot = telegram_chatbot('config.cfg')

def make_reply(msg):
    if msg is not None:
        reply = 'Hello. I am the COVID Self Help Chatbot. '
    return reply

update_id = None
while True:
    print('...')
    updates = bot.get_updates(offset=update_id)
    updates = updates['result']
    if updates:
        for item in updates:
            update_id = item['update_id']
            try:
                message = item['message']['text']
            except:
                message = None
            from_ = item['message']['from']['id']
            reply = make_reply(message)
            bot.send_message(reply, from_)
