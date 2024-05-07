import os
import replicate
from database_functions import get_known_words
from prompts import create_sentence_prompt


os.environ["REPLICATE_API_TOKEN"] = "Your replicate API key"


def get_sentence():
    words = get_known_words()
    prompt = create_sentence_prompt + words
    sentence = ''
    for event in replicate.stream(
        "meta/meta-llama-3-70b-instruct",
        input={
            "prompt": prompt,
            "system_prompt": "You are a professional English - Russian teacher",
        }
    ):
        sentence += str(event)
    return sentence


