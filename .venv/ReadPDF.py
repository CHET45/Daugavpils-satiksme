# importing required classes
"""
from pypdf import PdfReader
def extractTimetable(lines):
    lines = lines.splitlines()
    timetable = {}  # hour:[minutes,minutes]
    for line in lines:
        hour = line[0:3]
        minutes = []
        minute = ""
        for m in line[3:len(line) + 1]:
            minute += m
            if len(minute) == 2:
                minutes.append(minute)
                minute = ""
        timetable[hour] = minutes
    return timetable
# creating a pdf reader object
def CreateTimetables(page):

    #
    reader = PdfReader('satiksme.pdf')
    page = reader.pages[0]
    #

    text=page.extract_text()
    lines=text[text.index('StacijaDARBA DIENAS')+len("StacijaDARBA DIENAS")+3:text.index('BRĪVDIENAS')]
    WorkdayTimetable=extractTimetable(lines)#hour:[minutes,minutes]

    lines=text[text.index('BRĪVDIENAS')+len("BRĪVDIENAS")+3:text.index('BUT Ļ EROVA IELA  1234567 Druka ̄t')]
    HolydayTimetable=extractTimetable(lines)#hour:[minutes,minutes]
"""
print("ķ".encode("utf-8"))