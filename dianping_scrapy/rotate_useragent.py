import random
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware
class RotateUserAgentMiddleware(UserAgentMiddleware):
    def __init__(self,user_agent=''):
        self.user_agent=user_agent
    def process_request(self, request, spider):
        ua=random.choice(self.user_agent_list)
        # print(ua)
        if ua:
            request.headers.setdefault('User-Agent',ua)
    user_agent_list=[
                     'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)',
                     'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET CLR 2.0.50727; SE 2.X MetaSr 1.0)',
                     'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
                     'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Avant Browser)',
                     'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
                     'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; TencentTraveler 4.0)',
                     'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Maxthon 2.0)',
                     'Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11',
                     'Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11',
                     "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
                     "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
                     "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
                     "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
                     "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
                     "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
    ]

import base64
# Start your middleware class
class ProxyMiddleware(object):
    # overwrite process request
    def process_request(self, request, spider):
        # Set the location of the proxy
        ip=random.choice(self.ip_list)
        # print(ip)
        request.meta['proxy'] = ip
    ip_list=[
             # A9 可用
             'http://221.230.254.112:28881',
             # H6 可用
             'http://115.221.119.144:41652',

             # KN 可用
             'http://120.33.247.224:30756',

             # 70 可用
             'http://27.154.180.156:27233'
             ]