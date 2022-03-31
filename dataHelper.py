import logging
import time
from datetime import datetime, timezone
from typing import List
from urllib.parse import urlparse

import requests
import vobject
from dateutil import tz
from icalevents.icalevents import events
from icalevents.icalparser import Event
from lxml import etree
from requests.auth import HTTPBasicAuth

from settings import *

logger = logging.getLogger('app')


def sort_by_date(e: Event):
    return e.start.astimezone()


def get_events(max_number: int) -> List[Event]:
    logger.info("Retrieving calendar infos")
    utc_timezone = tz.tzutc()
    current_timezone = tz.tzlocal()

    try:
        logger.info("query webdav")
        event_list = events(WEBDAV_CALENDAR_URL, fix_apple=WEBDAV_IS_APPLE)
        event_list.sort(key=sort_by_date)
        logger.info(event_list)

        logger.info("filter events")
        start_count = 0
        for event in event_list:
            event.start.replace(tzinfo=utc_timezone)
            event.start = event.start.astimezone(current_timezone)

            # remove events from previous day (problem based on time-zones)
            day_number = time.localtime().tm_mday
            print(datetime.now(current_timezone))
            if (event.end < datetime.now(current_timezone)):
                start_count += 1
                max_number += 1

        logger.info("Got {} calendar-entries (capped to {})".format(
            len(event_list), max_number-start_count))
        return event_list[start_count:max_number]

    except Exception as e:
        logger.critical(e)
        return []


def get_birthdays() -> List[str]:
    return []
