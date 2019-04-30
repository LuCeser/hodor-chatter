from flask import *
from flask_restful import Api, Resource, reqparse
from wxpy import *

app = Flask(__name__)
api = Api(app)


bot = Bot(cache_path=True, console_qr=True)


@bot.register(Friend, TEXT)
def friend_msg_handler(msg):
    """
    处理好友消息
    :param msg:
    :return:
    """
    print(">>>>> 收到 {} : {}".format(msg.sender.name, msg.text))


# @bot.register(msg_types=FRIENDS)
# def auto_accept_friends(msg):
#     """
#     自动接受好友请求
#     :param msg:
#     :return:
#     """
#     new_friends = msg.card.accept()
#     new_friends.send('我们是同志了')


class NotificationApi(Resource):
    def post(self):
        req_json = request.get_json()
        print(">>>> 向群聊: {} 发送构建结果通知".format(req_json['groupName']))
        wx_group = bot.groups().search(req_json['groupName'])[0]
        send_msg = '服务: {0} 构建结果: {1}\r\n版本: {2}'\
            .format(req_json['serviceName'], req_json['buildResult'], req_json['version'])
        wx_group.send(send_msg)


api.add_resource(NotificationApi, '/wx/notify', endpoint='notify')

# @app.route('/wx/alter/<string:group_name>', methods=['POST'])
# def send_msg_to_group(group_name):
#     if not request.json:
#         print("没有请求信息")
#         abort(400)
#     return 'hi'
#
#
# @app.errorhandler(404)
# def not_found(error):
#     return make_response(jsonify({'error': 'not found'}), 404)


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
