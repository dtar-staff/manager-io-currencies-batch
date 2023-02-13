from datetime import datetime

from abstract_root import AbstractRoot, NULL_OBJECT, NULL_KEY
import json
from math import floor

DATE_SEPARATOR="-"
NULL_DATE_STR = "1970" + DATE_SEPARATOR + "01" + DATE_SEPARATOR + "01"
FIRST_JAN_1970_TICKS = 621355968000000000
NULL_DATE = datetime(year=1970, month=1, day=1)

def date_from_api_response(date:str)->datetime:
	year, month, day = [int(x) for x in date.split(DATE_SEPARATOR)]
	return datetime(year=year, month=month, day=day)

def date_to_api_request(date:datetime) -> str:
	return f"{date.year}-{date.month:02}-{date.day:02}"

def date_from_ticks(ticks:int) -> datetime:
	return datetime.fromtimestamp((ticks - FIRST_JAN_1970_TICKS) // 10**7)

def truncate_float(fl_number: float, decimals=4) -> float:
	return float(format(fl_number, f".{decimals}f"))


class ExchangeRate(AbstractRoot):
	# The implementation of manager.io Exchange Rate object

	def __init__(self, *args):
		if len(args) == 5:
			self.date = args[0]
			self.currency_key = args[1]
			self.rate = args[2]
			super().__init__(args[3], args[4])
		elif len(args) == 3:
			parent = args[2]
			if isinstance(args[0], str):
				parsed_response_1 = json.loads(args[0])
				parsed_response_2 = json.loads(args[1])
				self.date = date_from_api_response(parsed_response_1.get("Date", NULL_DATE_STR))
				self.currency_key = parsed_response_1["Currency"]
				self.rate = parsed_response_1["Rate"]
				self.name = parsed_response_2["Name"]
				self.timestamp = date_from_ticks(parsed_response_2["Timestamp"])
				super().__init__(parsed_response_2["Key"], parent)
			elif isinstance(args[0], dict):
				dict_response_1 = args[0]
				dict_response_2 = args[1]
				self.date = date_from_api_response(dict_response_1.get("Date", NULL_DATE_STR))
				self.currency_key = dict_response_1["Currency"]
				self.rate = dict_response_1["Rate"]
				self.name = dict_response_2["Name"]
				self.timestamp = date_from_ticks(dict_response_2["Timestamp"])
				super().__init__(dict_response_2["Key"], parent)

	def to_dict(self) -> dict:
		result_dict = dict()
		result_dict["Date"] = date_to_api_request(self.date)
		result_dict["Currency"] = f"{self.currency_key}"
		result_dict["Rate"] = truncate_float(self.rate)
		return result_dict

	def to_json(self) -> str:
		return json.dumps(self.to_dict())
