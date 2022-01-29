# WhatsApp Chat Analysis

Simple WhatsApp chat analyzer written in Python.

Script run the following analysis:

- Summary (num of message, senders, top sender, top day)
- Line plot with number of message per date
- Bar plot with the top 10 date
- Bar plot with number of message per dat (Mon, Tue, ...)
- Bar plot with number of message per sender
- Bar plot with the top 10 word used
- Bar plot with the top 10 emoji uses
- word cloud

Note: it would seem that the export format differs from apple and android. There is a parameter to cofigure the os used.

### Install

Just install python package found in requirements.txt and enjoy

```
pip install -r requirements.txt
```

### Run

To run use *main.py* file.

Parameters:
```
positional arguments:
  path                  relative or absolute path to the chat

optional arguments:
  -h, --help            show this help message and exit
  --os {ios,android}, -i {ios,android}
                        smartphone os used to export chat.Valid value are
                        'ios' (default) or 'android'.
  --lang {it,en}, -l {it,en}
                        Chat language.Valid value are 'it' for italian
                        (default) or 'en' for english.
  --save, -s            Save result in output_path
  --output_name OUTPUT_NAME, -o OUTPUT_NAME
                        Output name of generated files. Default is current
                        long timestamp
  --output_path OUTPUT_PATH, -p OUTPUT_PATH
                        Output path of generated files. Default 'plot/'
```

Example:

```
python main.py path/my_chat.txt
```


### How to export Whatsapp chat

[Apple](https://www.easeus.com/iphone-data-transfer/export-whatsapp-chat.html)

[Android](https://faq.whatsapp.com/android/chats/how-to-save-your-chat-history/?lang=it)


### Author 
Cavallo Giacomo [Linkedin](https://www.linkedin.com/in/giacomo-cavallo-b29516157/)

