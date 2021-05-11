from bot import telegram_chatbot
from extract_data import *

bot = telegram_chatbot('config.cfg')

def make_intro():
    reply = 'Hello. I am the COVID Self Help Chatbot.'
    return reply

def make_reply(msg):
    if msg is not None:
        reply = 'Please select a requirement:'
    return reply

def answer_query(data, reqmnt_list, state_list, city_list, chat_id, message_id, callback_id):
    bot.answer_callback_query(callback_id)
    if data[0] == 'None':
        reply = 'Please select a requirement:'
        bot.edit_message(reply, 'reqmnt', reqmnt_list, chat_id, message_id)
    elif data[0] == 'reqmnt':
        reply = f"Please select the state in which you want {data[1]}:"
        bot.edit_message(reply, 'state', state_list, chat_id, message_id, data[1])
    elif data[0] == 'state':
        reply = f"Please select the city in {data[2]} where you want {data[1]}:"
        bot.edit_message(reply, 'city', city_list, chat_id, message_id, data[1], data[2])
    elif data[0] == 'city':
        info = get_info(data[1], data[2], data[3])
        if data[1] == 'Oxygen':
            info = info[['NAME', 'CONTACT NUMBER']].reset_index()
            reply = f"Name: {info['NAME'][0]}\nContact No.: {info['CONTACT NUMBER'][0]}"
        elif data[1] == 'Hospital Beds':
            info = info[['Name of Hospital', 'Phone Number']].reset_index()
            reply = f"Name: {info['Name of Hospital'][0]}\nContact No.: {info['Phone Number'][0]}"
        bot.send_message(reply, chat_id)

reqmnt_list = get_reqmnt_list()
state_list = []
city_list = []
update_id = None
while True:
    updates = bot.get_updates(offset=update_id)
    updates = updates['result']
    if updates:
        for item in updates:
            update_id = item['update_id']
            if 'callback_query' in item:
                item = item['callback_query']
                callback_id = item['id']
                from_ = item['from']['id']
                message_id = item['message']['message_id']
                data = item['data'].split(':')
                if data[0] == 'reqmnt':
                    state_list = get_state_list(data[1])
                elif data[0] == 'state':
                    city_list = get_city_list(data[1], data[2])
                answer_query(data, reqmnt_list, state_list, city_list, from_, message_id, callback_id)
            elif 'message' in item:
                item = item['message']
                from_ = item['from']['id']
                message = item['text']
                reply = make_intro()
                bot.send_message(reply, from_)
                reply = make_reply(message)
                bot.send_message_inline(reply, 'reqmnt', reqmnt_list, from_)
