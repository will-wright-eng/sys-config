"""Tests for hello function."""
import pytest

from sys_config.sys_config import ConfigHandler

config_handler = ConfigHandler(project_name='test')

def test_config_handler():
	"""test config handler"""
	assert config_handler.check_exists()  == "config file does not exist -- run configure endpoint"

def test_config_input():
	"""test config input"""
	config = {'ServerAliveInterval'.lower(): '45',
	              'Compression'.lower(): 'yes',
	              'CompressionLevel'.lower(): '8',}
	config_handler.config_file_input(config_dict=config)
	for l,r in zip(config_handler.get_configs().items(),config.items()):
		assert l == r
