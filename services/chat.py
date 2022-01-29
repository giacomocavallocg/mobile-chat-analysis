import re
import pandas as pd
from .text_processor import TextProcessor
from .utils import parse_datetime


class WhatsAppChat(object):

    def __init__(self, chat_content, text_processor=TextProcessor()):
        self.raw = chat_content
        self.text_processor = text_processor
        self.df = self._process_raw_data()

    def _process_raw_data(self):
        """
        messages = re.findall('(\d{2}\/\d{2}\/\d{2})(?:, )(\d{2}:\d{2})(?: - )([a-zA-Z0-9_ ]+)(?:: )(.*)', self.raw)

        messages = \
            re.findall('(?:\\[)(\\d{2}/\\d{2}/\\d{2})(?:, )(\\d{2}:\\d{2}:\\d{2})(?:\\])([a-zA-Z0-9_ ]+)(?:: )(.*)',
                       self.raw)
        """

        messages = self.text_processor.read_messages(self.raw)
        data = list()
        for m in messages:
            data.append(self._process_message(m))

        return pd.DataFrame(data)

    def _process_message(self, raw_message):
        date, time, sender, message_text = raw_message

        dt, day = self.text_processor.parse_datetime(date, time)
        message_text = self.text_processor.remove_link(message_text)
        is_media = self.text_processor.is_media(message_text)
        if not is_media:
            token, emoj, emoj_name = self.text_processor.parse_text(message_text)
        else:
            token, emoj, emoj_name = [], [], []

        return {
            "date": dt,
            "day": day,
            "sender": sender,
            "tokens": ",".join(token),
            "emoji": ",".join(emoj),
            "emoji_name": ",".join(emoj_name),
            "is_media": is_media
        }

