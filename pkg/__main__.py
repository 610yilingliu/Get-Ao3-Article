import re
import multiprocessing
import datetime
from router import ao3, urlanalyzer, url_decorator
from article import article
from export import write_totxt


def exportsinglearticle(url,silent = False):
    '''
    Bind method to put article from a url to a txt file
    Variable type: url - String
    '''
    url = url_decorator(url)
    article_wanted = article(url)
    title = article_wanted.gettitle()
    author = article_wanted.getauthor()
    content = article_wanted.getcontent()
    summary = article_wanted.getsummary()
    notes = article_wanted.getnotes()
    chapter = article_wanted.getchap()
    related_chaps = article_wanted.get_related_chaps()
    if silent!= False:
        print('Exporting ' + title)
    write_totxt('./article', title = title, author = author, content = content, chapter = chapter, summary = summary, notes = notes)
    return related_chaps

def getchapurls(url):
    articls_instance = article(url)
    return articls_instance.get_related_chaps()

def exportchapsrelated(url):
    chap_related = getchapurls(url)
    for url in chap_related:
        url = url_decorator(url)
        exportsinglearticle(url)

def exportarticles(pages_ls, getall_chaps):
    '''
    Bind method to get urls from every element from a page list, them use exportsinglearticle() to export
    Multiprocessing is applied
    Variable type: pages_ls - list 
    '''
    stack = []
    cutpattern = re.compile(r'<\!--main content-->([\s\S]*)<\!--\/content-->')
    for page in pages_ls:
        pageitem = ao3(page)
        print('Analyzing ' + pageitem.geturl())
        page_html = pageitem.gethtml()
        html_patterned = cutpattern.search(page_html)
        item_tocheck = html_patterned.groups()[0]
        stack.append(item_tocheck)
        if len(stack) == 2:
            if stack[0] == stack[1]:
                print('Duplicated Page, Finish Analyzing Process')
                break
            else:
                stack.remove(stack[0])
        url_ls = pageitem.getarticles()
        if getall_chaps == True:
            for url in url_ls:
                chap_related = getchapurls(url)
                if chap_related !=None:
                    url_ls = list(set(url_ls + chap_related))
        if url_ls != []:
            # if __name__ == '__main__' is needed for multiprocessing.
            p = multiprocessing.Pool(process_num)
            # cannot use for url in url_ls, else cannot stop while two pages are the same.
            for i in range(len(url_ls)):
                p.apply_async(exportsinglearticle, args = (url_ls[i], False))
            p.close()
            p.join()
        else:
            print('All Articles Downloaded')
            break

def runner(pageurl, process_num, fetch_pages, allchaps):
    pagesitem = urlanalyzer(pageurl)

    if pagesitem.geturltype() == 'article' or pagesitem.geturltype() == 'chap':
        if allchaps == False:
            exportsinglearticle(pagesitem.geturl())
        else:
            exportchapsrelated(pagesitem.geturl())
    else:
        if fetch_pages == True:
            pages_ls = pagesitem.fetch_pages()
            exportarticles(pages_ls, allchaps)
        else:
            exportarticles([pageurl], allchaps)

        
# write for multiprocessing
if __name__ == '__main__':
    # pyintaller helper, prevent from bugs
    multiprocessing.freeze_support()
    print("本程序在中国大陆无法使用，请让你在海外的朋友，或有梯子（代理需要开启全局模式）的朋友帮忙下载AO3中文章")
    pageurl = input('Please paste an AO3 url here:  ')
    fetch_pages_command = input('Get all pages related to this url? if yes, type y (lowercase), if not,type anything else:  ')
    getall_chaps_command = input('Get all chaps related to pages in this url? if yes, type y (lowercase), if not,type anything else:  ')
    process_num = 3

    if fetch_pages_command == 'y':
        fetch_pages = True
    else:
        fetch_pages = False

    if getall_chaps_command == 'y':
        getall_chaps = True
    else:
        getall_chaps = False
    
    t1 = datetime.datetime.now()
    runner(pageurl, process_num, fetch_pages = fetch_pages, allchaps = getall_chaps)
    t2 = datetime.datetime.now()
    t3 = t2 - t1
    print('Download Finished')
    print('Time to finish this downloading process: ' + str(t3))
    input("Press enter to close program")

