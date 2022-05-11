import time
import sys, os

colors_enabled = False

def enable_colors():
	global colors_enabled
	colors_enabled = True
	os.system("color")

class Option:
	def __init__(self, name, description, func, color=""):
		self.name = name
		self.description = description if description != "" else "No description set."
		self.func = func
		self.color = self.get_color(color) if colors_enabled else ""

		# if color is unset there's no need to reset
		self.reset_color = "" if self.color == "" else self.get_color("reset")

	def get_color(self, color):
		color = color.lower()

		if not colors_enabled:
			return ""

		clr = ""

		# for multiple text decorations => "red;bold;underline"
		if ";" in color:
			for col in color.split(";"):
				clr += self.get_color(col)

			return clr

		return {
			"black": "\033[30m",

			"dark_red": "\033[31m",

			"dark_green": "\033[32m",

			"dark_yellow": "\033[33m",

			"dark_blue": "\033[34m",

			"purple": "\033[35m",

			"dark_cyan": "\033[36m",

			"light_gray": "\033[37m",

			"gray": "\033[90m",

			"red": "\033[91m",

			"green": "\033[92m",

			"yellow": "\033[93m",

			"blue": "\033[94m",

			"pink": "\033[95m",

			"cyan": "\033[96m",

			"white": "\033[97m",

			"reset": "\033[0m",

			"bold" : "\033[1m",

			"underline" : "\033[4m",

			"no_underline" : "\033[24m"
			
			}.get(color, "")

class Menu:

	def __init__(self, caller = None, title = "Select your option:", help=True, exit=True, back=True):
		self.options = []
		self.caller = caller
		self.title = title

		self.inited_after = False

		self.back_opt = back
		self.help_opt = help
		self.exit_opt = exit

	def add_option(self, opt):
		number = len(self.options) + 1
		self.options.append((number, opt))

	# add default options at the end
	def init_after(self):
		if self.help_opt:
			self.add_option(Option("Help", "Prints the description of specific option.", self.help))

		if self.caller is not None and self.back_opt:
			self.add_option(Option("Back", "Goes to previous menu.", self.back))

		if self.exit_opt:
			self.add_option(Option("Exit", "Exits the program.", self.exit))

	def help(self, caller):
		# caller is always self

		print(f"Select which option you want to help with (1-{len(self.options)})")
		opt = self.validate_input()

		if opt is None:
			print("\nInvalid option number\n")
		else:
			print(f"\nDescription for {opt.name}: ")
			print(opt.description)

		self.print()
		self.get_input()

	def back(self, caller):
		# caller is always self
		if self.caller is None: return

		self.caller.print()
		self.caller.get_input()

	def exit(self, caller):
		print("\nExiting program..\n")
		sys.exit(0)

	def print(self):
		# call init after to add default options
		if not self.inited_after: self.init_after()
		# set this to True so it only runs once
		self.inited_after = True

		print( \
	f'''\r
    +-------------------------------+
    |                               |
    | {self.title}{(30-len(self.title)) * " "}|
    |                               |
''' \
	, end="")

		# enumerate gives current index
		for i, (number, opt) in enumerate(self.options):
			
			s = f"    | {opt.color}[{number}]: {opt.name}{opt.reset_color}"

			# colors are also strings but they aren't visible so we need to get rid of them
			s_len = len(s) - len(opt.color) - len(opt.reset_color)

			spaces = (36 - s_len) * " " + "|"

			# if option is the last one, don't add new line
			end = "\n" if i != len(self.options) - 1 else ""

			print(s + spaces, end=end)

		print( \
	'''
    |                               |
    +-------------------------------+
	''' \
	)

	def get_input(self):
		opt = self.validate_input()

		while opt is None:
			print("\nInvalid option\n")
			self.print()
			opt = self.validate_input()

		opt.func(self)

	def validate_input(self):
		try:
			opt = int(input("> "))

			for num, option in self.options:
				if opt == num:
					return option

		except ValueError:
			return None

		return None
