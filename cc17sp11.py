# coding=utf-8
'''
Decoder for percent encoded strings

In contrast to URLDecoder, this decoder keeps percent signs that are not
followed by hexadecimal digits, and does not convert plus-signs to spaces.

You can put this snippet of code into your filter script.
'''

def decode(encoded):
    def getHexValue(b):
        if '0' <= b <= '9':
            #return chr(ord(b) - 0x30)
            return chr(ord(b) - 0x30)
        elif 'A' <= b <= 'F':
            #return chr(ord(b) - 0x37)
            return chr(ord(b) - 0x37)
        elif 'a' <= b <= 'f':
            #return chr(ord(b) - 0x57)
            return chr(ord(b) - 0x57)
        return -1

    if encoded is None:
        return None
    encodedChars = encoded
    encodedLength = len(encodedChars)
    decodedChars = ''
    encodedIdx = 0
    while (encodedIdx+2) < encodedLength:
        #print(encodedChars)
        #print(str(getHexValue(encodedChars[encodedIdx + 1])) + ', ' + str(getHexValue(encodedChars[encodedIdx + 2])))
        if encodedChars[encodedIdx] == '%' and encodedIdx + 2 < encodedLength and getHexValue(encodedChars[encodedIdx + 1]) != -1 and getHexValue(encodedChars[encodedIdx + 2]) != -1:
            #  current character is % char
            value1 = getHexValue(encodedChars[encodedIdx + 1])
            value2 = getHexValue(encodedChars[encodedIdx + 2])
            decodedChars += chr((ord(value1) << 4) + ord(value2))
            encodedIdx += 2
        else:
            decodedChars += encodedChars[encodedIdx]
        encodedIdx += 1
    return str(decodedChars)


#print('START')
open_file = open( '../pageviews-20161109-000000', 'r', encoding = 'utf-8')
#open_file = open( '../test_short', 'r', encoding = 'utf-8')
out_file = open( '../output', 'w', encoding = 'utf-8')
#output = open_file.read()
#print('OPEN FINISH')
b_list_head=['Media:', 'Special:', 'Talk:', 'User:',
'User_talk:', 'Wikipedia:', 'Wikipedia_talk:', 'File:',
'File_talk:', 'MediaWiki:', 'MediaWiki talk:', 'Template',
'Template talk', 'Help', 'Help talk', 'Category',
'Category talk', 'Portal', 'Portal talk', 'Book',
'Book talk', 'Draft', 'Draft talk', 'Education Program',
'Education Program talk', 'TimedText talk', 'Module', 'Module talk',
'Gadget', 'Gadget talk', 'Gadget definition', 'Gadget definition talk']
b_list_end=['.png', '.gif', '.jpg', '.jpeg',
'.tiff', '.tif', '.xcf', '.mid',
'.ogg', '.ogv', '.svg', '.djvu',
'.oga', '.flac', '.opus', '.wav',
'.webm', '.ico', '.txt', '_(disambiguation)'
]

for line in open_file.readlines():
    line_item = line.split()
    #print(line_item[0], line_item[1], line_item[2], line_item[3])
    line_item[1] = decode(str(line_item[1]))
    if(len(line_item[0]) != 0 and len(line_item[1]) != 0 and len(line_item[2]) != 0 and len(line_item[3]) != 0):
        #print('FOUR ELEMENT')
        if(line_item[0] == 'en' or line_item[0] == 'en.m'):
            #print('EN or EN.M')
            b_list_cnt1 = 0
            if(line_item[1] != '404.php' and line_item[1] != 'Main_Page' and line_item[1] != '-' and (not 'a' <= line_item[1][0] <= 'z' )):
                for b_item_1 in b_list_head:
                    if(not line_item[1].startswith(b_item_1)):
                        b_list_cnt1 += 1
                        #print('b_list_cnt1=' + str(b_list_cnt1))
                        b_list_cnt2 = 0
                        for b_item_2 in b_list_end:
                            if(not line_item[1].endswith(b_item_2)):
                                b_list_cnt2 += 1
                                #print('b_list_cnt2=' + str(b_list_cnt2))
                                #print('COLLECTED!!!!')
                                if(b_list_cnt1 == 32 and b_list_cnt2 == 20):
                                    out_file.write(line_item[1] + '\t' + line_item[2] + '\n')
    #print(line, end='')
    
open_file.close()
out_file.close()

