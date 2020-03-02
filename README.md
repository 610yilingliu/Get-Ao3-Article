# Get-Ao3-Article
批量获取AO3文章并保存为文档（Get Ao3 articles through auther name or tags, save as image）

原定保存为长图，但因为selenium需要chrome driver，得额外安装所以还是保存为文档了

使用正则表达式清理网页非常容易出问题（发文格式不同，对应的html戳也不同），目前尚在测试排查bug

目前article.py是bug重灾区