import requests
import re

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
        '<!-- end cache -->':'\n',
        '<!--/main-->':'\n',
        '<!--/chapter-->': '\n',
        '<h3 class="heading">':'',
        '<div class="notes module" role="complementary">':'',
        '</a>':' ',
        '<b>':'',
        '</b>':'',
        '<!--/descriptions-->': '\n',
        '<p class=\"jump\">(See the end of the work for <a href=\"#work_endnotes\">more notes .)': '\n',

    }
    if text!= None:
        for key in replace_dict.keys():
            text = text.replace(key, replace_dict[key])
        return text.strip()
    else:
        return None
    

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

    def getchap(self):
        html = self.__html
        pattern = re.compile(r'<h3 class=\"title\">\s+<a href=.*>(.*?)</a>')
        search_result = pattern.findall(html)
        if search_result != []:
            chapters = [cleaner(chapter) for chapter in search_result]
            return chapters
        return None
    
    def getsummary(self):
        html = self.__html
        pattern = re.compile(r'<h3 class=\"heading\">Summary\:<\/h3>([\s\S]*)<\/blockquote>')
        search_result = pattern.findall(html)
        if search_result !=[]:
            summaries = [cleaner(summary) for summary in search_result]
            return summaries
        return None

    def getnotes(self):
        '''return list'''
        html = self.__html
        pattern = re.compile(r'<h3 class=\"heading\">Notes\:<\/h3>([\s\S]*?)<\/blockquote>')
        search_result = pattern.findall(html)
        if search_result!= []:
            notes = [cleaner(note) for note in search_result]
            return notes
        return None

    def getcontent(self):
        html = self.__html
        # not good enough.(?:<\!--main content-->|<\!--chapter content-->)[\s\S]*(?:<\!--\/chapter-->|<\!--\/main-->) works in regexr but does not work here
        pattern1 = re.compile(r'<\!--chapter content-->([\s\S]*)<\!--\/main-->')
        pattern2 = re.compile(r'<\!--chapter content-->([\s\S]*)<\!--\/chapter-->')
        pattern3 = re.compile(r'<\!--main content-->([\s\S]*)<\!--\/chapter-->')
        pattern4 = re.compile(r'<\!--main content-->([\s\S]*)<\!--\/main-->')
        plist = [pattern1, pattern2, pattern3, pattern4]
        for pattern in plist:
            search_result = pattern.search(html)
            if search_result != None:
                content = search_result.groups()[0]
                return cleaner(content)
        print('Page type not supported, please check if it is from ao3')
        input("Press enter to close program")
        exit()




