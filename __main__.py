import argparse
import pyperclip
import sys

from .pretty import *
from ast import literal_eval
from pathlib import Path


parser = argparse.ArgumentParser(
    prog='python -m pretty',
    # usage='%(prog)s [-h] [-i INDENT] [-inch INCH] [-nlch NLCH] [[[-f FILE | [[-ff SCR] [-tf DST]]] | [-c | [[-fc] [-tc]]]] | input]',
    formatter_class = argparse.ArgumentDefaultsHelpFormatter)

input_arg = parser.add_argument(
                                nargs='?',
                                dest = 'input',
                                type = str,
                                default= '',
                                help = 'String to be evaluated',
                                )
format_group = parser.add_argument_group(title='format')

indent_arg = format_group.add_argument('-i', '--indent',
                                       dest = 'indent',
                                       type = int,
                                       default = pretty.indent,
                                       help = 'indent character'
                                       )

inch_arg = format_group.add_argument('-inch', '--indent_char',
                                     dest = 'inch',
                                     type = str,
                                     default = str(pretty.inch.encode())[1:],
                                     help = 'new line character'
                                     )

nlch_arg = format_group.add_argument('-nlch', '--new_line_char',
                                     dest = 'nlch',
                                     type = str,
                                     default = str(pretty.nlch.encode())[1:],
                                     help = 'indent character * indent'
                                     )

file_group = parser.add_argument_group(title = 'file')

file_arg = file_group.add_argument('-f', '--file',
                                   dest = 'file',
                                   help = 'File content as input and output.'
                                   )


from_file_arg = file_group.add_argument('-ff', '--from_file',
                                        dest = 'scr',
                                        help = 'File content as input.'
                                        )

to_file_arg = file_group.add_argument('-tf', '--to_file',
                                      dest = 'dst',
                                      help = 'Write formated input to file.'
                                      )

clip_group = parser.add_argument_group(title='clip')

clip_arg = clip_group.add_argument('-c', '--clip',
                                   dest = 'clip',
                                   action= 'store_true',
                                   help = 'Input from clipbord and otput to clipboard.'
                                   )

from_clip_arg = clip_group.add_argument('-fc', '--from_clip',
                                        dest = 'from_clip',
                                        action= 'store_true',
                                        help = 'Use copied text as input.'
                                        )


to_clip_arg = clip_group.add_argument('-tc', '--to_clip',
                                      dest = 'to_clip',
                                      action= 'store_true',
                                      help = 'Copy the output.'
                                      )

parser.add_mutually_exclusive_group()._group_actions.extend([input_arg, file_arg, clip_arg, from_file_arg, from_clip_arg])
parser.add_mutually_exclusive_group()._group_actions.extend([file_arg, clip_arg, to_file_arg, to_clip_arg])

args = parser.parse_args()
pprint(literal_eval(args.input))