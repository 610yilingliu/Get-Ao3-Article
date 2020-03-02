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
    
    def getsummary(self):
        html = self.__html
        pattern = re.compile(r'<h3 class=\"heading\">Summary\:<\/h3>([\s\S]*)<\/blockquote>')
        search_result = pattern.search(html)
        if search_result != None:
            summary = search_result.groups()[0]
            return summary
        return None

    def getnotes(self):
        '''return list'''
        html = self.__html
        pattern = re.compile(r'<h3 class=\"heading\">Notes\:<\/h3>([\s\S]*?)<\/blockquote>')
        search_result = pattern.findall(html)
        return search_result

    def getcontent(self):
        html = self.__html
        pattern = re.compile(r'<\!--main content-->([\s\S]*)((?=<\!--\/chapter-->)|(?=<\!--\/main-->))')
        search_result = pattern.search(html)
        # not good enough.((?<=<\!--main content-->)|(?<=<\!--chapter content-->))([\s\S]*)((?=<\!--\/chapter-->)|(?=<\!--\/main-->)) works in regexr but does not work here
        if search_result == None:
            pattern = re.compile(r'<\!--chapter content-->([\s\S]*)((?=<\!--\/chapter-->)|(?=<\!--\/main-->))')
            search_result = pattern.search(html)
        content = search_result.groups()[0]
        return content

def cleaner(text):
    replace_dict = {
        '<!--main content-->':'\n',
        '<!--chapter content-->':'\n',
        '<div class=\"userstuff module\" role=\"article\">': '',
        '<div class=\"userstuff\">': '',
        '<h3 class=\"landmark heading\" id=\"work\">':'',
        '<div id=\"chapters\" role=\"article\">':'',
        '</h3>': '\n',
        '<p>':'',
        '</p>': '\n',
        '<br/>': '\n',
        '<div>': '',
        '</div>':'',
        '<p dir=\"ltr\">':'',
        '<blockquote class=\"userstuff\">': '',
        '</blockquote>':'\n',
        '<!-- end cache -->':'\n'
    }
    if text!= None:
        for key in replace_dict.keys():
            text = text.replace(key, replace_dict[key])
        return text.strip()
    else:
        return None
    
