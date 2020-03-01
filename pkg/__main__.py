from article import article
from router import ao3, fetch_pages
from export import write_totxt

pageurl = 'https://archiveofourown.org/tags/%E6%98%8E%E5%94%90'


def page_urls(url, getall = True):
    if getall == True:
        url_ls = fetch_pages(url)
        return url_ls
    return [url]

page_ls = page_urls(pageurl)

for page in page_ls:
    instance = ao3(page)
    url_ls = instance.getarticles()
    if url_ls != []:
        for url in url_ls:
            article_wanted = article(url)
            title = article_wanted.gettitle()
            author = article_wanted.getauthor()
            content = article_wanted.getcontent()
            write_totxt('./article', title = title, author = author, content = content)
    else:
        print('All Articles Downloaded')
        break
        

