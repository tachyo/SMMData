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
                logger.error("received {} requesting {}".format(lastResponse, url))
                print("request unsuccessful! we received an http error code")
                print("this could mean that nintendo is rate-limiting us")
                print("or a more generic error somewhere in the network happened")
                print("ether way the problem should resolve itself")
                print("will retry in {} seconds".format(30*tries))
                print("more information on what happened has been written to error.log")
                time.sleep(30**tries)
                continue

        except requests.exceptions.RequestException as e:
            logger.error("network error while requesting {}\n{}".format(url, e))
            print("an network error occurred!")
            print("this is usually not a problem an will resolve itself")
            print("if the problem persists please double check your internet connection")
            print("will retry in {} seconds".format(60))
            print("more information on what happened has been written to error.log")
            time.sleep(60)
            lastResponse = -1
            continue

        cards = r.html.find('.course-card')
        for c in cards:
            try:
                levelInfo = (SMMParser.parseLevlCard(c))
            except Exception as e:
                logger.error("parsing error while processing \n{}\n{}".format(url,e))
                print("an parsing error occurred!")
                print("probably caused by unexpected/incomplete level information")
                print("this level will not be inserted into the database")
                print("more information on what happened has been written to error.log")
                continue

            try:
                db.persistLevelInfo(levelInfo)
            except Exception as e:
                logger.error("database error while processing \n{}\n{}".format(url, e))
                print("an database error occurred!")
                print("this should actually never happen, but is not critical")
                print("this level will not be inserted into the database")
                print("more information on what happened has been written to error.log")
                continue

    time.sleep(5)

session.close()
db.close()
