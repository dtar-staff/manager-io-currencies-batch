
NULL_KEY=""

class NullObject:
        def __init__(self):
            self.key = NULL_KEY

NULL_OBJECT = NullObject()

class AbstractRoot:
	def __init__(self, key: str, parent_object=NULL_OBJECT):
		self.key = key
		self.parent = parent_object

	def set_parent(self, parent_object=NULL_OBJECT):
		self.parent = parent_object
