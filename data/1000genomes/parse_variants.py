variants = open('variants.sql')
output = open('variants2.sql', 'w')
flag = False
c_lines = 0
for line in variants:
	if flag:
		output.writelines(line)
		c_lines+=1
	if line.startswith('COPY'):
		flag=True
	if line.startswith('\.'):
		break
print(c_lines)