import png

pngfile = open('test.png','rb')

pixels = list(png.Reader(file = pngfile).read()[2])

newpixels = []
filler = ' '

for row in pixels[160:640-160:]:
    newrow = []
    for cell in row[480::]:       
        if chr(cell) in ',.-!?' or cell >= 65 and cell < 128:
            newrow.append(chr(cell))
        else:
            newrow.append(filler)
    if newrow:
        newpixels.append(''.join(newrow))
        #print(str(newrow)) 
        #break

with open('output.html','wt',encoding='ASCII') as filewrite:
    filewrite.write('\n'.join(newpixels))

pngfile.close()
