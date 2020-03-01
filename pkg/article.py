import requests
import re

class article(object):
    def __init__(self, url, 
    header = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
    } ):
        req = requests.get(url, headers = header)
        html = req.text
        self.__html = html
        self.__url = url

    def geturl(self):
        return self.__url
    
    def gethtml(self):
        return self.__html

    def gettitle(self):
        html = self.__html
        pattern = re.compile(r'<title>\n(.*)\n')
        title = pattern.search(html).groups()[0]
        # delete space
        title = title.strip()
        return title
    
    def getauthor(self):
        html = self.__html
        pattern = re.compile(r'<a rel=\"author\" href=\"\/users\/(.*?)/')
        author = pattern.search(html).groups()[0]
        return author

    def getcontent(self):
        html = self.__html
        pattern = re.compile(r'userstuff\">([\s\S]*)<\!-- end cache -->')
        search_result = pattern.search(html)
        # if is in Chapter
        if search_result == None:
            pattern2 = re.compile(r'</h3>\n([\s\S]*)<\!--\/main-->')
            content = pattern2.search(html).groups()[0]
        else:
            content = search_result.groups()[0]
        replace_dict = {
            '<p>':'',
            '</p>': '\n',
            '<br/>': '\n',
            '<div>': '',
            '</div>':'',
            '<p dir=\"ltr\">':'',
        }
        for key in replace_dict.keys():
            content = content.replace(key, replace_dict[key])
        return content
