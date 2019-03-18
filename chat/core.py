import itchat
import pickle

user_data_file = "user_data.pkl"


def init_user_dict():
    user_info = dict()
    with open(user_data_file, 'wb') as f:
        pickle.dump(user_info, f)


# 调用接口或者方法获取返回值
def get_response(msg):
    user = get_user_info(msg.fromUserName)
    reply = "请问您注册的邮箱是什么？"
    print("<<<< {0} : {1}".format(msg['User']['NickName'], reply))
    return reply


def get_user_info(user_id):
    '''
    根据wechat userid获取本地用户配置
    :param user_id:
    :return:
    '''
    print("获取用户%s信息" % (user_id))
    user_info = dict()
    try:
        with open(user_data_file, 'rb') as f:
            user_info = pickle.load(f)
            print(user_info)
    except FileNotFoundError:
        print("用户信息不存在")
        init_user_dict()
    except PermissionError:
        print("无法读取用户权限信息")

    if user_info.get(user_id):
        print("用户已存在")
    else:
        print("当前客户 {0} 未注册".format(user_id))
        add_user_info(user_id)

    return ""


def add_user_info(user_info):
    '''
    添加用户信息
    :param user_id:
    :return:
    '''
    with open(user_data_file, 'wb') as f:
        f.write(user_info)


@itchat.msg_register(itchat.content.TEXT)
def text_handler(msg):
    print(">>>> {0} : {1}".format(msg['User']['NickName'], msg['Text']))

    reply = get_response(msg)
    default_reply = "收到，稍后给您回复"
    return reply or default_reply


@itchat.msg_register(itchat.content.VOICE)
def voice_handler(msg):
    pass


@itchat.msg_register(itchat.content.PICTURE)
def picture_handler(msg):
    default_reply = "对不起，我现在还看不懂图片哦"
    return default_reply


# 开启暂存登陆状态
itchat.auto_login(hotReload=True)
itchat.run()
