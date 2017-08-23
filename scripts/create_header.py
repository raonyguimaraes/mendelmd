dbnfsp = open('dbNSFP3.4a.readme.txt')
header = open('header.txt', 'w')

tags = {}

for line in dbnfsp:
    row = line.split('\t')
    if row[0].isdigit():
        digit = int(row[0])
        last_digit = digit
        tags[digit] = ' '.join(row[1:]).strip()
    else:
        #add to last digit
        if len(tags)>0:
            tags[digit]+=' '.join(row).strip()
        
list_tags = []
for tag in tags:
    # print(tag, tags[tag])
    digit = int(tag)
    #get func pred tags + clinvar
    if (digit > 23 and digit < 105) or (digit > 187 and digit < 192):
        row = tags[tag].split(' ')
        
        tag_name = row[0].replace(':', '')
        list_tags.append('dbNSFP_'+tag_name)

        # tag_description = ' '.join(row[1:]).strip()
        # # # print(tag_description)
        # header_tag = '##INFO=<ID=dbNSFP_%s,Number=A,Type=String,Description="%s">\n' % (tag_name, tag_description.replace('"', '').strip())
        # header.writelines(header_tag)

# print(','.join(list_tags))
for tag in list_tags:
    header.writelines(tag+'\n')    