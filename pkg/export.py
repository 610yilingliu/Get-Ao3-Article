import os

def write_totxt(subfolder, title, author, content):
    if not os.path.exists(subfolder):
        os.mkdir(subfolder)
        print('maked')
    # replace invalid chars from file name
    winfname = ''
    invalid_char = ['\\', '/', ':', '*', '?', '<', '>', '|','\"']
    for i in range(len(title)):
        if title[i] not in invalid_char:
            winfname += title[i]
        else:
            winfname += '_'

    name = winfname + '.txt'
    print(name)
    with open(subfolder + '/' + name, 'w', encoding = 'utf-8') as f:
        f.write(title.encode('utf-8').decode('utf-8'))
        f.write('\n')
        f.write('Author: '+ author)
        f.write('\n')
        f.write(content)
