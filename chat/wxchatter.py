import os

from flask import *
from flask_restful import Api, Resource
from wxpy import *
import pickle

app = Flask(__name__)
api = Api(app)


bot = Bot(cache_path=True, console_qr=True)

principal_file = 'principal.pkl'
build_log = 'build_log.pkl'


# @bot.register(Friend, TEXT)
# def friend_msg_handler(msg):
#     """
#     处理好友消息
#     :param msg:
#     :return:
#     """
#     print(">>>>> 收到 {} : {}".format(msg.sender.name, msg.text))


class BuildInfoApi(Resource):
    """
    记录构建结果
    """
    def post(self):
        """
    {
    "buildTime":"2019-04-12 19:22:30",
    "serviceName":"roster-service",
    "lastCommit":"9da3dk91bdk834q",
    "commitLog":"feat: 增加新功能",
    "imageName":"roster-service:191",
    "buildResult":true,
    "lastAuthor":"paul"
    }
    """
        req_json = request.get_json()
        print(">>> 服务: {} 构建结果: {}".format(req_json['serviceName'], req_json['buildResult']))
        self.persistance_log(req_json)
        if req_json['buildResult']:
            self.notify_build_success(req_json)
        else:
            self.notify_build_failure(req_json)

    @staticmethod
    def persistance_log(build_info):
        """
        记录日志
        :param build_info:
        :return:
        """
        build_infos = []
        if os.path.exists(build_log):
            build_infos = pickle.load(open(build_log, 'rb'), encoding='utf-8')

        build_infos.append(build_info)
        pickle.dump(build_infos, open(build_log, 'wb'))

    def notify_build_success(self, build_info):
        """
        通知群组构建成功
        :return:
        """
        principal_dict = pickle.load(open(principal_file, 'rb'), encoding='utf-8')
        group_name = principal_dict.get("groups").get(build_info['serviceName'])
        print(">>> 通知群组 {} 服务 {} 构建成功".format(group_name, build_info['serviceName']))
        send_msg = '服务: {0} \r\n构建时间: {1}\r\n镜像名: {2}\r\n提交信息: {3}'\
            .format(build_info['serviceName'], build_info['buildTime'], build_info['imageName'], build_info['commitLog'])
        self.notify_wx_group(group_name, send_msg)

    def notify_build_failure(self, build_info):
        """
        通知服务负责人构建失败
        :param build_info:
        :return:
        """
        principal_dict = pickle.load(open(principal_file, 'rb'), encoding='utf-8')
        friends_name = principal_dict.get("friends").get(build_info['serviceName'])
        print(">>> 通知 服务 {} 负责人 {} 构建失败".format(build_info['serviceName'], friends_name))
        send_msg = '服务: {0} \r\n构建时间: {1}\r\n镜像名: {2}\r\n提交信息: {3}' \
            .format(build_info['serviceName'], build_info['buildTime'], build_info['imageName'], build_info['commitLog'])
        self.notify_wx_friend(friends_name, send_msg)

    @staticmethod
    def notify_wx_group(group_name, msg):
        print("<<< {}".format(msg))
        wx_groups = bot.groups(update=True).search(group_name)
        if wx_groups:
            wx_groups[0].send(msg)
        else:
            print("找不到群聊 {}".format(group_name))

    @staticmethod
    def notify_wx_friend(friend, msg):
        print("<<< {}".format(msg))
        wx_friends = bot.friends().search(friend)
        for friend in wx_friends:
            friend.send(msg)


# 记录构建信息，并发送通知到服务负责人或测试人员
api.add_resource(BuildInfoApi, '/wx/info', endpoint='cd')


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
