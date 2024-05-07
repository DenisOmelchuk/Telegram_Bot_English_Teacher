from db_tables import db, LLAMAUserWords
from db_tables import User, UserWords, Translation, Example, Word
import peewee
from datetime import datetime, timedelta


def create_user(username):
    with db.connection_context():
        user = User.create(username=username)
        return user


def get_user(username):
    with db.connection_context():
        try:
            user = User.get(username=username)
            return user

        except:
            user = create_user(username)
            return user


def get_new_word_from_db(username):
    levels = ['A1', 'A2', 'B1', 'B2', 'C1', 'C2']
    for level in levels:
        try:
            word = (
                Translation
                .select()
                .join(Word)
                .where(~Translation.id.in_(
                    UserWords.select(UserWords.translation).where(UserWords.user == User.get(User.username == username))
                ))
                .where(Translation.level == level)
                .limit(1)
            )
            if word:
                return list(word)

        except peewee.PeeweeException as e:
            print("Error occurred:", e)
            return 0, []


def get_word_for_repeating(username):
    try:
        user_word_obj = (UserWords.select()
                         .where(
            (UserWords.user == User.get(User.username == username)) & (UserWords.in_studying == True) & (
                    UserWords.repeated_by_user == False))
                         .limit(1)
                         )
        if user_word_obj:
            translation_object_id = user_word_obj[0].translation.id
            translation = Translation.get(id=translation_object_id)
            user_word_obj[0].repeated_by_user = True
            user_word_obj[0].save()
            return [translation]
        else:
            user_word_objs = (UserWords.select()
            .where(
                (UserWords.user == User.get(User.username == username)) & (UserWords.in_studying == True)))
            if len(user_word_objs) > 0:
                for user_word_obj in user_word_objs:
                    user_word_obj.repeated_by_user = False
                    user_word_obj.save()
                return get_word_for_repeating(username)
            return None


    except peewee.PeeweeException as e:
        print("Error occurred:", e)
        return None


def get_word_for_exam(username):
    try:
        user_word_obj = (UserWords.select()
                         .where(
            (UserWords.user == User.get(User.username == username)) & (UserWords.is_learned == True))
                         .limit(1)
                         )
        if user_word_obj:
            translation_object_id = user_word_obj[0].translation.id
            translation = Translation.get(id=translation_object_id)
            return [translation]
        else:
            return None

    except peewee.PeeweeException as e:
        print("Error occurred:", e)
        return None


def get_right_answer(translation_id):
    translation_object = Translation.get(id=translation_id)
    right_answer = translation_object.word.word
    return right_answer


def get_user_word_object(username, translation_id):
    try:
        return UserWords.get(
            (UserWords.user == User.get(username=username)) &
            (UserWords.translation == Translation.get(id=translation_id))
        )
    except UserWords.DoesNotExist:
        return None


def mark_word_as_learned(username, translation_id):
    word = get_user_word_object(username, translation_id)
    if word:
        word.is_learned = False
        word.known_by_user = True
        word.exams_count += 1
        word.save()
        translation = Translation.get(id=translation_id)
        LLAMAUserWords.get_or_create(user=username, word=translation.word)
    else:
        print('Error occurred: mark_word_as_learned')


def exam_fail(username, translation_id):
    word = get_user_word_object(username, translation_id)
    if word:
        word.exams_count += 1
        word.count_exam_failed += 1
        word.save()
    else:
        print('Error occurred: exam_fail')


def record_last_given_word(user, translation):
    user.last_given_translation_id = translation.id
    user.save()


def add_word_to_learning(user):
    translation_id = user.last_given_translation_id
    UserWords.create(user=user, translation=translation_id, in_studying=True)
    user.count_words_in_studying += 1
    user.save()


def mark_word_as_known(user):
    translation_id = user.last_given_translation_id
    UserWords.create(user=user, translation=translation_id, known_by_user=True)
    translation = Translation.get(id=translation_id)
    LLAMAUserWords.get_or_create(user=user.username, word=translation.word)


def mark_word_as_ready_for_exam(user):
    translation_id = user.last_given_translation_id
    user_word_obj = get_user_word_object(user.username, translation_id)

    user.count_words_in_studying -= 1
    user.save()

    if user_word_obj:
        user_word_obj.is_learned = True
        user_word_obj.in_studying = False
        user_word_obj.date_of_exam = datetime.now() + timedelta(hours=24)
        user_word_obj.save()


def get_known_words(username):
    words = ''
    words_obj = (LLAMAUserWords
                 .select()
                 .join(Word, on=(Word.id == LLAMAUserWords.word))
                 .where(LLAMAUserWords.user == username))
    for word in words_obj:
        words += f'{word.word.word} [{word.count_of_use}], '
    return words


def set_activity(user, activity):
    user.activity = activity
    user.save()


def set_tense(user, tense):
    if user.tense == 'past' or user.tense == 'present' or user.tense == 'future':
        user.tense += f' {tense}'
    else:
        user.tense = tense
    user.save()

