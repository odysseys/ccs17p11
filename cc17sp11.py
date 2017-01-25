import re
#print('START')
#open_file = open( '../pageviews-20161109-000000_short', 'r', encoding = 'utf-8')
open_file = open( '../test_short', 'r', encoding = 'utf-8')
#output = open_file.read()
#print('OPEN FINISH')
for line in open_file.readlines():
    print(line, end='')
    
open_file.close()

