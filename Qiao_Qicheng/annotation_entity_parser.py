import numpy as np
import os
import re

ANNOTATION_FILE = "./annotations"
TEMP_FILE = "./quality_txt_resources/temp.txt"
OUT_FILE = "./quality_txt_resources/annotation_entities.txt"
FILE_LIST = [f for f in os.listdir(ANNOTATION_FILE) if os.path.isfile(os.path.join(ANNOTATION_FILE, f))]


#rex list
IP_REX = "\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}"
ARG_REX = "Arg\d:T\d"
DATE_REX = "\d+\/\d+\/\d+"
DATE2_REX = "\d+\-\d+\-\d+"
DATE3_REX = r"(Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)\s+(\d{1,2})*\s*(\d{4})"
SHA64_REX = "\w{16}\n"
HEX_REX = "(\w{2}\s){8}"
RELATION_REX = r"\bT{1}\d*\s"
URL_REX = "uri!\d*"
HTTP_REX = "http:\/\/\d*"
APP_NAME_REX = r"\[*\.\]*\w{1,3}\b"
TIME_REX = "\d{2}:\d{2}:*\d*"
ARG3_REX ="Arg2:\d*"
WEB_REX = ".*\..*\..*"
PATH_REX = "\w*\\\w*"
PATH2_REX = "\w*\/\w*"
EDGE_REX = "\w*[.|:]"
PURE_SYMBOL_REX = "\B\W\W\W"
DOT_REX = "\[dot\]"

#wired rex list
DOT_REX = ""


def parse_one_file(file, out):
    with open(os.path.join(ANNOTATION_FILE,file), 'r') as f:
        lines = f.readlines()

    for line in lines:
        temp = line.split('\t')
        out.write(temp[-1])

        # print(temp[-1])

def get_raw_text():
    f = open(TEMP_FILE, "w")
    # parse_one_file(FILE_LIST[0], f)
    for file in FILE_LIST:
        parse_one_file(file, f)
    f.close()

def check(line):
    return re_check(IP_REX, line) or re_check(ARG_REX, line) or re_check(ARG3_REX, line) or re_check(DATE_REX, line) or re_check(DATE2_REX, line) or re_check(SHA64_REX, line) \
           or re_check(HEX_REX, line) or re_check(RELATION_REX, line) or re_check(URL_REX,line) or re_check(HTTP_REX, line) or re_check(APP_NAME_REX, line) or re_check(TIME_REX, line) or re_check(WEB_REX, line)\
            or re_check(PATH_REX, line) or re_check(EDGE_REX, line) or re_check(PATH2_REX, line) or re_check(PURE_SYMBOL_REX, line) or re_check(DOT_REX, line) or re_check(DATE3_REX, line)


def re_check(rex, line):
    res = re.search(rex, line)
    if res:
        print("removed", res.string)
        return True

def parse_temp_file():
    with open(TEMP_FILE, 'r') as f:
        lines = f.readlines()

    f = open(OUT_FILE, "w")
    for l in lines:
        if not l=='\n':
            if not check(l):
                f.write(l)
    f.close()

if __name__ == '__main__':
    get_raw_text() #parse out entity
    parse_temp_file() #rex out

