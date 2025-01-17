from configparser import ConfigParser
import os

config = ConfigParser()
config.read("./config.ini")

class ConfigKey():
	def __init__(self) -> None:
		self.hf_key = config["KEY"]["openai_key"]
