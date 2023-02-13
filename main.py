#!/usr/bin/python3

import csv
import os
import sys
from get_currencies_template import *
from config import *
import cache_or_new
from datetime import datetime
import tkinter as tk
import tkinter.messagebox
from tkinter import ttk
from exchange_rate import date_from_api_response
import logger
from cache import clear_cache


def if_dir_not_empty():
	logger.log("Started cleaning templates directory")
	# If it's a real directory
	# Remove all files in directory
	for file in os.listdir(path):
		fullpath = path + file
		if os.path.isfile(fullpath):
			logger.log(fullpath)
			os.remove(fullpath)
		else:
			logger.log(fullpath)
			os.rmdir(fullpath)
	logger.log("Templates directory cleared.")

def download_templates():
	logger.log("Downloading templates")

	foreign_businesses = cache_or_new.fb()
	fb_ordered_by_base_currency = cache_or_new.fbb(foreign_businesses)
	currencies_tree = cache_or_new.ct(fb_ordered_by_base_currency)

	with open(path + TEMPLATE_NAME + CSV_EXT, "w") as csvfile:
		csv_writer = csv.writer(csvfile)
		csv_writer.writerow(["Data", datetime.now().date().isoformat()])
		for code in currencies_tree.keys():
				csv_writer.writerow(["Waluta_bazowa", code])
				csv_writer.writerow(["Ilość_kursów", len(currencies_tree[code])])
				for foreign_currency_code in currencies_tree[code]:
					csv_writer.writerow([foreign_currency_code])
	logger.log("Templates downloaded")



def download_button_click():
	logger.log("User clicked download")
	if len(os.listdir(path)) > 0:
		user_agrees = tk.messagebox.askokcancel(title="Folder", message="Folder dla szablonów nie jest pustym. Czy chcesz wyczyścić i kontynuować?")
		if user_agrees:
			logger.log("User is agree to clean templates directory")
			if_dir_not_empty()
	progress = ttk.Progressbar(mode="indeterminate")
	progress.pack()
	progress.start()
	status["text"] = "Pobieram szablon..."
	window.update()
	download_templates()
	status["text"] = ""
	progress.stop()
	progress.pack_forget()
	window.update()
	tk.messagebox.showinfo(title="Operacja skończyła się pomyślnie", message="Szablon pobrano.")

def open_button_click():
	logger.log("User clicked open")
	os.popen("xdg-open " + full_template_path)

def upload_button_click():
	logger.log("User clicked upload")
	if not os.path.isfile(full_template_path):
		tk.messagebox.showinfo(title="Brak szablonu", message=f"Brakuje szablonu [{full_template_path}]")
	else:
		progress = ttk.Progressbar(mode="indeterminate")
		progress.pack()
		progress.start()
		status["text"] = "Ustawiam kursy..."
		window.update()
		upload_exchange_rates()
		status["text"] = ""
		progress.stop()
		progress.pack_forget()
		window.update()
		tk.messagebox.showinfo(title="Operacja skończyła się pomyślnie", message="Kursy walut zostały ustawione.")


def upload_exchange_rates():
	logger.log("Started uploading exchange rates")
	date = get_date_from_csv(full_template_path)
	date = date_from_api_response(date)
	exchanges = get_exchange_rates_from_csv(full_template_path)

	foreign_businesses = cache_or_new.fb()
	fb_ordered_by_base_currency = cache_or_new.fbb(foreign_businesses)
	exchanges_tree = cache_or_new.xtr(fb_ordered_by_base_currency, date)

	current_business_has_rate = False

	for current_base in fb_ordered_by_base_currency.keys():	
#		logger.log(f"current base = {current_base}")
		for business in fb_ordered_by_base_currency[current_base]:
#			logger.log(f"business.name = {business.name}")
			f_currencies = cache_or_new.fcu(business)
			for f_currency_code in f_currencies.keys():
#				logger.log(f"f_currency_code = {f_currency_code}")
				f_currency = f_currencies[f_currency_code]
				for rate in exchanges[current_base]:
#					logger.log(f"rate = {rate}")
					if f_currency_code in rate.keys():
