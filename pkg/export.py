import os

def write_totxt(subfolder, title, author, content, chapter, summary, notes):
    '''
    Export fetched content from AO3 to a local txt file
    Variables type: subfolder - string, title - string, author - string, content - string, chapter - list, summary - list, notes -list
    '''
    if not os.path.exists(subfolder):
        os.mkdir(subfolder)
    # replace invalid chars from file name
    winfname = ''
    invalid_char = ['\\', '/', ':', '*', '?', '<', '>', '|','\"']
    for i in range(len(title)):
        if title[i] not in invalid_char:
            winfname += title[i]
        else:
            winfname += '_'

    name = winfname + '.txt'
    with open(subfolder + '/' + name, 'w', encoding = 'utf-8') as f:
        f.write(title.encode('utf-8').decode('utf-8'))
        f.write('\n')
        f.write('Author: '+ author)
        f.write('\n')
        if chapter != None:
            for i in range(len(chapter)):
                f.write(chapter[i] + '\n')
        if summary != None:
            for i in range(len(summary)):
                # i start from 1 instead of 0 for reading
                f.write('Summary '+ str(i+1) + ': '+ summary[i] + '\n')
        if notes != None:
            for i in range(len(notes)):
                f.write('Note ' + str(i+1) + ': ' + notes[i] + '\n')
        f.write(content)
