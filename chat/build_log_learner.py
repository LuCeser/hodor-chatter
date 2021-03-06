import os
import pickle
import sys
import traceback
from configparser import ConfigParser

import pymysql

build_log = 'build_log.pkl'


class BuildLog(object):

    def __init__(self):
        cfg = self.read_config()
        self.db_url = cfg.get('db_info', 'db_url')
        self.db_name = cfg.get('db_info', 'db_name')
        self.db_username = cfg.get('db_info', 'db_username')
        self.db_password = cfg.get('db_info', 'db_password')
        self.db_name = cfg.get('db_info', 'db_name')

    @staticmethod
    def load_log(path):
        """
        记录日志
        :param path: 本地结果路径
        :return:
        """
        build_infos = []
        if os.path.exists(path):
            build_infos = pickle.load(open(build_log, 'rb'), encoding='utf-8')

        return build_infos

    def insert_build_log(self, log):
        """
        插入数据库
        :param log:
        :return:
        """
        db = pymysql.connect(self.db_url, port=3306, user=self.db_username, password=self.db_password, db=self.db_name)
        result = 1
        if not log['buildResult']:
            result = 0

        cursor = db.cursor()
        sql = """INSERT INTO `build_log` 
        (`build_time`, 
        `service_name`, 
        `last_commit_id`, 
        `image_name`, 
        `build_result`, 
        `author`, 
        `last_commit_log`, 
        `auto_test`, 
        `publish_environment`)
        VALUES 
        ('{}', '{}', '{}', '{}', {}, '{}', '{}', {}, '{}');
        """.format(log['buildTime'], log['serviceName'], log['lastCommit'], log['imageName'], result,
                   log.get('lastAuthor'), str(log['commitLog']), 0, '')

        try:
            cursor.execute(sql)
            db.commit()
            print("插入结果完成, 返回")
            return True
        except:
            print('插入数据失败')
            traceback.print_exc(file=sys.stdout)
            return False
        finally:
            db.close()

    @staticmethod
    def read_config():
        cfg = ConfigParser()
        cfg.read('config.ini')
        return cfg

