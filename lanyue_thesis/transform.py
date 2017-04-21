import sys
import os

filename = sys.argv[1]

cur_str = ""

misc_template = "@Misc{name,\n \
title    = \"{%s}\",\n\
author   =  {%s},\n \
year     = {%s},\n \
howpublished = \"\url{%s}\",\n \
}\n"  

def process_str(s):
    #print "got ",s 
    index = s.find("http")
    if index == "-1":
        index = s.find("www")
    if index == "-1":
        print "ERROR"
        exit(-1)

    first_part = s[:index]
    second_part = s[index:]
    #print first_part
    #print second_part

    pindex = first_part.rfind(". ") 
    #print pindex, len(first_part)
    if (len(first_part) - pindex) <= 5:
        pindex = first_part.rfind(". ", 0, pindex - 1)

    #print pindex
    #print first_part[:pindex]
    #print first_part[(pindex +1):].strip()

    author = (first_part[:pindex]).title()
    title = first_part[(pindex +1):].strip()

    urlandyear = second_part
    url = urlandyear.split(",")[0]
    year = urlandyear.split(",")[1]
    print misc_template % (title, author, year, url)

for line in open(filename):
    line = line.strip()
    if line == "":
        process_str(cur_str)
        cur_str = ""
    else:
        cur_str += line
        

# Process final str
if (cur_str.strip() != ""):
    process_str(cur_str)

