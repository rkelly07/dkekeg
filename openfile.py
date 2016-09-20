file = open('recent.txt', 'r')

num = file.read()
print int(num) +1
file.close()
file = open('recent.txt', 'w')
file.write("301")

file = open('recent.txt', 'r')

num = file.read()
file.close()
print num



