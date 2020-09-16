# AO3文章批量下载工具

**必须给在国外或者有梯子的人用！！！必须给在国外或者有梯子的人用！！！必须给在国外或者有梯子的人用！！！重要的事情说三遍！！！**



批量获取AO3文章并保存为文档（Get Ao3 articles through auther name or tags, save as txt file）

原定保存为长图，但因为selenium大佬需要chrome driver，得额外安装所以还是保存为文档了

使用正则表达式清理网页非常容易出问题（发文格式不同，对应的html戳也不同），目前尚在测试排查bug

目前article.py是bug重灾区, 如果在下载文章时发现文章内容中有很多奇怪的字符（HTML编码）请将解析错误的页面发邮件给 <yilingliu1994@gmail.com>，人在秒回

如果一段时间没回，发 <22214014@student.uwa.edu.au>也可, 目前我人因为travel restriction暂时还在国内，前面的常用邮箱在梯子出问题时是无法访问的（重申一遍，想举报的就别白费功夫了，我用的是学校提供的合法梯子。自己在aws搭建的梯子服务器其实更加稳定，但是目前不敢用）

## 更新日志

2020.3.4

增加文章内分章节获取功能

## 使用方法：

### 方法1：

对于无计算机基础用户：直接下载百度网盘中```ao3文章批量下载工具.exe```,解压后点击```ao3_fetcher.exe```即可开始使用

链接: https://pan.baidu.com/s/1IkFxlIhw3KL2Sitp0obQpw 提取码: n2xa 复制这段内容后打开百度网盘手机App，操作更方便哦

然后按照提示输入ao3链接以及确认是否获取该链接下所有相关链接/相关分章节即可，下载完成后的文章在```ao3_fetcher.exe```同目录```article```文件夹下, 完成后按Enter结束。

至于在小黑窗上显示的信息是什么意思，请看后面的提示信息说明


### 方法2

首先请确保你有python3环境，否则无法使用此方法。

把整个目录拉下来， 命令行中进入项目目录

按照你的python电脑中是否双版本python共存（本项目基于python3，在python2下无法运行）

python3 单版本下：
```python pkg```

python2，python3共存的情况下：
```python3 pkg```

然后和exe文件使用方法一样，按照提示输入ao3链接以及确认是否获取该链接下所有相关链接/相关分章节即可，下载完成后的文章在同目录```./article```文件夹下, 完成后按Enter结束

## 提示信息说明

中文命令行有时候会乱码，所以我所有的提示信息都是用英文写的，全是字面意思。

Please paste an AO3 url here: 在这里黏贴ao3链接

Get all pages related to this url? if yes, type y (lowercase), if not,type anything else: 是否获取该链接下所有相关链接(其实是搜索结果翻页功能)？（针对多页的搜索结果）如果是请按小写y（注意全角半角！一定要是半角字符），如果只想获取当前页内容，随便按个什么

Get all chaps related to pages in this url? if yes, type y (lowercase), if not,type anything else: 是否获取所有分章节？如果是请按小写y，否则随便按什么

Cannot visit provided url, please check your network and url address ： 链接无法访问，清检查你的网络状态（如果开着梯子，请开全局模式）。请勿输入镜像网站链接或其他网址

Page type not supported, please check if it is from ao3： 该网址不是ao3链接

Analyzing xxx ： 正在解析xxx网址

Exporting xxx: 正在将xxx文输出至本地txt文件

Download Finished: 下载完成

Time to finish this downloading process: xxx ： 花费时间：xxx

Press enter to close program： 按Enter结束程序

## 针对同行们的源码修改指路

```__main__.py```中启动器的```process_num```可改，这是我使用multiprocessing模块打开的多进程池，原来是3个进程，可以加

```article.py```里有个```replace_dict``` 是清理html时需要替换掉到的字符 - 目标字符的字典形式，可改（如果误删或者少清了什么东西）

## 这个其实写的很烂,但是最近似乎没有人用,所以就暂时不更新了...特别是multiprocessing那边,当时完全不懂乱写的-.-!


