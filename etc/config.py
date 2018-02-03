# -*- coding: utf-8 -*-
# strictly no functions
__author__ = "Vijay Anand RP"

import configparser
from lib.util import OsUtil, JsonUtil

config = configparser.ConfigParser()
config_file = OsUtil.join_path(OsUtil.current_directory(__file__), 'config.ini')
config.read(config_file)

if not OsUtil.check_if_file_exist(config_file):
    print(config_file)
    raise FileNotFoundError

# [ PROJECT NAME ]
project_name = config['project_settings']['project_name']


# [ DIRECTORY CONFIGURATIONS ]
# get root directory
path_root = OsUtil.root_directory(__file__)
# data path
path_data = OsUtil.join_path(path_root, config['path_settings']['data'], create_dir=True)
# Config path
path_etc = OsUtil.join_path(path_root, config['path_settings']['etc'], create_dir=True)
# Logs path
path_log = OsUtil.join_path(path_data, config['path_settings']['logs'], create_dir=True)

file_log = config['log_settings']['file_log']

# [ CLOUD CONFIGURATIONS ]
json_credential = config['cloud_settings']['json_credential']
json_credential = OsUtil.join_path(path_etc, json_credential)
credential = JsonUtil.read(file_path=json_credential)
if not credential:
    raise FileNotFoundError

# download format
file_format = config['cloud_settings']['file_format']
