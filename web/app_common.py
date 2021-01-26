import datetime
import arrow
from pymongo import MongoClient
link_api_agent = ''
link_api_mac = ''

client = MongoClient("mongodb://0.0.0.0:27017")
class Timer(object):
    @classmethod
    def get_timestamp_now(cls):
        now = arrow.utcnow()
        return now.timestamp
    @classmethod
    def get_timestamp(cls,timedate):
        date = datetime.datetime.strptime(timedate, "%Y/%m/%d")
        at = datetime.datetime.timestamp(date)
        return int(at)

def Convert_timestamp(timestamp):
    try:
        ts = datetime.datetime.fromtimestamp(int(timestamp)).strftime("%d/%m/%Y")
    except Exception as e:
        return ''
    return ts
def Convert_timestamp2(timestamp):
    try:
        ts = datetime.datetime.fromtimestamp(int(timestamp))
    except Exception as e:
        return ''
    return ts

