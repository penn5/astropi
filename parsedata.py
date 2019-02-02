import sys
f = open('data.csv', 'rb')
out = open('out.log', 'wb')
o = out
d = f.read()
needsClosing = False
i = 0
c = ''
escaped = False
isAfterComma = True
for ch in d:
    lc = c
    c = chr(ch)
    if isAfterComma:
        if needsClosing:
            o.close()
        o = out
        if c == 'E':
            o.write(b'\nE: ')
        elif c == 'W':
            o.write(b'\nW: ')
        elif c == 'D':
            o.write(b'\nD: ')
        elif c == 'V':
            o.write(b'\nV: ')
        elif c == 'M':
            o.write(b'\nWriting image to file.')
            o = open('image_'+str(i)+'.jpg', 'wb')
        elif c == 'L':
            o.write(b'\nLocation currently at ')
        elif c == 'S':
            sys.exit()
        else:
            raise Exception("Malformed datatype. STOP.", c)
        isAfterComma = False
        continue


    if c == '\\' and escaped == False:
        escaped = True
        continue
    elif c == '\\' and escaped == True:
        escaped = False
        o.write(bytes([ch]))
        continue

    if c == ',' and escaped == False:
            isAfterComma = True
            continue
    elif c == ',' and escaped == True:
        escaped = False


    print(c, escaped)


    if escaped == True and c != '\\':
        raise Exception("Unexpected \\. STOP.")
    elif escaped == True and c == '\\':
        escaped = False


    if escaped == False:
        o.write(bytes([ch]))




