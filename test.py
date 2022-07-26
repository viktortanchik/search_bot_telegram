import grequests

#import requests
from itertools import groupby

# get the API KEY here: https://developers.google.com/custom-search/v1/overview

def find_test(key):
    query = "car"
    page = 1
    data = []
    urls=[]
    for i in range(1):
        #url = f"https://www.googleapis.com/customsearch/v1?key=AIzaSyCB3rMM4vcu3Ildll2Aw43CRWbBky8k9SM&cx=9573f7af3478ae9ff&q={query}&start={i}"
        url = f"https://www.googleapis.com/customsearch/v1?{key}{str(query)}&start={i}"
        #data = requests.get(url).json()
        urls.append(url)
    response = (grequests.get(url) for url in urls)
    pages = grequests.map(response)
    for r in pages:
        #r = requests.get('https://www.googleapis.com/customsearch/v1?'+url)
        #print(url)
        reqiest = r.json()
        #print("reqiest['items']>>",reqiest['items'])
        try:
            for i in reqiest['items']:
                items = {}
                #print(i['link'])
                items['title'] = i['title']
                items['link'] = i['link']
                #data.append(items)
                data.append(i['link'])
            # print(data)
        except KeyError as er:
            print("Error", er)
    #print('##############################')
    #print(data)
    dic = dict.fromkeys(data)
    #print(dic)
    new_urls=list(dic)
    print(new_urls)

# new_x = [el for el, _ in groupby(data)]
#
# print(new_x)

'''
https://t.me/s/MentaCarMarket?after=139
https://t.me/s/MentaCarMarket?after=236
https://t.me/s/MentaCarMarket?before=210
https://t.me/s/MentaCarMarket?before=87
https://t.me/s/MentaCarMarket?before=189
https://t.me/s/MentaCarMarket?before=316
https://t.me/s/MentaCarMarket?before=41
https://t.me/s/MentaCarMarket?before=23
https://t.me/s/MentaCarMarket?after=84
https://t.me/s/MentaCarMarket?before=2
'''
