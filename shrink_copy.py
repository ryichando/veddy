#
# Author: Ryoichi Ando (https://ryichando.graphics)
# License: CC BY-SA 4.0 (https://creativecommons.org/licenses/by-sa/4.0/)
#
import os, sys, argparse, shutil, utility
from PIL import Image
#
def create_dir(dir):
	if not os.path.exists(dir):
		print( f'create dir "{dir}"')
		os.makedirs(dir)
#
def check_skip(path,names):
	if names:
		for name in names:
			if name in root:
				print( f'skipping "{path}"' )
				return True
	return False
#
if __name__ == '__main__':
	#
	parser = argparse.ArgumentParser()
	parser.add_argument('--source',help='source directory path')
	parser.add_argument('--target',help='target directory path')
	parser.add_argument('--scale',default=0.25,type=float,help='scaling factor')
	parser.add_argument('--exclude',nargs='*',help="Ignore list")
	args = parser.parse_args()
	#
	assert( os.path.isdir(args.source) )
	if os.path.exists(args.target):
		while True:
			answer = input(f'Delete "{args.target}" ? [Y/n]: ').lower()
			if answer == 'y':
				shutil.rmtree(args.target)
				break
			elif answer == 'n':
				sys.exit()
	#
	os.mkdir(args.target)
	for root, dirs, files in os.walk(args.source, topdown=False):
		if check_skip(root,args.exclude):
			continue
		relpath = os.path.relpath(root,args.source)
		for file in files:
			if check_skip(file,args.exclude):
				continue
			path_from = os.path.join(root,file)
			path_target = os.path.join(args.target,relpath,file)
			if file.lower().endswith(utility.get_image_extensions()):
				dir = os.path.dirname(path_target)
				create_dir(dir)
				with Image.open(path_from) as image:
					o_width,o_height = image.size
					n_width = int(args.scale * o_width)
					n_height = int(args.scale * o_height)
					print( f'resize "{path_from} ({o_width}x{o_height})" ==> "{path_target}" ({n_width}x{n_height})')
					image.resize((n_width,n_height),Image.LANCZOS).save(path_target)
			if file.lower().endswith(utility.get_video_extensions()):
				dir = os.path.dirname(path_target)
				create_dir(dir)
				shutil.copy(path_from,path_target)