import argparse
from services import read_file, WhatsAppChat, ChatAnalyzer, TextProcessor, Lang, Source


def main(chat_path, source, lang, save=False, out_name=None, out_path=None):
    content = read_file(chat_path)

    wp = WhatsAppChat(content, text_processor=TextProcessor(source, lang=lang))

    ca = ChatAnalyzer(wp, save=save, files_name=out_name, out_folder=out_path)

    ca.get_summary()
    ca.get_date_distribution()
    ca.top_10_date_distributions()
    ca.get_day_distribution()
    ca.get_sender_distribution()
    ca.get_top10_word_distribution()
    ca.get_top10_emoji_distribution()
    ca.get_word_cloud()
    ca.save_report()


def parse_args():
    parser = argparse.ArgumentParser(description='Whatapp analysis input parser')
    parser.add_argument('path',
                        help='relative or absolute path to the chat')
    parser.add_argument('--os', '-i',
                        help='smartphone os used to export chat.Valid value are \'ios\' (default) or \'android\'.',
                        default="ios", choices=['ios', 'android'])
    parser.add_argument('--lang', '-l',
                        help='Chat language.Valid value are \'it\' for italian (default) or \'en\' for english.',
                        default="it", choices=['it', 'en'])
    parser.add_argument('--save', '-s', action='store_const',
                        help='Save result in output_path',
                        default=False, const=True)
    parser.add_argument('--output_name', '-o',
                        help='Output name of generated files. Default is current long timestamp',
                        default=None)
    parser.add_argument('--output_path', '-p',
                        help='Output path of generated files. Default \'plot/\'',
                        default="plot")
    return parser.parse_args()


if __name__ == "__main__":

    args = parse_args()

    os_name = Source.IOS if args.os == 'ios' else Source.ANDROID
    lang = Lang.IT if args.lang == 'it' else Lang.EN
    save_result = bool(args.save)
    output_name = args.output_name if save_result else None
    output_path = args.output_path if save_result else None
    main(args.path, os_name, lang, save_result, output_name, output_path)


