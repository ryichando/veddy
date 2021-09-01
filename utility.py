import os, subprocess, fnmatch, pathlib, requests
from clint.textui import progress
from urllib.parse import urlparse
from PIL import Image
#
# Video and image extensions
def get_video_extensions():
	return ( '.mp4', '.mov', '.mpeg', '.avi' )
#
def get_image_extensions():
	return ( '.png', '.jpg', '.jpeg', '.bmp', '.tiff' )
#
# https://stackoverflow.com/questions/43878953/how-does-one-detect-if-one-is-running-within-a-docker-container-within-python
def in_docker():
	return os.environ.get('AM_I_IN_A_DOCKER_CONTAINER',False)
#
# https://stackoverflow.com/questions/3844430/how-to-get-the-duration-of-a-video-in-python
def get_video_duration( path ):
	#
	return float(subprocess.run(
		'ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1'.split()+[path],
		stdout=subprocess.PIPE,stderr=subprocess.STDOUT).stdout)
#
# https://stackoverflow.com/questions/2017843/fetch-frame-count-with-ffmpeg
def get_video_frame_count( path ):
	#
	return int(subprocess.run(
		'ffprobe -v error -count_packets -show_entries stream=nb_read_packets -of csv=p=0'.split()+[path],
		stdout=subprocess.PIPE,stderr=subprocess.STDOUT).stdout)
#
# https://stackoverflow.com/questions/27792934/get-video-fps-using-ffprobe
def get_video_fps( path ):
	#
	return eval(subprocess.run(
		'ffprobe -v error -select_streams v -of default=noprint_wrappers=1:nokey=1 -show_entries stream=r_frame_rate'.split()+[path],
		stdout=subprocess.PIPE,stderr=subprocess.STDOUT).stdout)
#
# https://stackoverflow.com/questions/17615414/how-to-convert-binary-string-to-normal-string-in-python3
def get_video_resolution( path ):
	#
	return tuple([int(elm) for elm in subprocess.run(
		'ffprobe -v error -select_streams v:0 -show_entries stream=width,height -of csv=s=x:p=0'.split()+[path],
		stdout=subprocess.PIPE,stderr=subprocess.STDOUT).stdout.decode('ascii').replace('\n','').split('x')])
#
# https://stackoverflow.com/questions/6444548/how-do-i-get-the-picture-size-with-pil
def get_image_resolution( path ):
	#
	with Image.open(path) as im:
		return im.size
#
# https://docs.python.org/3/library/fnmatch.html
def get_image_count( path ):
	path_obj = pathlib.Path(path)
	count = 0
	for file in os.listdir(path_obj.parent):
		if fnmatch.fnmatch(file,path_obj.name.replace('%d','*')):
			count += 1
	return count
#
def get_frame_count( path ):
	for ext in get_video_extensions():
		if path.endswith(ext):
			return get_video_frame_count(path)
	for ext in get_image_extensions():
		if path.endswith(ext):
			return get_image_count(path)
	print( f'Unknown type {path}' )
	os.exit(-1)

# https://stackoverflow.com/questions/15644964/python-progress-bar-and-downloads
def download(url,dirpath='.',username='',password=''):
	#
	if username and password:
		r = requests.get(url,stream=True,auth=(username,password))
	else:
		r = requests.get(url,stream=True)
	#
	filename = os.path.basename(urlparse(url).path)
	path = dirpath + '/' + filename
	if r.status_code == 200:
		with open(path,'wb') as f:
			total_length = int(r.headers.get('content-length'))
			print( f'Downloading {filename}' )
			for chunk in progress.bar(r.iter_content(chunk_size=1024), expected_size=(total_length/1024)+1):
				if chunk:
					f.write(chunk)
					f.flush()
		return filename
	else:
		return None