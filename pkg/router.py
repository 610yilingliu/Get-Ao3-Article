import requests
import re
import string

class ao3(object):
    '''
    AO3 search result object, with its url, html and url of articles inside it
    Variable type: url - String
    '''
    def __init__(self, url, header = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
    }):
        try:
            req = requests.get(url, headers = header)
            html = req.text
            self.__html = html
            self.__url = url
        except:
            print('Cannot visit provided url, please check your network and url address')
            input("Press enter to close program")
            exit()

    def geturl(self):
        '''
        return url, type: string
        '''
        return self.__url
    
    def gethtml(self):
        '''
        return html, type: String
        '''
        return self.__html

    def getarticles(self):
        '''
        return a list with urls on the current page
        '''
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

class urlanalyzer(object):
    '''
    Analyze the type of input url
    Variable type: url - String
    '''
    def __init__(self, url):
        self.__url = url
        pattern_pagenum = re.compile(r'\?page=(\d{1,})$')
        pattern_searchresult = re.compile(r'&work_search%')
        pattern_fandom = re.compile(r'works\?fandom_id=')
        pattern_singlearticle = re.compile(r'/works/\d{1,}$')
        '''
        If not a AO3 link
        '''
        if not url.startswith('https://archiveofourown.org/'):
            print('Please make sure your url is from https://archiveofourown.org/, instead of a mirror website')
            input("Press enter to close program")
            exit()
        elif url.endswith('works'):
            self.__urltype = 'works'
        elif re.search(pattern_pagenum, url) != None:
            self.__urltype = 'pagenum'
        elif re.search(pattern_searchresult, url)!= None:
            self.__urltype = 'searchresult'
        elif re.search(pattern_fandom, url)!= None:
            if re.search(pattern_pagenum, url) == None:
                self.__urltype = 'fandom'
            else:
                self.__urltype = 'fandomwithnum'
        elif url.endswith('bookmarks'):
            self.__urltype = 'bookmarks'
        elif url.endswith('collections'):
            self.__urltype = 'collections'
        elif url.endswith('series'):
            self.__urltype = 'series'
        elif re.search(pattern_singlearticle, url)!= None or url.endswith('view_adult=true'):
            self.__urltype = 'article'
        else:
            self.__url = url + '/works'
            self.__urltype = 'works'

    def geturl(self):
        return self.__url

    def geturltype(self):
        return self.__urltype

    def fetch_pages(self):
        '''
        Return all pages relaged to this url
        '''
        url = self.__url
        tp = self.__urltype
        url_ls = []
        if tp == 'works' or tp == 'series' or tp == 'collections' or tp == 'bookmarks' or tp == 'fandom':
            for i in range(1,100):
                url_ls.append(url + '?page=' + str(i)) 
            return url_ls
            return   
        elif tp =='pagenum' or tp == 'fandomwithnum':
            baseurl = url.rstrip(string.digits)
            for i in range(1,100):
                url_ls.append(baseurl + '?page=' + str(i))
            return url_ls
        elif tp == 'searchresult':
            baseurl_prefix = 'https://archiveofourown.org/works/search?page='
            is_pagenum_pattern = re.compile(r'page=')
            if is_pagenum_pattern.search(url) == None:
                suffix_pattern = re.compile(r'https:\/\/archiveofourown\.org\/works\/search\?(.*?)$')
                base_suffix = suffix_pattern.search(url).groups()[0]
                for i in range(1,100):
                    url_ls.append(baseurl_prefix + str(i) + base_suffix)
                return url_ls
            else:
                suffix_pattern = re.compile(r'(?<=https:\/\/archiveofourown\.org\/works\/search\?page=)\d+&(.*)')
                suffix_withnum = suffix_pattern.search(url).groups()[0]
                base_suffix = suffix_withnum.lstrip(string.digits)
                for i in range(1,100):
                    url_ls.append(baseurl_prefix + str(i) + base_suffix)
                return url_ls
        elif tp == 'article':
            pass
