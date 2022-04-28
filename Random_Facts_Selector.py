import json
import os
import random
import textwrap
########################################################################
class Random_Fact(object):
	""""""
	#----------------------------------------------------------------------
	def __init__(self,category,subject,fact):
		"""Constructor"""
		self.category=category
		self.subject = subject
		self.fact = fact
	#----------------------------------------------------------------------
	def print_out(self):
		""""""
		print("Category:{} Subject:{}".format(self.category,self.subject))
		print("Fact:\n{}".format("\n".join(textwrap.wrap(self.fact, width=80,replace_whitespace=False)) ))

########################################################################
class Random_Data_Selector(object):
	""""""
	#----------------------------------------------------------------------
	def __init__(self,data,label=None):
		"""Constructor"""
		self.passed_selected_keys = []
		self.data  = data
		self.lable = label
		if isinstance(self.data,list):
			self.data_type = "l"
		elif isinstance(self.data,dict):
			self.data_type = "d"
		else:
			raise ValueError("data input must be a list or dict and a {} was found").format(type(data))

	#----------------------------------------------------------------------
	def __len__(self):
		""""""
		return len(self.data)

	#----------------------------------------------------------------------
	def get_Random_Key(self):
		""""""
		if len(self.passed_selected_keys) == len(self):
			self.passed_selected_keys = []

		rand_key = random.randint(0, len(self)-1 )

		while rand_key in self.passed_selected_keys:

			rand_key = random.randint(0, len(self)-1 )

		self.passed_selected_keys.append(rand_key)

		if self.data_type == "l":
			return rand_key
		else:
			return list(self.data.keys())[rand_key]

		return rand_key
	#----------------------------------------------------------------------
	def get_Random_Data(self):
		""""""
		key  = self.get_Random_Key()
		data = self.data[key]
		if isinstance(data,list) or isinstance(data,dict):
			data = Random_Data_Selector(data,label=key)
		return data

########################################################################
class Random_Facts_Selector(Random_Data_Selector):
	""""""
	#----------------------------------------------------------------------
	def __init__(self):
		"""Constructor"""
		json_file = os.path.join(os.path.dirname(__file__),"Data/random_facts.json")
		with open(json_file,"r") as fp:
			data = json.load(fp)
			super(Random_Facts_Selector,self).__init__(data)
	#----------------------------------------------------------------------
	def get_Random_Fact(self):
		""""""
		category = self.get_Random_Data()
		subject = category.get_Random_Data()
		fact    = subject.get_Random_Data()
		return Random_Fact(category.lable, subject.lable, fact)
