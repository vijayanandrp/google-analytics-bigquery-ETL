# -*- coding: utf-8 -*-
__author__ = "Vijay Anand RP"
__status__ = "Development"

import json
import os
import random
import string
from datetime import datetime, timedelta
import time


class TimeUtil(object):
    @staticmethod
    def wait_for_file(file_path=None, time_in_secs=60):
        flag = False
        if not file_path:
            print('Empty file path.')
            return False
        for second in range(time_in_secs):
            time.sleep(1)
            if not OsUtil.check_if_file_exist(file_name=file_path):
                continue
            else:
                flag = True
                break
        return flag

class DateUtil(object):

    @staticmethod
    def get_year_value(str_val=False):
        """ 2017 """
        date_stamp = datetime.now().strftime('%Y')
        print("Year Number: %s " % date_stamp)
        if str_val:
            return date_stamp.strip()
        return int(date_stamp)

    @staticmethod
    def get_month_value():
        """ 5 """
        date_stamp = datetime.now().strftime('%m')
        print("Month Number: %s " % date_stamp)
        return int(date_stamp)

    @staticmethod
    def get_week_number():
        """ 20 """
        date_stamp = datetime.now().strftime('%V')
        print("Week Number: %s " % date_stamp)
        return int(date_stamp)

    @staticmethod
    def get_date_time(fmt='%Y-%m-%d-%H-%M-%S'):
        """ 2017-05-19-04-20-38 """
        date_stamp = datetime.now().strftime(fmt)
        print("date_stamp_with_time: %s " % date_stamp)
        return date_stamp

    @staticmethod
    def get_date_time1(fmt='%Y-%m-%d-%H-%M-%S'):
        """ 2017-05-19-04-20-38 """
        date_stamp = datetime.now().strftime(fmt)
        print("date_stamp_with_time: %s " % date_stamp)
        return date_stamp.replace('-', '_')

    @staticmethod
    def get_date(fmt='%Y-%m-%d'):
        """ 2017-04-29 """
        date_stamp = datetime.now().strftime(fmt)
        print("date_stamp_date_only: %s " % date_stamp)
        return date_stamp

    @staticmethod
    def get_date2(fmt="%d%b%y"):
        """ 31Mar17 """
        date_stamp = datetime.now().strftime(fmt)
        print("date_stamp_date_only: %s " % date_stamp)
        return date_stamp

    @staticmethod
    def get_date3(fmt="%A %d %B %Y"):
        """ Friday 31. March 2017 """
        date_stamp = datetime.now().strftime(fmt)
        print("date_stamp_date_only: %s " % date_stamp)
        return date_stamp

    @staticmethod
    def get_date4(fmt="%A, %d. %B %Y %I:%M%p"):
        """ Tuesday, 21. November 2006 04:30PM """
        date_stamp = datetime.now().strftime(fmt)
        print("date_stamp_date_only: %s " % date_stamp)
        return date_stamp

    @staticmethod
    def get_time(fmt='%H-%M-%S'):
        date_stamp = datetime.now().strftime(fmt)
        print("date_stamp_time_only: %s " % date_stamp)
        return date_stamp

    @staticmethod
    def get_date_with_subtract(fmt='%Y-%m-%d', days_to_subtract=1):
        date_stamp = datetime.now() + timedelta(days=-days_to_subtract)
        date_stamp = date_stamp.strftime(fmt)
        print("date_stamp_with_days_subtraction: %s " % date_stamp)
        return date_stamp


class OsUtil(object):

    @staticmethod
    def root_directory(__file__=None):
        if not __file__:
            raise FileNotFoundError
        return os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

    @staticmethod
    def current_directory(__file__=None):
        if not __file__:
            raise FileNotFoundError
        return os.path.dirname(os.path.realpath(__file__))

    @staticmethod
    def join_path(source, value, create_dir=False):
        new_path = os.path.join(source, value)
        if create_dir:
            OsUtil.check_dir_and_create(new_path)
        return new_path

    @staticmethod
    def check_if_file_exist(file_name=None):
        if not file_name:
            print("file is empty")
            return False
        if os.path.isfile(file_name):
            print("file {} is found".format(file_name))
            return True
        else:
            print("file ({} not found".format(file_name))
            return False

    @staticmethod
    def check_if_path_exist(file_path=None):
        if not file_path:
            print("path value is empty")
            return False
        if os.path.isdir(file_path):
            print("path {} is found".format(file_path))
            return True
        else:
            print("path {} not found".format(file_path))
            return False

    @staticmethod
    def list_files_in_path(path=None):
        if not OsUtil.check_if_path_exist(file_path=path):
            return []
        for path, dirs, files in os.walk(path):
            return files

    @staticmethod
    def check_dir_and_create(path=None):
        if not path:
            print('Path cannot be None')
            return False
        if not os.path.isdir(path):
            os.makedirs(path)
            print('{} path not available. Creating it'.format(path))
            return True
        else:
            print('{} path already available'.format(path))
            return True


class RandomUtil(object):

    @staticmethod
    def random_string(length=6):
        return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))


class JsonUtil(object):
    @staticmethod
    def read(file_path=None):
        if not file_path:
            print('Json file path is empty.')
            return None
        if not OsUtil.check_if_file_exist(file_path):
            return None
        with open(file_path, 'r', encoding='utf-8') as fp:
            return json.load(fp)
