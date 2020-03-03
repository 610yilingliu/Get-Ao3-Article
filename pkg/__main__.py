import re
import multiprocessing
from article import article
from router import ao3, urlanalyzer
from export import write_totxt
import datetime

def exportsinglearticle(url, silent = False):
    article_wanted = article(url)
    title = article_wanted.gettitle()
    author = article_wanted.getauthor()
    content = article_wanted.getcontent()
    summary = article_wanted.getsummary()
    notes = article_wanted.getnotes()
    chapter = article_wanted.getchap()
    if silent == False:
        print('Processing ' + title)
    write_totxt('./article', title = title, author = author, content = content, chapter = chapter, summary = summary, notes = notes)


def exportarticles(pages_ls):
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
                break
            else:
                stack.remove(stack[0])
        url_ls = pageitem.getarticles()
        if url_ls != []:
            # if __name__ == '__main__' is needed for multiprocessing.
            print(url_ls)
            p = multiprocessing.Pool(process_num)
            # cannot use for url in url_ls, else cannot stop while two pages are the same.
            for i in range(len(url_ls)):
                p.apply_async(exportsinglearticle, args = (url_ls[i], False))
                print('pool started')
            p.close()
            p.join()
        else:
            print('All Articles Downloaded')
            break

def runner(pageurl, process_num, fetch_pages = True):
    pagesitem = urlanalyzer(pageurl)

    if pagesitem.geturltype() == 'article':
        exportsinglearticle(pageurl)

    else:
        if fetch_pages == True:
            pages_ls = pagesitem.fetch_pages()
            exportarticles(pages_ls)
        else:
            exportarticles([pageurl])

        
# write for multiprocessing
if __name__ == '__main__':
    pageurl = 'https://archiveofourown.org/users/huaishang233/pseuds/huaishang233/works?fandom_id=25495134'
    process_num = 3
    t1 = datetime.datetime.now()
    runner(pageurl, process_num)
    t2 = datetime.datetime.now()
    t3 = t2 - t1
    print('Spend Time: ' + str(t3))

