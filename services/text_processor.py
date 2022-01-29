import emoji
import stop_words
import simplemma
from string import punctuation
from . import Lang, Source
import re
from datetime import datetime

lemmatizator = simplemma.lemmatize
tokenize = simplemma.simple_tokenizer
load_lemma_dict = simplemma.load_data
punctuation = punctuation.replace("@", "") + "’"


class TextProcessor(object):

    LINK_REGEX = r'(https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|' \
                 r'www\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|' \
                 r'https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9]+\.[^\s]{2,}|www\.[a-zA-Z0-9]+\.[^\s]{2,})'

    IOS_CHAT_REGEX = r'(?:\[)(\d{2}/\d{2}/\d{2})(?:, )(\d{2}:\d{2}:\d{2})(?:\])([a-zA-Z0-9_ ]+)(?:: )(.*)'
    ANDROID_CHAT_REGEX = r'(\d{2}\/\d{2}\/\d{2})(?:, )(\d{2}:\d{2})(?: - )([a-zA-Z0-9_ ]+)(?:: )(.*)'

    def __init__(self, source=Source.IOS, lang=Lang.IT, lemmatize=False):

        if type(lang) is not Lang:
            raise ValueError("lang param must be Lang")
        elif lang is Lang.IT:
            lang_key = "it"
            self.media_str = ["\u200eimmagine omessa", "\u200evideo omesso", "\u200eGIF esclusa", "<Media omessi>"]
        elif lang is Lang.EN:
            lang_key = "en"
            self.media_str = ["\u200eimmagine omessa", "\u200evideo omesso", "\u200eGIF esclusa", "<Media omessi>"]
        else:
            raise ValueError("Unsupported lang %s" % str(lang))

        self.source = source
        self.lang = lang
        self.stop_word = stop_words.get_stop_words(lang_key)
        self.emoj_to_unicode = emoji.UNICODE_EMOJI[lang_key]
        self.lemma_dict = load_lemma_dict(lang_key) if lemmatize else None

    def read_messages(self, raw_chat):
        rex = __class__.ANDROID_CHAT_REGEX if self.source == Source.ANDROID else __class__.IOS_CHAT_REGEX
        return re.findall(rex, raw_chat)

    def parse_text(self, text):
        clean_text = ""
        emj = []
        emj_name = []
        for i in range(len(text)):
            c = text[i]
            if text[i] in punctuation:
                c = " "
            elif emoji.is_emoji(text[i]):
                emj.append(text[i])
                emj_name.append(self.emoj_to_unicode[text[i]])
                c = " "
            clean_text += c

        token = []
        for w in tokenize(clean_text):

            fixed_w = lemmatizator(w.lower(), self.lemma_dict) if self.lemma_dict else w.lower()
            if fixed_w not in self.stop_word and not fixed_w.startswith("@"):
                token.append(fixed_w)

        return token, emj, emj_name

    def is_media(self, text):
        return text in self.media_str

    def parse_datetime(self, date, time):
        date_format = '%d/%m/%y %H:%M' if self.source == Source.ANDROID else "%d/%m/%y %H:%M:%S"
        dt = datetime.strptime(" ".join((date, time)), date_format)
        day = dt.strftime("%a")
        return dt, day

    @staticmethod
    def remove_link(text):
        return re.sub(__class__.LINK_REGEX, " ", text)
