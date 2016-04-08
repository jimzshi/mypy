input = open("input.txt","r")
location = [(0,0)]
x = 0
y = 0
n = 1
for line in input:
	for i in line:
		if i == "^":
			y -= 1
		elif i == "v":
			y += 1
		elif i == "<":
			x -= 1
		elif i == ">":
			x += 1
		if (x,y) in location:
			pass
		else:
			n += 1
		location.append((x,y))
#print n

