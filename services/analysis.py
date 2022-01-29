from . import WhatsAppChat
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import math
from wordcloud import WordCloud
import time
import os
from prettytable import PrettyTable


class ChatAnalyzer(object):

    def __init__(self, chat, save=False, files_name=None, out_folder=None):
        if type(chat) is not WhatsAppChat:
            raise ValueError("Invalid chat type")

        self.chat = chat
        self.save = save

        if self.save:
            self.file_name, self.out_folder = __class__.prepare_output(files_name, out_folder)
            self.report_content = []

    @staticmethod
    def prepare_output(files_name, out_folder):
        files_name = files_name if files_name is not None else str(round(time.time() * 1000))
        out_folder = out_folder if out_folder is not None else "plot"

        if not os.path.exists(out_folder):
            os.mkdir(out_folder)

        return files_name, out_folder

    def get_summary(self):
        senders_frequency = self.chat.df.sender.value_counts()

        days_frequency = self.chat.df.apply(lambda row: row.date.date(), axis=1).value_counts()

        summary = {
            "message_numbers": len(self.chat.df),
            "senders": list(senders_frequency.index),
            "best_sender": (senders_frequency.index[0], senders_frequency.values[0]),
            "best_day": (days_frequency.index[0], days_frequency.values[0])
        }

        header = summary.keys()
        columns = [[v] for v in summary.values()]
        self._create_result_tables("SUMMARY", header, *columns)

        return summary

    def get_date_distribution(self):
        date_frequency = self.chat.df.apply(lambda row: row.date.date(), axis=1).value_counts(sort=False)

        x = list(range(len(date_frequency.index)))
        y = date_frequency.values

        fig = plt.figure(figsize=(15, 5))
        ax = fig.add_subplot(1, 1, 1)

        ax.plot(x, y)
        ax.set_ylabel('Messages')
        ax.set_xlabel('Date')
        ax.set_title('Message per date distribution')
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d/%Y'))
        # set labels
        label_skip = 1
        if len(x) > 24:
            label_skip = math.ceil(len(x)/24)

        ax.set_xticks([idx for idx in range(len(x)) if idx % label_skip == 0],
                      [idx for i, idx in enumerate(date_frequency.index) if i % label_skip == 0], rotation=90)

        fig.autofmt_xdate()

        self._display("date_distribution")
        self._create_result_tables("DATE DISTRIBUTION", ["Date", "Message"], date_frequency.index, y)

        return list(zip(date_frequency.index, y))

    def top_10_date_distributions(self):
        date_frequency = self.chat.df.apply(lambda row: row.date.date(), axis=1).value_counts().iloc[:10]

        index = list(range(len(date_frequency.index)))

        fig = plt.figure(figsize=(10, 5))
        ax = fig.add_subplot(1, 1, 1)

        ax.bar(index, date_frequency.values, color='#d62728')

        ax.set_ylabel('Messages')
        ax.set_xlabel('Day')
        ax.set_title('Message per days distribution')

        ax.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d/%Y'))
        ax.set_xticks(index, date_frequency.index)
        fig.autofmt_xdate()

        self._display("top10_date_distribution")
        self._create_result_tables("TOP 10 DATE DISTRIBUTION", ["Date", "Message"],
                                   date_frequency.index, date_frequency.values)

        return list(zip(date_frequency.index, date_frequency.values))

    def get_day_distribution(self):
        day_frequency = self.chat.df.day.value_counts()

        day_name = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        day_count = [day_frequency[d] for d in day_name]

        index = list(range(len(day_name)))

        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)

        ax.bar(index, day_count, color='#d62728')

        ax.set_ylabel('Messages')
        ax.set_xlabel('Day')
        ax.set_title('Message per days distribution')
        ax.set_xticks(index, day_name)

        self._display("day_distribution")

        self._create_result_tables("DAY DISTRIBUTION", ["Day", "Message"], day_name, day_count)

        return list(zip(day_name, day_count))

    def get_sender_distribution(self):
        sender_frequency = self.chat.df.sender.value_counts()

        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)

        ax.bar(sender_frequency.index, sender_frequency.values, color='#d62728')

        ax.set_ylabel('Messages')
        ax.set_xlabel('Sender')
        ax.set_title('Message per sender')

        fig.autofmt_xdate()

        self._display("sender_distribution")
        self._create_result_tables("SENDER DISTRIBUTION", ["Sender", "Message"],
                                   sender_frequency.index, sender_frequency.values)

        return list(zip(sender_frequency.index, sender_frequency.values))

    def get_top10_word_distribution(self):

        def text_filter(row): return not row.is_media and len(row.tokens) > 0

        word_frequency = \
            self.chat.df[self.chat.df.apply(text_filter, axis=1)] \
                .apply(lambda row: row.tokens.split(","), axis=1) \
                .explode().value_counts()[:10]

        fig = plt.figure(figsize=(10, 5))
        ax = fig.add_subplot(1, 1, 1)

        ax.bar(word_frequency.index, word_frequency.values, color='#d62728')

        ax.set_ylabel('Frequency')
        ax.set_xlabel('Word')
        ax.set_title('Word frequency')
        fig.autofmt_xdate()

        self._display("top10_word_distribution")
        self._create_result_tables("TOP 10 WORD FREQUENCY", ["Word", "Frequency"],
                                   word_frequency.index, word_frequency.index)

        return list(zip(word_frequency.index, word_frequency.values))

    def get_top10_emoji_distribution(self):

        def emoji_filter(row): return not row.is_media and len(row.emoji_name)>0

        emoji_frequency = \
            self.chat.df[self.chat.df.apply(emoji_filter, axis=1)] \
                .apply(lambda row: row.emoji_name.split(","), axis=1) \
                .explode().value_counts()[:10]

        if self.save:
            pass

        fig = plt.figure(figsize=(10, 5))
        ax = fig.add_subplot(1, 1, 1)

        ax.bar(emoji_frequency.index, emoji_frequency.values, color='#d62728')

        ax.set_ylabel('Frequency')
        ax.set_xlabel('Emoji')
        ax.set_title('Emoji frequency')
        fig.autofmt_xdate()

        self._display("top10_emoji_distribution")
        self._create_result_tables("TOP 10 EMOJI FREQUENCY", ["Emoji Name", "Frequency"],
                                   emoji_frequency.index, emoji_frequency.values)

        return list(zip(emoji_frequency.index, emoji_frequency.values))

    def get_word_cloud(self):

        def text_filter(row): return not row.is_media and len(row.tokens) > 0

        word_frequency = \
            self.chat.df[self.chat.df.apply(text_filter, axis=1)] \
                .apply(lambda row: row.tokens.split(","), axis=1) \
                .explode().value_counts()

        frequency_dict = dict(word_frequency)

        wordcloud = WordCloud().generate_from_frequencies(frequency_dict)
        plt.figure(figsize=(20, 10))
        plt.imshow(wordcloud, interpolation="bilinear")
        plt.axis("off")
        self._display("word_cloud")

    def save_report(self):
        if not self.save:
            return

        report_path = "%s/%s_%s.txt" % (self.out_folder, self.file_name, "report")
        report_content = "".join(["%s\n%s\n\n" % (name, table) for name, table in self.report_content])

        with open(report_path, "w") as f:
            f.write(report_content)

    def _display(self, graph_name=None):
        if self.save:
            plot_path = "%s/%s_%s.png" % (self.out_folder, self.file_name, graph_name)
            plt.savefig(plot_path, bbox_inches='tight')
        else:
            plt.show()

    def _create_result_tables(self, name, headers, *args):
        if len(headers) != len(args):
            raise ValueError("Headers and number of args must be the same")

        t = PrettyTable()
        for h, col in zip(headers, args):
            t.add_column(h, col)

        if self.save:
            self.report_content.append((name, t.get_string()))
        else:
            print("%s\n%s\n\n" % (name, t.get_string()))

        return t