#						logger.log(f"f_currency_code is in rate.keys()")
#						logger.log(f"Processing rate: {rate}")
						exchange_code = f_currency_code + "/" + current_base
						logger.log(f"Target: {exchange_code} = {rate[f_currency_code]} @ {business.name}")
						if exchange_code in exchanges_tree.keys():
#							logger.log(f"{exchange_code} is in exchanges_tree.keys()")
							for ex_rate_list in exchanges_tree[exchange_code]:
#								logger.log(f"ex_rate_list = {[[y.to_dict() for y in x] for x in exchanges_tree[exchange_code]]}")
								for ex_rate in ex_rate_list:
#									logger.log(f"ex_rate = {ex_rate.currency_key}")
									if ex_rate.parent.parent.key == business.key:
										logger.log(f"UPDating existing {exchange_code} @ {business.name} = {rate[f_currency_code]} [{ex_rate.key}]")
										manager.update_exchange_rate(ex_rate, rate[f_currency_code], date)
										current_business_has_rate = True
						if not current_business_has_rate:
								logger.log(f"SETting new {exchange_code} @ {business.name} = {rate[f_currency_code]}")
								manager.set_exchange_rate(business, f_currency, rate[f_currency_code], date)
						current_business_has_rate = False
	logger.log("Exchange rates uploaded")


def get_raw_data_from_csv(filename) -> list:
	raw_data = []
	with open(full_template_path) as f:
		csv_reader = csv.reader(f)
		for row in csv_reader:
			raw_data.append(row)
	return raw_data


def get_date_from_csv(filename) -> str:
	date = ""
	raw_data = get_raw_data_from_csv(filename)
	if raw_data[0][0] == "Data" and len(raw_data) > 1:
		date = raw_data[0][1]
	return date



def get_exchange_rates_from_csv(filename) -> dict:
	raw_data = get_raw_data_from_csv(filename)
	exchanges = {}
	del raw_data[0]
	count = 0
	i = 0
	current_base = ""
	overall = len(raw_data)
	while i < overall:
		if raw_data[i][0] == "Waluta_bazowa" and len(raw_data[i]) > 1:
			current_base = raw_data[i][1]
			exchanges[current_base] = []
			i += 1
			if raw_data[i][0] == "Ilość_kursów" and len(raw_data[1]) > 1:
				count = int(raw_data[i][1])
				i += 1
				for j in range(i, i+count):
					if len(raw_data[j]) > 1:
						currency, rate = raw_data[j][0], raw_data[j][1].replace(",", ".")
						if len(rate) > 0:
							rate = float(rate)
							exchanges[current_base].append({currency: rate})
				i += count
			else:
				logger.log("Template structure error: cannot determine count of exchange rates")
				logger.log(raw_data)
				logger.log(f"At row: {i}")
				return {}
		else:
			logger.log("Template structure error: base currency not set")
			logger.log(raw_data)
			logger.log(f"At row: {i}")
			return {}
	return exchanges


def clear_cache_button_click():
	logger.log("User clicked clear cache and log")
	clear_cache()
	logger.clear_log()
	tk.messagebox.showinfo(title="Posprzątałem", message="Pamięć podręczna została wyczyszczoną.")


path = TEMPLATES_DIR
if not path.endswith("/"):
	path += "/"

full_template_path = path + TEMPLATE_NAME + CSV_EXT


logger.log("\n\nSession started")
window = tk.Tk()
window.title("Waluty w Managery")
window.geometry("400x250")
download_button = tk.Button(text=">>>Pobierz szablon<<<", command=download_button_click)
download_button.pack()
open_button = tk.Button(text="Otwórz szablon", command=open_button_click)
open_button.pack()
upload_button = tk.Button(text="-=#Ustaw kursy walut#=-", command=upload_button_click)
upload_button.pack()
clear_cache_button = tk.Button(text="Wyczyść pamięć podręczną i dzieńnik", command=clear_cache_button_click)
clear_cache_button.pack()
status = tk.Label(text="")
status.pack()
window.mainloop()
