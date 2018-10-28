import sys
import scrython
from scrython import *
import re

def format_args(string, f):
    f.write('\n## Args\n\n|arg|type|description|\n|:---:|:---:|:---:|')

    arg_list = re.findall(r'(\w*\s*\(\w+[,\s\w]{1,}\):[\w\s\'\\`,.]*[^\w\s\(])', string)

    for arg in arg_list:
        arg_name = re.findall(r'[^\s]*', arg)[0]

        description = re.findall(r'(?<=:\s)(.*)', arg)[0]

        type_and_optional = re.findall(r'(?<=\()\w+[,\s\w]+(?=\))', arg)[0]

        if len(type_and_optional) > 1:
            f.write('|{}|{}|{}|\n'.format(arg_name, type_and_optional, description))

        else:
            f.write('|{}|{}|{}|\n'.format(arg_name, type_and_optional, description))

def format_returns(string, f):
    f.write('\n## Returns\n{}\n'.format(string.strip()))

def format_raises(string, f):

    f.write('\n## Raises\n\n|exception type|reason|\n|:---:|:---:|')

    exception_list = re.findall(r'\w+:[\w\s\\\']+[^\s\w:]', string)

    for exception in exception_list:
        exception_name = re.findall(r'[^:]*', exception)[0]

        exception_description = re.findall(r'(?<=:\s)([\w\s\.\'\\]*)', exception)[0]

        f.write('|{}|{}|\n'.format(exception_name, exception_description))

def format_examples(string, f):

    example_list = re.findall(r'>{3}[\s\w=.("+:,)]+', string)

    f.write('\n## Examples\n')
    f.write('```\n{}\n```'.format('\n'.join(example_list)))

for _class in scrython.__all__:

    intro = """
These docs will likely not be as detailed as the official Scryfall Documentation, and you should reference that for more information.

>In the event that a key isn't found or has been changed, you can access the full JSON output with the `scryfallJson` variable (`{}().scryfallJson`).
""".format(eval(_class).__name__)

    class_docstring = repr(re.sub(r'\n+', '', eval(_class).__doc__)) # removes newlines

    remove_extra_spaces = re.sub(' +', ' ', class_docstring)

    args = re.findall(r'(?<=Args:)(.*)(?=Returns:)', remove_extra_spaces)[0]

    returns = re.findall(r'(?<=Returns:)(.*)(?=Raises:)', remove_extra_spaces)[0]

    raises = re.findall(r'(?<=Raises:)(.*)(?=Examples:)', remove_extra_spaces)[0]

    examples = re.findall(r'(?<=Examples:)(.*)', remove_extra_spaces)[0]

    with open('{}.md'.format(_class), 'w') as f:
        f.write('# **class** `{}()`\n'.format(_class))
        f.write(intro)
        format_args(args, f)
        format_returns(returns, f)
        format_raises(raises, f)
        format_examples(examples, f)

    break


    # match = list(filter(None, (token.strip() for token in re.findall(r'[^\n]*', eval(_class).__doc__))))

    # with open('{}.md'.format(eval(_class).__name__), 'w') as f:
    #     f.write('# **class** `{}()`\n'.format(eval(_class).__name__))
    #     f.write(intro)
    #     for token in match:
    #         if re.findall(r'[A-Z][a-z].*:', token) and ':' in re.findall(r':.*', token): # Match section header
    #             f.write('\n\n## {}\n\n'.format(token.replace(':', '')))
    #             if 'Example' in token:
    #                 f.write(token)
    #             else:
    #                 f.write('| arg | description |\n|:---:|:---:|')
    #         elif re.findall(r'[\w]+\s\(.+\):', token): # Match args description
    #             if 'Defaults' in token:
    #                 f.write(token)
    #             else:
    #                 f.write('\n|{}|'.format(token))
    #         else:
    #             f.write('\n|{}|'.format(token))
    break
