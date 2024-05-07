import peewee

# Establish a connection to the SQLite database
db = peewee.SqliteDatabase('dictionary.db')


class Word(peewee.Model):
    word = peewee.CharField()

    class Meta:
        database = db


class Translation(peewee.Model):
    word = peewee.ForeignKeyField(Word, backref='translations', related_name='word_translations')
    translation = peewee.CharField(null=True)
    level = peewee.CharField(null=True)
    type_description = peewee.CharField(null=True)
    description = peewee.CharField(null=True)
    ru_description = peewee.CharField(null=True)
    word_type = peewee.CharField(null=True)
    audio_file_path = peewee.CharField(null=True)

    class Meta:
        database = db


class User(peewee.Model):
    username = peewee.CharField(max_length=34, primary_key=True)
    count_words_in_studying = peewee.IntegerField(default=0)
    count_words_for_exam = peewee.IntegerField(default=0)
    count_words_passed_exam = peewee.IntegerField(default=0)
    last_given_translation_id = peewee.IntegerField(default=0)
    eng_sentence = peewee.CharField(max_length=500)
    activity = peewee.CharField(max_length=50, null=True)
    tense = peewee.CharField(max_length=20, null=True)

    class Meta:
        database = db


class UserWords(peewee.Model):
    user = peewee.ForeignKeyField(User, backref='user_words', on_delete='CASCADE')
    translation = peewee.ForeignKeyField(Translation, backref='translation_users')
    count_exam_failed = peewee.IntegerField(default=0)
    in_studying = peewee.BooleanField(default=False)
    is_learned = peewee.IntegerField(default=False)
    date_of_exam = peewee.DateTimeField(null=True)
    known_by_user = peewee.BooleanField(default=False)
    exams_count = peewee.IntegerField(default=0)
    repeated_by_user = peewee.BooleanField(default=False)

    class Meta:
        database = db


class Example(peewee.Model):
    example = peewee.CharField()
    ru_example = peewee.CharField(null=True)
    translation = peewee.ForeignKeyField(Translation, backref='examples')

    class Meta:
        database = db


class LLAMAUserWords(peewee.Model):
    user = peewee.ForeignKeyField(User, backref='llama_user_words', on_delete='CASCADE')
    word = peewee.ForeignKeyField(Word, backref='llama_user_words')
    count_of_use = peewee.IntegerField(default=0)

    class Meta:
        database = db




