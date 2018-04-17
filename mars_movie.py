import sys, io, re
import subprocess
import matplotlib.pyplot as pp
import matplotlib.animation as anim
import requests
import bs4
import IPython.display
import PIL, PIL.Image, PIL.ImageOps, PIL.ImageEnhance

IMG_SIZE = 500
# url to the Curiosity Rover's front hazcams page
HAZCAM_URL = 'https://mars.nasa.gov/msl/multimedia/raw/?s={}&camera=FHAZ%5F'

def get_right_url(left_url):
	return re.sub('FLB', 'FRB', left_url) 

def create_anaglyph(l_img_url, r_img_url):
	'''Create a 3d image by blending red and cyan versions of the images'''
	l_img_bytes = requests.get(l_img_url).content
	r_img_bytes = requests.get(r_img_url).content
	l_img = PIL.Image.open(io.BytesIO(l_img_bytes))
	r_img = PIL.Image.open(io.BytesIO(r_img_bytes))
	l_img = format_img(l_img)
	r_img = format_img(r_img)
	l_img_red = PIL.ImageOps.colorize(l_img, (0,0,0),(255,0,0))
	r_img_cyan = PIL.ImageOps.colorize(r_img, (0,0,0),(0,255,255))
	return PIL.Image.blend(l_img_red, r_img_cyan, 0.5)

def format_img(img):
	img = resize(img)
	return remove_fisheye(img)

def remove_fisheye(img):
	return img.transform((500,500),
	PIL.Image.QUAD,
	data=(0,0,100,500,400,500,500,0),
	resample=PIL.Image.BILINEAR)

def resize(img, size=IMG_SIZE):
	return img.resize((size,size))

def get_img_urls(html):
	'''Find the full size image urls from the html page and return as a list'''
	soup = bs4.BeautifulSoup(html, "html5lib")
	divs = soup.find_all('div', class_='RawImageUTC')
	img_urls = []
	for div in divs:
		for child in div.children:
			if(child.name == 'a'):
				# Get only full resolution image urls
				if(child['href'][109] != 'T'):
					img_urls.append(child['href'])
	# Sort to ensure left side image urls are first
	img_urls.sort()
	return img_urls

def create_anaglyphs(img_urls):
	anaglyphs = []
	for i in range(int(len(img_urls)/2)):
		left_url = img_urls[i]
		right_url = get_right_url(left_url)
		ag = create_anaglyph(left_url, right_url)
		anaglyphs.append(ag)
	return anaglyphs

def create_movie(images, sol, file_name):
	fig = pp.figure(figsize=(500/72,500/72), dpi=72)
	axes = pp.Axes(fig, [0,0,1,1])
	axes.set_axis_off()
	fig.add_axes(axes)

	ffmpeg = anim.writers['ffmpeg']
	writer = ffmpeg(fps=3, bitrate=1000)
	out_file = file_name + '.mp4'
	with writer.saving(fig, out_file, 72):
		for img in images:
			pp.imshow(img, interpolation='none')
			writer.grab_frame()
	print("File saved: ", out_file)

def get_input():
	'''Get user input until a valid day is entered, then return the day and list of image urls'''
	while True:
		sol = input("Enter the number of the Mars solar day to make a movie of: ")
		url = HAZCAM_URL.format(sol)
		response = requests.get(url)
		if response.ok:
			# Enure image exist for the solar day
			img_urls = get_img_urls(response.text)
			if len(img_urls) > 0:
				return (sol, img_urls)
			else:
				print("Could not obtain images for that solar day")
		else:
			print("Could not obtain a response for that solar day")

def main():
	print("Welcome to Mars movie maker!\n"
		"Let's make a movie from the Curiosity Rover's front hazcams\n"
		"See the possible options for solar days here:\n"
		"https://mars.nasa.gov/msl/multimedia/raw\n")
	sol, img_urls = get_input()
	print("Creating anaglyph images")
	anaglyphs = create_anaglyphs(img_urls)
	file_name = 'MarsSol' + sol
	print("Creating movie")
	create_movie(anaglyphs, sol, file_name)
	ans = input("Convert movie to .gif format? (y/n)")
	if ans == 'y':
		subprocess.call("ffmpeg -y -i {}.mp4 -b:v 2000k {}.gif".format(file_name, file_name))
		print('\ngif file created')


if __name__ == "__main__":
    main()