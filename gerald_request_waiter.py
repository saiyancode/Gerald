import requests as r
import datetime
from random import choice
import time

class goget():
    def __init__(self, proxies):
        self.start_time = datetime.datetime.now()
        self.last_request = None
        self.proxies = self.__proxy_dict(proxies) if proxies != False else 0
        self.ban_time = 10

    def __proxy_dict(self,proxies):
        pro = {}
        for proxy in proxies:
            pro[proxy] = (True,0)
        return pro

    def __select_proxy(self):
        # Update the proxy dict if enough time has passed for the proxy to be tried again
        for proxy, value in self.proxies.items():
            if value[0] != True:
                if datetime.datetime.now() - value[0] >= datetime.timedelta(seconds=self.ban_time * value[1]):
                    self.proxies[proxy] = (True,value[1])
        return choice([key if value[0] != False else 0 for key, value in self.proxies.items()])

    def make_request(self,url):
        # Pull a proxy from the dict & run it - if request isn't 200 pull another
        proxy = self.__select_proxy()
        a = r.get(url)
        if a.status_code == 403:
            self.proxies[proxy] = (datetime.datetime.now(),self.proxies[proxy][1]+1)
        return a

    def wait_between_requests(self, wait, url):
        # Waits for set time between requests
        a = self.make_request(url) if self.last_request == None else 0
        if a != 0:
            self.last_request = datetime.datetime.now()
            return a
        time_to_wait = (self.last_request + datetime.timedelta(seconds=wait)) - datetime.datetime.now() if self.last_request != None else 0
        time.sleep(time_to_wait.seconds)
        # Request can be made so make it & return
        return self.make_request(url)

    def requests_per_hour(self, num, url):
        pass

    def requests_per_sec(self, num, url):
        pass


c = goget(proxies=['82.145.57.93'])
a = c.wait_between_requests(10,'https://www.google.co.uk')
time.sleep(1)
b = c.wait_between_requests(5,'https://adaptworldwide.com')