import requests as r
import datetime
from random import choice
import time

class goget():
    def __init__(self, proxies=False, protocol="http"):
        self.start_time = datetime.datetime.now()
        self.last_request = None
        self.proxies = self.__proxy_dict(proxies)
        self.ban_time = 5
        self.protocol = protocol

    def __proxy_dict(self,proxies):
        if proxies == False:
            return 0
        pro = {}
        for proxy in proxies:
            pro[proxy] = (True,0)
        return pro

    def __select_proxy(self):
        # Update the proxy dict if enough time has passed for the proxy to be tried again
        for proxy, value in self.proxies.items():
            if value[0] != True:
                if datetime.datetime.now() - value[0] >= datetime.timedelta(seconds=self.ban_time):
                    self.proxies[proxy] = (True,value[1])

        # Return the proxy structure that's according to the set protocol
        return {self.protocol: choice([key if value[0] == True else 0 for key, value in self.proxies.items()])}

    def __proxy_wait(self):
        # If all proxies are banned wait to till there is an unbanned proxy
        min_wait = self.ban_time
        for proxy, value in self.proxies.items():
            if value[0] != True:
                time_to_wait = (datetime.datetime.now() + datetime.timedelta(seconds=min_wait)) - value[0]
                min_wait = time_to_wait.seconds if min_wait > time_to_wait.seconds else min_wait
        time.sleep(min_wait+1)
        return self.__select_proxy()

    def make_request(self,url):
        # Pull a proxy from the dict & run it - if request isn't 200 pull another
        if self.proxies == False:
            return r.get(url)

        # Retry 50 times each time looping through the proxy dict and if all banned waiting for the ban time until they unban
        for n in range(50):
            try:
                # get a proxy
                proxy = self.__select_proxy()
                # if all are banned be prepped to wait
                proxy = self.__proxy_wait() if list(proxy.values())[0] == 0 else proxy
                a = r.get(url, proxies=proxy)
                if a.status_code != 200:
                    self.proxies[list(proxy.values())[0]] = (datetime.datetime.now(),self.proxies[list(proxy.values())[0]][1]+1)
                else:
                    return a
            except Exception as e:
                print(e)
                print("Skipping due to connection error")

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
        a = self.make_request(url) if self.last_request == None else 0
        if a != 0:
            self.last_request = datetime.datetime.now()
            return a
        # Turn the seconds into a split allowance per hour e.g. 200 requests an hour is 1 every 18 seconds
        time_to_wait = 3600 / num
        time.sleep(time_to_wait)
        # Request can be made so make it & return
        return self.make_request(url)

    def requests_per_sec(self, num, url):
        pass


c = goget(proxies=['95.154.216.236:80'], protocol="http")
a = c.wait_between_requests(2,'https://adaptworldwide.com')
b = c.wait_between_requests(5,'https://adaptworldwide.com')
c = c.requests_per_hour(500,'https://adaptworldwide.com')

print(a.status_code, b.status_code,c.content)