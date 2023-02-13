from config import LOG_NAME, LOG_DIR, LOG_EXT
from datetime import datetime
import os
import sys

def log(*args):
	message = ""
	for argument in args:
		message += str(argument) + " "
	if not os.path.isdir(LOG_DIR):
		os.mkdir(LOG_DIR)
	with open(LOG_DIR + LOG_NAME + LOG_EXT, "a") as f:
		f.write(f"{datetime.now().isoformat()}: {message}\n")

def clear_log():
	if os.path.isdir(LOG_DIR):
		if os.path.isfile(LOG_DIR + LOG_NAME + LOG_EXT):
			os.remove(LOG_DIR + LOG_NAME + LOG_EXT)
