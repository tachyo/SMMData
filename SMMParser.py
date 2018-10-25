import SMMLevel
import SMMAuthor
import time
import datetime
import more_itertools as mit

themeDict = {
    "sb" : "mario_bros",
    "sb3": "mario_bros3",
    "sw" : "mario_world",
    "sbu": "mario_bros_u"
}

def typographyToInt(ty, percentage=False):
    digits = len(ty)-(3 if percentage else 1)
    num = 0
    for t in ty:
        if t.attrs['class'][1] == 'typography-1':
            num += 1 * (10 ** digits);
        if t.attrs['class'][1] == 'typography-2':
            num += 2 * (10 ** digits);
        if t.attrs['class'][1] == 'typography-3':
            num += 3 * (10 ** digits);
        if t.attrs['class'][1] == 'typography-4':
            num += 4 * (10 ** digits);
        if t.attrs['class'][1] == 'typography-5':
            num += 5 * (10 ** digits);
        if t.attrs['class'][1] == 'typography-6':
            num += 6 * (10 ** digits);
        if t.attrs['class'][1] == 'typography-7':
            num += 7 * (10 ** digits);
        if t.attrs['class'][1] == 'typography-8':
            num += 8 * (10 ** digits);
        if t.attrs['class'][1] == 'typography-9':
            num += 9 * (10 ** digits);
        if t.attrs['class'][1] == 'typography-second':
            digits += 1 #i know, thats kinda hacky
        digits -= 1
    return num/100 if percentage else num;


def parseTries(tries):
    t = list(mit.split_before(tries,lambda x: x.attrs['class'][1] == 'typography-slash'))
    return [typographyToInt(t[0]),typographyToInt(t[1])]

def parseDateTime(str):
    tokens = str.split(' ')
    if len(tokens) == 1:
        creationTime = time.mktime(datetime.datetime.strptime(tokens[0], "%m/%d/%Y").timetuple())
        timestamp = datetime.datetime.fromtimestamp(creationTime).strftime("%Y-%m-%d %H:%M")

    else:
        if (tokens[1] == "mins.") or (tokens[1] == "min."):
            creationTime = datetime.datetime.now() - datetime.timedelta(minutes=int(tokens[0]))
        if (tokens[1] == "hours") or (tokens[1] == "hour"):
            creationTime = datetime.datetime.now() - datetime.timedelta(hours=int(tokens[0]))
        if (tokens[1] == "days") or (tokens[1] == "day"):
            creationTime = datetime.datetime.now() - datetime.timedelta(days=int(tokens[0]))
        timestamp = creationTime.strftime("%Y-%m-%d %H:%M")

    return timestamp

def parseTheme(str):
    return themeDict[str.split('_')[2]]

def parseMedals(m):
    if m.attrs['class'][2] == 'common_icon_coin11':
        return typographyToInt(m.find('.typography'))
    else:
        return int(m.attrs['class'][2][16:])

def parseLevlCard(c):
    level = SMMLevel.Level()
    level.id = c.find('a.button.course-detail.link', first=True).attrs['href'][9:]
    level.name = c.find('.course-title', first=True).text
    level.theme = parseTheme(c.find('.gameskin', first=True).attrs['class'][2])
    level.created = parseDateTime(c.find('.created_at', first=True).text)
    level.difficulty = c.find('.rank', first=True).text

    tag = c.find('.course-tag')[0].text
    level.tag = None if tag == "---" else tag

    level.likes = typographyToInt(c.find('.liked-count', first=True).find('.typography'))
    level.played = typographyToInt(c.find('.played-count', first=True).find('.typography'))
    level.shared = typographyToInt(c.find('.shared-count', first=True).find('.typography'))
    level.clearRate = typographyToInt(c.find('.clear-rate', first=True).find('.typography'), percentage=True)

    tries = parseTries(c.find('.tried-count', first=True).find('.typography'))
    level.triesSuccess = tries[0]
    level.triesTaken = tries[1]

    authorExists = (c.find('.icon-mii', first=True) != None)
    if authorExists:

        author = SMMAuthor.Author()
        author.id = c.find('.icon-mii', first=True).attrs['href'][9:].split('?', 1)[0]
        author.name = c.find('.name', first=True).text
        author.medals = parseMedals(c.find('.medals', first=True))
        author.country = c.find('.flag', first=True).attrs['class'][1]
        level.authorId = author.id
    else:
        author = None

    return level, author

def parsePage(response):
    page = []
    cards = response.html.find('.course-card')
    for c in cards:
        page.append(parseLevlCard(c))

    return page