import manager_wrapper as manager
import logger
from datetime import datetime, timedelta

def get_businesses_with_foreign_currencies() -> list:
	logger.log("Loading foreign currencies...")
	all_businesses = manager.get_businesses()
	businesses_with_foreign_currencies = []
	for business in all_businesses:
		logger.log(f"{business.name} [{business.key}]")
		if manager.get_foreign_currencies(business) != {}:
			businesses_with_foreign_currencies.append(business)
	logger.log("Foreign currencies loaded")
	return businesses_with_foreign_currencies

def get_businesses_ordered_by_base_currency(businesses_list) -> dict:
	logger.log("Loading base currencies")
	businesses_by_base_currency = {}
	for business in businesses_list:
		logger.log(f"{business.name} [{business.key}]")
		base_currency = manager.get_base_currency(business)
		if base_currency.description.code not in businesses_by_base_currency.keys():
			businesses_by_base_currency[base_currency.description.code] = [business]
		else:
			businesses_by_base_currency[base_currency.description.code].append(business)
	return businesses_by_base_currency

def get_currency_codes_list_by_base(businesses_ordered_by_base) -> dict:
	logger.log("Sorting currencies by base...")
	currencies_list_by_base = {}
	base_currencies = list(businesses_ordered_by_base.keys())
	for base_currency_code in base_currencies:
		currencies_list_by_base[base_currency_code] = []
		for business in businesses_ordered_by_base[base_currency_code]:
			foreign_currencies = manager.get_foreign_currencies(business)
			for foreign_currency_code in foreign_currencies.keys():
				if foreign_currency_code != base_currency_code:
					if foreign_currency_code not in currencies_list_by_base[base_currency_code]:
						currencies_list_by_base[base_currency_code].append(foreign_currency_code)
						logger.log(f"Added {foreign_currency_code} to {base_currency_code} list from '{business.name}'")
	logger.log("CTT ready")
	return currencies_list_by_base

def get_exchanges_tree_by_date(businesses_ordered_by_base, date: datetime):
	logger.log(f"Getting exchange rates, date: {date.isoformat()}")
	before = date + timedelta(days=1)
	after = date - timedelta(days=1)
	exchanges_tree = {}
	base_currencies = list(businesses_ordered_by_base.keys())
	for base_currency_code in base_currencies:
		for business in businesses_ordered_by_base[base_currency_code]:
			logger.log(f"{business.name} [{business.key}]")
			foreign_currencies = manager.get_foreign_currencies(business)
			exchange_rates = manager.get_exchange_rates(business, after, before)
			for foreign_currency_code in foreign_currencies.keys():
				fc_key = foreign_currencies[foreign_currency_code].key
				if fc_key in exchange_rates.keys():
					exchange_code = foreign_currency_code + "/" + base_currency_code
					for ex_rate in exchange_rates[fc_key]:
						logger.log(f"Found {exchange_code} for {date.date().isoformat()} = {ex_rate.rate} @ {business.name} [{ex_rate.key}]")
						if exchanges_tree.get(exchange_code):
							exchanges_tree[exchange_code] += [exchange_rates[ex_rate.currency_key]]
						else:
							exchanges_tree[exchange_code] = [exchange_rates[ex_rate.currency_key]]
	logger.log(f"DEBUG: CUR_TEMPLA {len(exchanges_tree.keys())}")
	logger.log("Finished getting exchange rates")
	return exchanges_tree



