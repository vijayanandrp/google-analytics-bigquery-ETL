# -*- coding: utf-8 -*-
__author__ = "Vijay Anand RP"
__status__ = "Development"

import logging
from etc.config import path_log, file_log
from lib.util import OsUtil, DateUtil, RandomUtil


class Logger(object):
    """ module for logging the executions and statements """
    def __init__(self, file_name=None, level='INFO', stream_output=False):
        if not file_name:
            file_name = file_log
        self.file_log = '{}_{}_{}.log'.format(DateUtil.get_date_time1('%Y%m%d%H%M%S'), file_name,
                                              RandomUtil.random_string())
        self.file_log = OsUtil.join_path(path_log, self.file_log)
        self.level_debug = level
        self.stream_output = stream_output

    def defaults(self, name_class=None):
        """ default configuration settings in the method """
        if not name_class:
            print('** Enter the class or function name **')
            raise NameError

        if self.level_debug is "INFO":
            level_debug = logging.INFO
        elif self.level_debug is "DEBUG":
            level_debug = logging.DEBUG
        else:
            level_debug = logging.INFO

        # log file configuration
        logging.basicConfig(level=level_debug,
                            filename=self.file_log,
                            filemode='a',
                            format='[%(asctime)s] - %(name)s - %(levelname)s - %(message)s',
                            datefmt='%d-%b-%y %I:%M%p')

        # console output
        if type(self.stream_output) is bool and self.stream_output:
            console = logging.StreamHandler()
            console.setLevel(level_debug)
            console.setFormatter(logging.Formatter('%(name)s - %(levelname)s - %(message)s'))
            logging.getLogger('').addHandler(console)

        return logging.getLogger("{}".format(name_class))



