def get_word_data(word):
    examples = [example.example for example in word.examples]
    ru_examples = [example.ru_example for example in word.examples]

    word_type = word.word_type if word.word_type is not None else ''
    type_description = f'({word.type_description})' if word.type_description is not None else ''
    word_data = f'*{word.word.word}*   _{word_type}_   _{type_description}_\n\n'
    if word.description:
        word_data += (f'_{word.description}_\n'
                      f'_{word.ru_description}_\n')
    word_data += f'*{word.translation}*\n\n'
    if examples:
        word_data += 'Примеры:\n'
        for index, example in enumerate(examples):
            word_data += (f'_{index + 1}: {example}_\n'
                          f'_{ru_examples[index]}_')
    audio_path = f'audio/{word.word.word}_{word.word_type}.mp3'
    return audio_path, word_data


def get_word_data_exam(word):
    ru_examples = [example.ru_example for example in word.examples]

    word_type = f'({word.word_type})' if word.word_type is not None else ''
    ru_description = word.ru_description if word.ru_description is not None else ''
    word_data = (f'*{word.translation}*   _{word_type}_\n\n'
                 f'{ru_description}\n')
    if ru_examples:
        word_data += '_Примеры:_\n'
        for index, ru_example in enumerate(ru_examples):
            word_data += f'_{index + 1}: {ru_example}_'
    return word_data
