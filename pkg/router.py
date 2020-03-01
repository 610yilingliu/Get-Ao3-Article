import requests
import re
import string

class ao3(object):
    def __init__(self, url, header = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
    }):
        req = requests.get(url, headers = header)
        html = req.text
        self.__html = html
        self.__url = url

    def geturl(self):
        return self.__url
    
    def gethtml(self):
        return self.__html

    def getarticles(self):
        html = self.__html
        pattern = re.compile(r'<h4 class=\"heading\">\n\s{1,}<a href=\"(.*?)\">')
        link_rawls = pattern.findall(html)
        if link_rawls!=[]:
            link_ls = []
            for link in link_rawls:
                if not link.endswith('?view_adult=true'):
                    link = 'https://archiveofourown.org/' + link + '?view_adult=true'
                else: 
                    link = 'https://archiveofourown.org/' + link
                link_ls.append(link)
            return link_ls
        else:
            return []


def fetch_pages(url):
    end_pattern = re.compile(r'\?page=(\d{1,})$')
    # if url is not end with page number
    url_ls = []
    if re.search(end_pattern, url) == None:
        for i in range(1,100):
            url_ls.append(url + '?page=' + str(i))
    else:
        baseurl = url.rstrip(string.digits)
        for i in range(1,100):
            url_ls.append(baseurl + '?page=' + str(i))
    return url_ls
