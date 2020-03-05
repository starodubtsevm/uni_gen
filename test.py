
data_in = []
byte = 0x2c

for j in range(7, -1, -1):
	data_in.append((byte & 1<<j)>>j)

print (data_in)
