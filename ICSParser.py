import os
from sys import platform

LESSONS = ['BI7-Binf', 'BI7-Life_science', 'BI3-Wiskunde', 'BI3-Binf']


def readfile(file):
    content = []
    with open(file) as f:
        for line in f:
            content.append(line)
    return content


def parser(content):
    processedContent = [content[0], content[1], content[2]]
    for lesson in LESSONS:
        toSearch = "SUMMARY:" + lesson + "\n"
        # find all occurences of the current lesson in the current file
        # indices contains the indexes of all SUMMARY: lines containing the current lesson
        indices = [i for i, x in enumerate(content) if x == toSearch]
        for index in indices:
            # Find first "BEGIN:VEVENT\n" in front of "SUMMARY:lesson\n"
            for i in range(index, 0, -1):
                if content[i] != "BEGIN:VEVENT\n":
                    continue
                else:
                    break
            eventStart = i
            # Find first "END:VEVENT\n" after "SUMMARY:lesson\n"
            for i in range(index, len(content)):
                if content[i] != "END:VEVENT\n":
                    continue
                else:
                    break
            eventEnd = i + 1
            description = "DESCRIPTION:"
            for i in range(eventStart, eventEnd):
                if content[i].startswith("ATTENDEE;"):
                    description += content[i].split(';')[1].split(':')[0]
                elif content[i].startswith("SEQUENCE:"):
                    processedContent.append(description + '\n')
                processedContent.append(content[i])
    processedContent.append("END:VCALENDAR\n")
    return processedContent


def main():
    print("ICSParser - Made by a genius")
    path = os.getcwd()
    toBeProcessed = []
    outexists = False
    if "out" in os.listdir():
        outexists = True
    for entry in os.listdir():
        if entry.endswith(".ics"):
            toBeProcessed.append(entry)

    print("Found " + str(len(toBeProcessed)) + " files to be processed.")
    if not outexists:
        os.mkdir('out')
    if platform == 'linux':
        outpath = path + "/out"
    else:
        outpath = path + "\\out"
    print(outpath)
    for file in toBeProcessed:
        print("Processing file: " + file)
        fileContent = readfile(file)
        processedContent = parser(fileContent)
        if platform == 'linux':
            writepath = outpath + "/" + file
        else:
            writepath = outpath + "\\" + file
        print("Writing to file: out/" + file)
        with open(writepath, 'w') as f:
            f.writelines(processedContent)


if __name__ == '__main__':
    main()
