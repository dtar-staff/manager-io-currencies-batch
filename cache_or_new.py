from cache import *
from cache_keys import *
from get_currencies_template import *

def fb():
        if is_cached(fb_key):
                foreign_businesses = get_from_cache(fb_key)
                logger.log("FB from cache")
        else:
                foreign_businesses = get_businesses_with_foreign_currencies()
                new_cache_record(foreign_businesses, fb_key)
        return foreign_businesses

def fbb(foreign_businesses):
        if is_cached(fbb_key):
                fb_ordered_by_base_currency = get_from_cache(fbb_key)
                logger.log("FBB from cache")
        else:
                fb_ordered_by_base_currency = get_businesses_ordered_by_base_currency(foreign_businesses)
                new_cache_record(fb_ordered_by_base_currency, fbb_key)
        return fb_ordered_by_base_currency

def ct(fb_ordered_by_base_currency):
        if is_cached(ct_key):
                logger.log("CT from cache")
                currencies_tree = get_from_cache(ct_key)
        else:
                currencies_tree = get_currency_codes_list_by_base(fb_ordered_by_base_currency)
                new_cache_record(currencies_tree, ct_key)
        return currencies_tree

def fcu(business):
        fcu_full_key = fcu_key + business.key
        if is_cached(fcu_full_key):
                logger.log(f"FCU from cache [{business.name}]")
                f_currencies = get_from_cache(fcu_full_key)
        else:
                f_currencies = manager.get_foreign_currencies(business)
                new_cache_record(f_currencies, fcu_full_key)
        return f_currencies

def xtr(fb_ordered_by_base_currency, date):
#        if is_cached(xtr_key):
#                logger.log("XTR from cache")
#                exchanges_tree = get_from_cache(xtr_key)
#        else:
#                exchanges_tree = get_exchanges_tree_by_date(fb_ordered_by_base_currency, date)
#                new_cache_record(exchanges_tree, xtr_key)
        exchanges_tree = get_exchanges_tree_by_date(fb_ordered_by_base_currency, date)
#        new_cache_record(exchanges_tree, xtr_key)
        return exchanges_tree
