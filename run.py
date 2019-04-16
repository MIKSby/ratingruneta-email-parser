from tasks import perform


with open('urls.txt', 'r') as f:
    for site in f:
        perform.delay(site.rstrip())
