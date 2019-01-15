#!/usr/bin/python3

import sys
import getopt

def usage():
    print("delc [-h] [-s count] file ...")
    print("options:")
    print("-h | --help: print this")
    print("-s | --skip count: delc will skip the 'count' first lines")
    print("to avoid removing any header")

def skip_quotes(quote, content, j):
    j += 1
    while content[j] != quote:
        if content[j] == '\\':
            j += 2
        else:
            j += 1
    return j

def skip_c_com(content, j, file_len, name):
    exit = content[j + 2 :].find("*/")
    if exit == -1:
        print("delc: error: unterminated C style comment in '" + name + "'")
        return content, -1
    else:
        return content[:j] + content[j + exit + 4:], file_len - exit - 4

def skip_cpp_com(content, j, file_len):
    exit = content[j + 2 :].find('\n')
    while exit != -1 and content[j + 2 + exit - 1] == '\\':
        tmp = content[j + 2 + exit + 1:].find('\n')
        if tmp == -1:
            exit = tmp
        else:
            exit += tmp + 1
    if exit == -1:
        return content[:j], file_len - 2
    return content[:j] + content[j + exit + 2:], file_len - exit - 2

def rm_whites(content, j, file_len):
    whites = 0
    while j >= whites + 1 and content[j - whites - 1] != '\n' and content[j - whites - 1].isspace():
        whites += 1
    if j >= whites + 1 and content[j - whites - 1] == '\n':
        whites += 1
    if whites == 0:
        return content, file_len, j
    else:
        return content[:j - whites] + content[j:], file_len - whites, j - whites

# skip is set to 12 by default to avoid removing the 42 header
skip = 12
try:
    opts, args = getopt.getopt(sys.argv[1:], "hs:", ["help", "skip"])
except getopt.GetoptError as err:
    print(str(err))
    sys.exit(2)
for o, a in opts:
    if o in ("-h", "--help"):
        usage()
        if len(args) == 0:
            sys.exit()
    elif o in ("-s", "--skip"):
        skip = int(a)
        if skip < 0:
            print("delc: error: the number of lines to skip can't be negative")
            sys.exit(2)
if len(args) == 0:
    print("delc: error: no input file")
    sys.exit(2)

for i in range(0, len(args)):
    name = str(args[i])
    file = open(name)

    content = ""
    j = 0
    for line in file:
        if skip > 0:
            j += len(line)
            skip -= 1
        content = content + line

    file_len = len(content)
    while j < file_len:
        if content[j] == '/':
            if content[j + 1] == '*':
                content, file_len = skip_c_com(content, j, file_len, name)
            elif content[j + 1] == '/':
                content, file_len = skip_cpp_com(content, j, file_len)
            if file_len != -1 and content[j] == '\n':
                content, file_len, j = rm_whites(content, j, file_len)
        elif content[j] == '\'' or content[j] == '"':
            j = skip_quotes(content[j], content, j) + 1
        else:
            j += 1
    new = open(name, mode="w")
    new.write(content)
    new.close()
