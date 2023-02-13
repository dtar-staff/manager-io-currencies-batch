from datetime import datetime
import json

from abstract_root import AbstractRoot, NULL_OBJECT, NULL_KEY


class CurrencyDescription:
	def __init__(self, *args):
		if len(args) > 1:
			self.code = args[0]
			self.name = args[1]
			if len(args) > 2:
				self.symbol = args[2]
			else:
				self.symbol = ""
		elif len(args) == 1:
			if isinstance(args[0], str):
				info_dict = json.loads(args[0])
				self.code = info_dict["Code"]
				self.name = info_dict["Name"]
				self.symbol = info_dict.get("Symbol", "")
			elif isinstance(args[0], str):
				info_dict = args[0]
				self.code = info_dict["Code"]
				self.name = info_dict["Name"]
				self.symbol = info_dict.get("Symbol", "")

	def to_dict(self) -> dict:
		result_dict = dict()
		result_dict["Code"] = f"{self.code}"
		result_dict["Name"] = f"{self.name}"
		result_dict["Symbol"] = f"{self.symbol}"
		return result_dict

	def to_json(self) -> str:
		return json.dumps(self.to_dict())


class BaseCurrency(AbstractRoot):
	# The implementation of manager.io Base Currency object
	def __init__(self, *args):
		if len(args) == 5:
			self.description = CurrencyDescription(code=args[0], name=args[1], symbol=args[2])
			super().__init__(args[3], args[4])
		elif len(args) == 3:
			if isinstance(args[0], str):
				parsed_response = json.loads(args[0])
				self.description = CurrencyDescription(parsed_response["Code"], parsed_response["Name"], parsed_response.get("Symbol"))
				super().__init__(args[1], args[2])
			elif isinstance(args[0], dict):
				dict_response = args[0]
				self.description = CurrencyDescription(dict_response["Code"], dict_response["Name"], parsed_response.get("Symbol"))
				super().__init__(args[1], args[2])

	def to_dict(self) -> dict:
		return self.description.to_dict()

	def to_json(self) -> str:
		return json.dumps(self.to_dict())



class ForeignCurrency(AbstractRoot):
	# The implementation of manager.io Foreign Currency object

	def __init__(self, *args):
		self.description = args[0]
		if len(args) == 4:
			self.name = args[1]
			super().__init__(args[2], args[3])
		else:
			if isinstance(args[1], str):
				parsed_response = json.loads(args[1])
				self.name = parsed_response["Name"]
				super().__init__(parsed_response["Key"], args[2])

			elif isinstance(args[1], dict):
				dict_response = args[1]
				self.name = dict_response["Name"]
				super().__init__(dict_response["Key"], args[2])


	def to_dict(self) -> dict:
		return self.description.to_dict()

	def to_json(self) -> str:
		return json.dumps(self.to_dict())
