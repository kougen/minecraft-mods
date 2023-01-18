import os
from termcolor import colored
from getch import getch, pause
import curses
from mod import ModManager

KEYS_ENTER = (curses.KEY_ENTER, b"\n", b"\r")
KEYS_UP = (curses.KEY_UP,b'H', b'k')
KEYS_DOWN = (b'P', b'j')
KEYS_SELECT = (curses.KEY_RIGHT, b' ')

screen: "curses._CursesWindow"

class Menu:
	def __init__(self, title: str, options: list[str], indicator='->', selected=0):
		# file_path = 'terminal_output.txt'
		# sys.stdout = open(file_path, "w")
		
		self.title = title
		self.indicator = indicator
		self.indicator_space = ' ' * len(indicator)
		self.options = options
		self.selected = selected
	
	def show(self):
		move = None
		page = 0
		max_page = (len(self.options) / 10) * 10
		if max_page < len(self.options):
			max_page += 1
		print(max_page)
		while move not in KEYS_ENTER:
			os.system('cls')
			print(f'Page: {page}, Selected: {self.selected}')
			for index in range(page * 10, 10 + page * 10):
				if index < len(self.options):
					option = self.options[index]
					if index == self.selected:
						print(colored(f'{self.indicator} {option}', "green"))
					else:
						print(f'{self.indicator_space} {option}')
			move = getch()
			if move in KEYS_DOWN and self.selected + 1 < len(self.options):
				self.selected += 1
			if move in KEYS_UP and self.selected - 1 >= 0:
				self.selected -= 1
			if self.selected >= page * 10 + 10:
				page += 1
			elif self.selected <= (page * 10) - 1:
				page -= 1
		return self.options[self.selected]


mods = ModManager(True)

menu = Menu("Test Menu", mods.mod_list)
mod = menu.show()
print(f'Selected item: {mod.filename}')