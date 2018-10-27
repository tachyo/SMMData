import time
import sqlite3
import SMMSearch
import SMMParser
import SMMLevel
import SMMDBService
import requests
from requests_html import HTMLSession
import logging

logging.basicConfig(filename='error.log', level=logging.ERROR,
                    format='%(asctime)s: %(message)s')
logger = logging.getLogger()

db = SMMDBService.DBService(sqlite3.connect('SMM.db'))

session = HTMLSession()

urlBuilder = SMMSearch.ExhaustiveSearch('liked_count_desc')
search = urlBuilder.next()
pageNum = 0;
for url in search:
    lastResponse = 0
    tries = 0;
    while lastResponse != 200:
        try:
            r = session.get(url)
            lastResponse = r.status_code
            print("{:>3} {}".format(lastResponse, r.reason))
            if lastResponse != 200:
                tries += 1
                sleep_sec = 30*tries
                logger.error("received {} requesting {}".format(lastResponse, url))
                print(
                    "Request unsuccessful! we received an http error code.\n"
                    "This could mean that nintendo is rate-limiting us.\n"
                    "Or a more generic error somewhere in the network happened.\n"
                    "Ether way the problem should resolve itself.\n"
                    "Will retry in {} seconds.\n"
                    "More information on what happened has been written to error.log"
                    .format(sleep_secs))
                time.sleep(sleep_sec)
                continue

        except requests.exceptions.RequestException as e:
            sleep_sec = 60
            logger.error("network error while requesting {}\n{}".format(url, e))
            print(
                "A network error occurred!\n"
                "This is usually not a problem an will resolve itself.\n"
                "If the problem persists please double check your internet connection.\n"
                "Will retry in {} seconds.\n"
                "More information on what happened has been written to error.log"
                .format(sleep_secs))
            time.sleep(sleep_sec)
            lastResponse = -1
            continue

        cards = r.html.find('.course-card')
        for c in cards:
            try:
                levelInfo = (SMMParser.parseLevlCard(c))
            except Exception as e:
                logger.error("parsing error while processing \n{}\n{}".format(url,e))
                print(
                    "A parsing error occurred!\n"
                    "Probably caused by unexpected/incomplete level information.\n"
                    "This level will not be inserted into the database.\n"
                    "More information on what happened has been written to error.log")
                continue

            try:
                db.persistLevelInfo(levelInfo)
            except Exception as e:
                logger.error("database error while processing \n{}\n{}".format(url, e))
                print(
                    "A database error occurred!\n"
                    "This should actually never happen, but is not critical.\n"
                    "This level will not be inserted into the database.\n"
                    "More information on what happened has been written to error.log")
                continue

    time.sleep(5)

session.close()
db.close()
