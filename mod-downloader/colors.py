
UNDERLINE = "(!u!)"
BOLD = "(!b!)"
RESET_ALL ="(!reset_all!)"
RESET_STYLE ="(!reset_s!)"
RESET_COLOR ="(!reset_c!)"

BLACK = "(!black!)"
RED = "(!red!)"
GREEN = "(!green!)"
YELLOW = "(!yellow!)"
GRAY = "(!gray!)"
PINK = "(!pink!)"

ansi_dict = {
	RESET_ALL: "\033[0m", 
	RESET_COLOR: "\033[39m", 
	BLACK : "\033[30m",
	RED : "\033[31m",
	GREEN : "\033[32m",
	YELLOW : "\033[33m", 
	"(!blue!)": "\033[34m",
	"(!purple!)": "\033[35m",
	"(!cyan!)": "\033[36m",
	"(!white!)": "\033[37m",
	PINK: "\033[38;5;213m",
	GRAY: "\033[90m",
	BOLD: "\033[1m",
	UNDERLINE: "\033[4m" }

def colorize(text: str, opstional_style=''):
	full_str = f'{opstional_style}{text}' + RESET_ALL
	for code in ansi_dict:
		full_str = full_str.replace(code, ansi_dict[code])
	return full_str