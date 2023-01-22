import os
from getch import getch, pause
import curses
from abc import abstractmethod
from colors import *


KEYS_ENTER = (curses.KEY_ENTER, b"\n", b"\r")
KEYS_UP = (curses.KEY_UP,b'H', b'k')
KEYS_DOWN = (b'P', b'j')
KEYS_SELECT = (curses.KEY_RIGHT, b' ')
KEYS_ESC = b'\x1b'

screen: "curses._CursesWindow"

class Menu:
	def __init__(self, title: str, options: list, callback, indicator: str, selected: int, shown_content: int):
		self.title = title
		self.indicator = indicator
		self.indicator_space = ' ' * len(indicator)
		self.options = options
		self.selected = selected
		self.page = 0
		self.shown_content = shown_content
		self.callback = callback

	def __str__(self):
		return self.title

	def action_check(self) -> bytes:
		move = getch()
		if move in KEYS_DOWN and self.selected + 1 < len(self.options):
			self.selected += 1
		if move in KEYS_UP and self.selected - 1 >= 0:
			self.selected -= 1
		if self.selected >= self.page * self.shown_content + self.shown_content:
			self.page += 1
		elif self.selected <= (self.page * self.shown_content) - 1:
			self.page -= 1
		return move

	@abstractmethod
	def show(self, parent=''):
		pass


class SingleMenu(Menu):
	def __init__(self, title: str, options: list, callback, indicator='->', selected=0, shown_content=15):
		super().__init__(title, options, callback, indicator, selected, shown_content)
	
	def show(self, parent=''):
		if parent != '':
			title = f'{parent} -> {self.title}'
		else:
			title = self.title
		move = None
		while move not in KEYS_ENTER:
			os.system('cls')
			print(f'{title}')
			for index in range(self.page * self.shown_content, self.shown_content + self.page * self.shown_content):
				if index < len(self.options):
					option = self.options[index]
					if index == self.selected:
						print(colorize(f'{self.indicator} {option}'))
					else:
						print(colorize(f'{self.indicator_space} {option}'))
			move = self.action_check()
			if move in KEYS_ESC:
				return None
		if self.callback is not None:
			self.callback(self.options[self.selected])
		return self.options[self.selected]


class MultiMenu(Menu):
	def __init__(self, title: str, options: list, callback, indicator='->', selected=0, shown_content=15, select_open='[', select_close=']', select_mark='*', unselect_mark=' '):
		super().__init__(title, options, callback, indicator, selected, shown_content)

		self.unselected = f'{select_open}{unselect_mark}{select_close}'
		self.selected_in = f'{select_open}{select_mark}{select_close}'
		
	def show(self, parent=''):
		if parent != '':
			title = f'{parent} -> {self.title}'
		else:
			title = self.title
		move = None
		selection = []
		while move not in KEYS_ENTER:
			os.system('cls')
			print(f'{title}')
			for index in range(self.page * self.shown_content, self.shown_content + self.page * self.shown_content):
				if index < len(self.options):
					option = self.options[index]
					if index == self.selected:
						if option in selection:
							print(colorize(f'{self.indicator} {self.selected_in} {option}'))
						else:
							print(colorize(f'{self.indicator} {self.unselected} {option}'))
					else:
						if option in selection:
							print(colorize(f'{self.indicator_space} {self.selected_in} {option}'))
						else:
							print(colorize(f'{self.indicator_space} {self.unselected} {option}'))
			move = self.action_check()
			if move in KEYS_SELECT:
				if self.options[self.selected] in selection:
					selection.remove(self.options[self.selected])
				else:
					selection.append(self.options[self.selected])
			if move in KEYS_ESC:
				return None
		self.callback(selection)


class MenuWrapper(Menu):
	def __init__(self, title: str, options: list[Menu], indicator='->', selected=0, shown_content=15):
		super().__init__(title, options, None, indicator, selected, shown_content)

	def show(self, parent=''):
		if parent != '':
			title = f'{parent} -> {self.title}'
		else:
			title = self.title
		move = KEYS_ENTER[1]  # type: bytes
		while move not in KEYS_ESC:
			os.system('cls')
			print(f'{title}')
			for index in range(self.page * self.shown_content, self.shown_content + self.page * self.shown_content):
				if index < len(self.options):
					option = self.options[index]
					if index == self.selected:
						print(colorize(f'{self.indicator} {option}'))
					else:
						print(f'{self.indicator_space} {option}')
			move = self.action_check()
			if move in KEYS_ENTER:
				self.options[self.selected].show(self.title)