import telebot
from telegram_bot_functions import send_message_with_buttons, send_word_to_user_learning, send_word_to_user_examination, \
    check_user_answer_exam, send_word_to_user_for_repeating, process_tense_practice
from database_functions import get_user, add_word_to_learning, \
    mark_word_as_known, mark_word_as_ready_for_exam, set_activity, set_tense

bot = telebot.TeleBot('Your tg bot key')


@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    get_user(user_id)
    send_message_with_buttons(message.chat.id, "Welcome to the English learning bot!",
                              ['Learn New Word'], bot, None)


@bot.message_handler(func=lambda message: True, content_types=['text'])
def handle_text(message):
    chat_id = message.chat.id
    user_input = message.text
    username = message.from_user.id
    user = get_user(username)

    if user_input == 'Learn New Word':
        set_activity(user, 'words learning')
        send_word_to_user_learning(chat_id, bot, user)

    elif user_input == 'Add to learning':
        add_word_to_learning(user)
        send_word_to_user_learning(chat_id, bot, user)
    elif user_input == 'Already know':
        mark_word_as_known(user)
        send_word_to_user_learning(chat_id, bot, user)
    elif user_input == 'Exam':
        set_activity(user, 'exam')
        send_word_to_user_examination(chat_id, bot, user)
    elif user_input == 'Cancel':
        set_activity(user, None)
        message = "Choose what you want"
        buttons = ['Repeat Learned Words', 'Learn New Word', 'Exam']
        send_message_with_buttons(chat_id, message, buttons, bot, None)
    elif user_input == 'Repeat Learned Words':
        set_activity(user, 'words repeating')
        send_word_to_user_for_repeating(chat_id, bot, user)
    elif user_input == 'Is Learned':
        mark_word_as_ready_for_exam(user)
        send_word_to_user_for_repeating(chat_id, bot, user)
    elif user_input == 'Next':
        send_word_to_user_for_repeating(chat_id, bot, user)
    else:
        message = ""
        buttons = ['Cancel']
        check_user_answer_exam(chat_id, bot, user, user_input)
        send_message_with_buttons(chat_id, message, buttons, bot, None)


bot.polling(none_stop=True)


