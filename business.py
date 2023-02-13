import json
from abstract_root import AbstractRoot, NULL_KEY, NULL_OBJECT

class Business(AbstractRoot):
	# The implementation of manager.io Business object

	def __init__(self, *args):
		if len(args) == 2:
			self.name = args[0]
			super().__init__(args[1])
		elif isinstance(args[0], str):
			raw_api_response = args[0]
			parsed_response = json.loads(raw_api_response)
			self.name = parsed_response["Name"]
			super().__init__(parsed_response["Key"])
		elif isinstance(args[0], dict):
			dict_response = args[0]
			self.name = dict_response["Name"]
			super().__init__(dict_response["Key"])

	def to_dict(self) -> dict:
		result_dict = dict()
		result_dict["Name"] = f"{self.name}"
		result_dict["Key"] = f"{self.key}"
		return result_dict

	def to_json(self) -> str:
		return json.dumps(self.to_dict())
