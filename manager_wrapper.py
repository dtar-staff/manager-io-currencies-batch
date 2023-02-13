import json
import requests
from abstract_root import NULL_OBJECT, NULL_KEY
from datetime import datetime

from business import Business
from chapter import BusinessChapter
from currency import ForeignCurrency, BaseCurrency, CurrencyDescription
from exchange_rate import ExchangeRate, date_from_ticks, NULL_DATE

import logger

ROOT_API_URL="192.168.16.228/api"
PROTOCOL="http://"
JSON_EXT=".json"
AUTH_USER="administrator"
AUTH_PASSWORD="YaEbalEtuHuiniu123!"
URL_SEPARATOR="/"


def url_construct(iterable_object) -> str:
	"""Creates url for json api
	Concatenates all keys and adds .json extension"""
	result_string = ""
	for string in iterable_object:
		if type(string) == str:
			if len(string) > 0 and string != NULL_KEY:
				result_string += URL_SEPARATOR + string
	return PROTOCOL + ROOT_API_URL + result_string + JSON_EXT

def get_full_access_key(object):
	full_key = ""
	array_of_keys = []
	current_object = object
	while current_object.key != NULL_KEY:
		array_of_keys.append(current_object.key)
		current_object = current_object.parent
	array_of_keys.reverse()
	for key in array_of_keys:
		full_key += URL_SEPARATOR + key
	return full_key[1:]

def perform_get_request(parent_key, key)->str:
	url_components = parent_key, key
	url = url_construct(url_components)
	auth=(AUTH_USER, AUTH_PASSWORD)
	r = requests.get(url, auth=auth)
#	logger.log("GET", url)
	return r.text

def perform_post_request(parent_key, key, json) -> str:
	url_components = parent_key, key
	url = url_construct(url_components)
	auth=(AUTH_USER, AUTH_PASSWORD)
#	logger.log("POST", url, json)
	resp_text = requests.post(url, auth=auth, data=json).text
	return resp_text

def perform_put_request(parent_key, key, json) -> str:
	url_components = parent_key, key
	url = url_construct(url_components)
	auth=(AUTH_USER, AUTH_PASSWORD)
#	logger.log("PUT",url, json)
	resp_text = requests.put(url, auth=auth, data=json).text
	logger.log(resp_text)
	return resp_text



def get_businesses()-> list:
	raw_response = perform_get_request(NULL_KEY, NULL_KEY)
	array_of_dicts = json.loads(raw_response)
	array_of_businesses = [Business(x) for x in array_of_dicts]
	return array_of_businesses

def get_business_chapters(business: Business) -> dict:
	parent_key = get_full_access_key(business)
	raw_response = perform_get_request(parent_key, NULL_KEY)
	array_of_dicts = json.loads(raw_response)
	array_of_chapters = [BusinessChapter(x, business) for x in array_of_dicts]
	dict_of_chapters = dict()
	for chapter in array_of_chapters:
		dict_of_chapters[chapter.name] = chapter
	return dict_of_chapters

def get_base_currency(business: Business) -> BaseCurrency:
	chapters = get_business_chapters(business)
	parent_key = get_full_access_key(chapters["BaseCurrency"])
	raw_response = perform_get_request(parent_key, NULL_KEY)
	return BaseCurrency(raw_response, chapters["BaseCurrency"].key, chapters["BaseCurrency"])


def _get_foreign_currencies(chapter: BusinessChapter) -> dict:
	parent_key = get_full_access_key(chapter)
	raw_response = perform_get_request(parent_key, NULL_KEY)
	array_of_dicts = json.loads(raw_response)
	dict_of_currencies = dict()
	for currency_dict in array_of_dicts:
		raw_currency_response = perform_get_request(parent_key, currency_dict["Key"])
		currency_description = CurrencyDescription(raw_currency_response)
		dict_of_currencies[currency_description.code] = ForeignCurrency(currency_description, currency_dict, chapter)
	return dict_of_currencies

def get_foreign_currencies(business: Business) -> dict:
	foreign_currencies = dict()
	chapters = get_business_chapters(business)
	if chapters.get("ForeignCurrency"):
		foreign_currencies = _get_foreign_currencies(chapters["ForeignCurrency"])
	return foreign_currencies


def _get_exchange_rates(chapter: BusinessChapter, after=NULL_DATE, before=datetime.now()) -> dict:
	parent_key = get_full_access_key(chapter)
	raw_response = perform_get_request(parent_key, NULL_KEY)
	array_of_dicts = json.loads(raw_response)
	dict_of_exchange_rates = dict()
	for exchange_rate_dict in array_of_dicts:
		month, day, year = [int(x) for x in exchange_rate_dict["Name"].split(" ")[-1].split("/")] # Getting date from name is not best idea, but better than a timestamp
		timestamp = datetime(year=year, month=month, day=day)
		if timestamp < before and timestamp > after:
			raw_exchange_rate_response = perform_get_request(parent_key, exchange_rate_dict["Key"])
			exchange_rate_description = json.loads(raw_exchange_rate_response)
			dict_of_exchange_rates[exchange_rate_description["Currency"]] = []
			dict_of_exchange_rates[exchange_rate_description["Currency"]].append(ExchangeRate(exchange_rate_description, exchange_rate_dict, chapter))
	return dict_of_exchange_rates

def get_exchange_rates(business: Business, after=NULL_DATE, before=datetime.now()) -> dict:
	exchange_rates = dict()
	chapters = get_business_chapters(business)
	if chapters.get("ExchangeRate"):
		exchange_rates = _get_exchange_rates(chapters["ExchangeRate"], after=after, before=before)
	return exchange_rates



def set_exchange_rate(business: Business, currency: ForeignCurrency, rate: float, date=datetime.now()):
	chapters = get_business_chapters(business)
	exchange_chapter = chapters.get("ExchangeRate")
	if exchange_chapter:
		parent_key = get_full_access_key(exchange_chapter)
		ex_rate = ExchangeRate(date, currency.key, rate, NULL_KEY, exchange_chapter)
		resp = perform_post_request(parent_key, NULL_KEY, ex_rate.to_json())
		resp_dict = json.loads(resp)
		if resp_dict["Success"] == True:
			ex_rate.key = resp_dict["Key"]
			return ex_rate
		logger.log(resp_dict)
	return False

def update_exchange_rate(exchange_rate: ExchangeRate, rate: float, date=datetime.now()):
	exchange_rate_full_key = get_full_access_key(exchange_rate)
	exchange_rate.rate = rate
	exchange_rate.date = date
	resp = perform_put_request(exchange_rate_full_key, NULL_KEY, exchange_rate.to_json())
	resp_dict = json.loads(resp)
	if resp_dict["Success"] == True:
		return True
	return False
