import itchat


# 调用接口或者方法获取返回值
def get_response(msg):
    userInfo = itchat.search_friends(userName=msg.fromUserName)
    reply = "请问您注册的邮箱是什么？"
    print("<<<< {0} : {1}".format(msg['User']['NickName'], reply))
    return reply


def get_user_info(user_id):
    '''
    根据wechat userid获取本地用户配置
    :param user_id:
    :return:
    '''
    pass


@itchat.msg_register(itchat.content.TEXT)
def print_content(msg):
    print(">>>> {0} : {1}".format(msg['User']['NickName'], msg['Text']))

    reply = get_response(msg)
    defaultReply = "收到，稍后给您回复"
    return reply or defaultReply


# 开启暂存登陆状态
itchat.auto_login(hotReload=True)
itchat.run()
