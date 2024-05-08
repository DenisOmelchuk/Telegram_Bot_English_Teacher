import telebot
from database_functions import record_last_given_word, get_new_word_from_db, get_word_for_exam, get_right_answer, \
    mark_word_as_learned, exam_fail, get_word_for_repeating
from new_word import get_word_data, get_word_data_exam


def send_message_with_buttons(chat_id, message_text, buttons, bot, audio_path):
    markup = telebot.types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    for button_text in buttons:
        markup.add(telebot.types.KeyboardButton(button_text))
    if message_text:
        bot.send_message(chat_id, message_text, reply_markup=markup, parse_mode='Markdown')
    if audio_path:
        with open(audio_path, 'rb') as audio:
            bot.send_audio(chat_id, audio, reply_markup=markup)


def send_word_to_user_learning(chat_id, bot, user):
    word = get_new_word_from_db(user.username)
    buttons = ['Add to learning', 'Already know', 'Repeat Learned Words', 'Exam']
    audio_path, word_data = get_word_data(word[0])
    record_last_given_word(user, word[0])
    send_message_with_buttons(chat_id, word_data, buttons, bot, audio_path)


def send_word_to_user_for_repeating(chat_id, bot, user):
    word = get_word_for_repeating(user.username)
    if word:
        buttons = ['Is Learned', 'Cancel', 'Next']
        audio_path, word_data = get_word_data(word[0])
        record_last_given_word(user, word[0])
        send_message_with_buttons(chat_id, word_data, buttons, bot, audio_path)
    else:
        buttons = ['Learn New Word', 'Exam', 'Repeat Learned Words']
        message = 'All words are learned, add new words or exam yourself!'
        send_message_with_buttons(chat_id, message, buttons, bot, None)


def send_word_to_user_examination(chat_id, bot, user):
    word = get_word_for_exam(user.username)
    if word:
        buttons = ['Cancel']
        word_data = get_word_data_exam(word[0])
        record_last_given_word(user, word[0])
        send_message_with_buttons(chat_id, word_data, buttons, bot, None)
    else:
        buttons = ['Learn New Word', 'Repeat Learned Words']
        message = 'All words are examined, Congratulations!'
        send_message_with_buttons(chat_id, message, buttons, bot, None)


def check_user_answer_exam(chat_id, bot, user, user_answer):
    right_answer = get_right_answer(user.last_given_translation_id)
    if right_answer == user_answer.lower():
        mark_word_as_learned(user.username, user.last_given_translation_id)
        send_word_to_user_examination(chat_id, bot, user)
    else:
        message = 'Answer is wrong. Please try again.'
        buttons = ['Cancel']
        exam_fail(user.username, user.last_given_translation_id)
        send_message_with_buttons(chat_id, message, buttons, bot, None)













