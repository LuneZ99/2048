import io
from PIL import Image
for j in ['0', '4', '8', '16', '32', '64', '128', '256', '512', '1024', '2048', '4096']:
    i = Image.open('gif\\'+j+'.gif')

    i = i.resize((192, 192), Image.ANTIALIAS)

    i.save('gif\\'+j+'.gif')