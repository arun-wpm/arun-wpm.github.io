g = open("boston-bangkok-copy/doc.kml", 'w')
diff = [100.534117 - (-71.060461), 13.745604 - 42.355444, 0] #Downtown Crossing -> Siam
def shift_coordinates(line):
    #check tabbing
    for c in line[:12]:
        if c != ' ':
            return line
    
    nums = line.split(',')
    after = []
    try:
        for i in range(3):
            after.append(float(nums[i]) + diff[i])
    except ValueError:
        return line
    return ' '*12 + ','.join(str(newnum) for newnum in after) + '\n'

with open("boston-bangkok/doc.kml") as f:
    while True:
        line = f.readline()
        if (line == ""):
            break
        g.write(shift_coordinates(line))
f.close()
g.close()