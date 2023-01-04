import argparse
from baselib import minecraft_path, check_path, clear_dir
from modoperations import update_mods, refresh_mods
from mod import ModManager
from sys import exit


parser = argparse.ArgumentParser()
group = parser.add_mutually_exclusive_group()
group.add_argument('--server', '-s', action='store_true', help='Copy the mods to the server\'s folder.')
parser.add_argument('--folder', help='\tSpecify the server\'s folder without prompting.')

group.add_argument('--client', '-c', action='store_true', help='Copy the mods to the client\'s minecraft folder.')
group.add_argument('--local', '-l', action='store_true')

parser.add_argument('--all', '-a', action='store_true')

parser.add_argument('--tidy', '-t', action='store_true')
parser.add_argument('--update', '-u', action='store_true')
args = parser.parse_args()

mods = ModManager(True)


if args.local:
	update_mods(mods, args.update)
elif args.server:
	target_path = args.folder
	while not check_path(target_path):
		target_path = input('Enter the server mod folder path: ')
		if not check_path(target_path):
			print('Server mod folder path does not exist!')
	refresh_mods(mods, target_path)
elif args.client:
	refresh_mods(mods, minecraft_path())
# else:
# 	print('No target specified!')
	# exit(0)

if args.tidy and args.server:
	target_path = args.folder
	while not check_path(target_path):
		target_path = input('Enter the server mod folder path: ')
		if not check_path(target_path):
			print('Server mod folder path does not exist!')
	clear_dir(target_path)
	exit(0)

update_mods(mods, True)
refresh_mods(mods, minecraft_path())
# clear_dir(minecraft_path())
exit(0)
