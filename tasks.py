from celery import Celery
import requests
import re


q = Celery('tasks', broker='redis://localhost:6379/0')


useragent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) ' \
            'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/' \
            '71.0.3578.98 Safari/537.36'


@q.task(name='parser')
def perform(url):
    try:
        r = requests.get(url=url + '/contacts',
                         headers={'User-agent': useragent}, timeout=30)
        if r.status_code == 200:
            collect(r.text)
            return 'OK'
        else:
            with open('not_found.txt', 'a') as nf:
                nf.write(url + '\n')
            return 'Not Found!'
    except Exception as e:
        print(e)


def collect(req):
    list_emails = re.findall('\w+@\w+[.]\w+', req)
    with open('result.txt', 'a') as f:
        for email in list_emails:
            f.write(email + '\n')
