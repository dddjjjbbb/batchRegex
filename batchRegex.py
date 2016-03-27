#!/usr/bin/env python

''' Depending on commmand line args, script applies set of Regex Patterns to all files. Will traverse dirctory tree. '''

import os.path
from os import walk
import re
import fnmatch
import argparse


def placeholder(line):
    return re.sub(r'<\?rh-placeholder(.+?)\?>', r'<rh_placeholder\1/>', line)


def condition(line):
    return re.sub(
        r'<\?rh-cbt_start (condition=".+?").\?>',
        r'<rh-cbt \1>',
        line)


def end(line):
    return re.sub(r'<\?(rh-cbt_end) \?>', '</rh-cbt>', line)

PREPROCESS_FUNCTIONS = [placeholder, condition, end]


def revertPlaceholder(line):
    return re.sub(r'<rh_placeholder(.+?)/>', r'<?rh-placeholder\1?>', line)


def revertCondition(line):
    return re.sub(r'<rh-cbt (condition=".+?")>', r'<?rh-cbt_start \1 ?>', line)


def revertEnd(line):
    return re.sub(r'</rh-cbt>', r'<?rh-cbt_end ?>', line)


POSTPROCESS_FUNCTIONS = [revertPlaceholder, revertCondition, revertEnd]


def preprocess(line):
    for operation in PREPROCESS_FUNCTIONS:
        line = operation(line)
    return line


def postprocess(line):
    for operation in POSTPROCESS_FUNCTIONS:
        line = operation(line)
    return line


def main():

    parser = argparse.ArgumentParser(
        description="Specify which Regex patterns")
    parser.add_argument(
        "--pre",
        help="applies regex patterns for pre-process, specify folder name")
    parser.add_argument(
        "--post",
        help="applies regex patterns for post-process, specify folder name")
    args = parser.parse_args()

    if args.pre == args.post:
        print("cannot apply both sets of regex patterns at once")
        return

        action = ''
    if args.pre:
        action = preprocess
        directory = args.pre
    if args.post:
        action = postprocess
        directory = args.post

    for dirName, subdirlist, filelist in walk("."):
        for filename in filelist:
            if fnmatch.fnmatch(filename, "*.html"):
                execute(os.path.join(dirName, filename), action)

if __name__ == '__main__':
    main()
