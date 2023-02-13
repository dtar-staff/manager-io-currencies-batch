import pickle
from config import CACHE_PATH, CACHE_EXT
import os
from hashlib import sha224
import logger

def clear_cache():
        logger.log("Started cache cleaning")
        cache_files = os.listdir(CACHE_PATH)
        for cache_file in cache_files:
                if os.path.isfile(CACHE_PATH + cache_file) and cache_file.endswith(CACHE_EXT):
                        logger.log(CACHE_PATH + cache_file)
                        os.remove(CACHE_PATH + cache_file)
        logger.log("Cache cleared.")

def obj_path(obj_hash):
	return CACHE_PATH + sha224(bytes(obj_hash, encoding='utf-8')).hexdigest() + CACHE_EXT

def new_cache_record(object, obj_hash):
	path = obj_path(obj_hash)
	if os.path.isfile(path):
		os.remove(path)
	with open(path, "wb") as f:
		pickle.dump(object, f)

def is_cached(obj_hash):
	path = obj_path(obj_hash)
	return os.path.isfile(path)

def get_from_cache(obj_hash):
	path = obj_path(obj_hash)
	if os.path.isfile(path):
		with open(path, "rb") as f:
			return pickle.load(f)
	else:
		return None
