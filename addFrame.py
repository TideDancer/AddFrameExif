# add frame with exif info to photo
# require PIL
# $ python addFrame.py path/
# outputs are in output/ folder

from PIL import Image, ImageOps, ImageDraw, ImageFont
from PIL.ExifTags import TAGS
import sys
import os
import glob

# get directory in argv[1]
files = [x for x in os.listdir(sys.argv[1]) if os.path.isfile(sys.argv[1]+x)]

for f in files:
	img = Image.open(sys.argv[1]+f)
	print 'start processing {}'.format(f)
	
	# get image size and expand black frame
	h = img.size[1]
	l = img.size[0]
	b = int(round(h*0.02))
	img_border = ImageOps.expand(img,border=b,fill='black')
	
	# get exif data
	exif_data = {
		TAGS[k]: v
		for (k,v) in img._getexif().items()
		if k in TAGS
		}
	
	# write useful exif data
	model = exif_data['Model']
	aper = exif_data['FNumber'][0]
	shut = int(round(1/exif_data['ExposureTime'][0]))
	iso = exif_data['ISOSpeedRatings'][0]
	lens = int(exif_data['FocalLength'][0])
	date = exif_data['DateTimeDigitized'][0]
	
	text = []
	text.append('{}'.format(model))
	text.append('F {}'.format(aper))
	text.append('1/{} s'.format(shut))
	text.append('ISO {}'.format(iso))
	text.append('{} mm'.format(lens))
	text.append(date)
	
	# write exif in the bottom
	font = ImageFont.truetype('Arial.ttf', int(round(h*0.018)))
	draw = ImageDraw.Draw(img_border)
	for i in range(0,len(text)):
		draw.text((b+i*l/len(text), h+b),text[i],(255,255,255),font)
	
	img_border.save('output/{}'.format(os.path.basename(f)))

