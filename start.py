import requests
import json
import time
import random
import hashlib
import sys
import os

s = requests.Session()
header = {"Accept-Encoding": "gzip, deflate, br",
                "Accept-Language": "zh-cn",
                "Connection": "keep-alive",
                "Content-Length": "0",
                "Host": "api-takumi.mihoyo.com",
                "Referer": "https://app.mihoyo.com",
                'User-Agent': 'Hyperion/67 CFNetwork/1128.0.1 Darwin/19.6.0',
                "x-rpc-app_version": "2.2.0",
                "x-rpc-channel": "appstore",
                "x-rpc-client_type": "1",
                "x-rpc-device_id": "".join(random.sample('abcdefghijklmnopqrstuvwxyz0123456789', 32)).upper(),
                "x-rpc-device_model": "iPhone11,8",
                "x-rpc-device_name": "".join(random.sample('abcdefghijklmnopqrstuvwxyz0123456789', random.randrange(5))).upper(),
                "x-rpc-sys_version": "14.0.1",}
result_status = None

## 日志
def get_file_path(file_name=""):
    """
    获取文件绝对路径, 防止在某些情况下报错
    :param file_name: 文件名
    :return:
    """
    return os.path.join(os.path.split(sys.argv[0])[0], file_name)

def to_log(info_type="", title="", info=""):
    """
    :param info_type: 日志的等级
    :param title: 日志的标题
    :param info: 日志的信息
    :return:
    """
    if not os.path.exists(get_file_path("logs")):
        os.mkdir(get_file_path("logs/"))
    now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    log = now + "  " + info_type + "  " + title + "  " + info
    with open(get_file_path("logs/mhytool.log"), "a", encoding="utf-8") as log_a_file_io:
        log_a_file_io.write(log + "\n")
    return log


## 生成DS
def get_DS():
    """
    IOS sign
    """
    ## DS 加密算法: 
    ## Ref: 1. https://github.com/lhllhx/miyoubi/issues/3
    #       2. https://github.com/jianggaocheng/mihoyo-signin/blob/master/lib/mihoyoClient.js
    t = int(time.time())
    a = "".join(random.sample('abcdefghijklmnopqrstuvwxyz0123456789', 6))
    re = hashlib.md5(f"salt=b253c83ab2609b1b600eddfe974df47b&t={t}&r={a}".encode(encoding="utf-8")).hexdigest()
    return f"{t},{a},{re}"


## 签到：
def miyoushe_signin(module_id):
    """
    docstring
    """
    global header
    global result_status

    header["DS"] = get_DS()

    ## 1: 崩坏3, 2: 原神, 3: 崩坏学园2, 4: 未定事件簿, 5: 崩坏：星穹铁道
    sign_data = {'gids': module_id} 
    url_signin = 'https://api-takumi.mihoyo.com/apihub/sapi/signIn'
    try:
        res_signin = s.post(url_signin, json=sign_data, headers=header, timeout=net_timeout)
    except:
        print(to_log("ERROR", "服务器连接失败。"))
        result_status = "error"
        return "error"
    result = json.loads(res_signin.text)
    if result["message"] == "OK":
            if "data" in result:
                if "points" in result["data"]:
                    print(to_log("INFO", "签到成功，获得 " + str(result["data"]["points"]) + " 米游币。"))
            else:
                print(to_log("INFO", "签到成功。"))
    elif result["message"] == "签到失败或重复签到":
        print(to_log("WARN", "签到失败或重复签到。"))
    else:
        print(to_log("ERROR", "签到出错!"))
        result_status = "error"


## 帖子相关：阅读，点赞，分享
def miyoushe_forumPost(fid):
    """
    1, 26, 30, 37, 52
    """
    global header
    global result_status

    URL = "https://api-takumi.mihoyo.com/post/api/getForumPostList?forum_id={}&is_good=false&is_hot=false&page_size=20&sort=create".format(fid)
    try:
        res = s.get(URL, headers=header, timeout=net_timeout)
    except:
        print(to_log("ERROR", "服务器连接失败。"))
        result_status = "error"
        return "error"
    res_text = json.loads(res.text)

    URL_upvote = 'https://api-takumi.mihoyo.com/apihub/sapi/upvotePost'
    URL_read = 'https://api-takumi.mihoyo.com/post/api/getPostFull?post_id='

    

    count = 0
    while count < 3:
        post_id = res_text['data']['list'][count]['post']['post_id']
        
        ## 阅读
        time.sleep(random.uniform(timesleep_1, timesleep_2))

        header["DS"] = get_DS()
        URL_read_id = URL_read + post_id
        try:
            res_read = s.get(URL_read_id,headers=header, timeout=net_timeout)
        except:
            print(to_log("ERROR", "服务器连接失败。"))
            result_status = "error"
            return "error"

        result = json.loads(res_read.text)
        if result["message"] == "OK":
            print(to_log("INFO", "帖子ID：" + post_id + " —— 阅读成功。"))
        else:
            print(to_log("ERROR", "帖子ID：" + post_id + " —— 阅读失败！"))
            result_status = "error"

        time.sleep(random.uniform(timesleep_1, timesleep_2))
            
        count += 1
    
    count = 0
    it = iter(res_text['data']['list'])
    while count < 10:
        ## 判断是否已经点赞
        while True:
            # 若帖子列表中所有帖子都已经点赞，则重新获取列表
            try:
                like_status = next(it)
                if like_status['self_operation']['attitude'] != 0:
                    print(to_log("INFO","帖子ID: " + like_status['post']['post_id'] + " —— 已经点赞过了。"))
                else:
                    break
            except StopIteration:
                print(to_log("INFO","帖子列表中所有帖子都已经点赞，正在获取新的列表。"))
                try:
                    res = s.get(URL, headers=header, timeout=net_timeout)
                except:
                    print(to_log("ERROR", "服务器连接失败。"))
                    result_status = "error"
                    return "error"
                it = iter(res_text['data']['list'])

        post_id = like_status['post']['post_id']
        
        ## 点赞
        upvote_data = {'is_cancel':False,  'post_id':post_id}
        try:
            res_vote = s.post(URL_upvote, json=upvote_data, headers=header, timeout=net_timeout)
        except:
            print(to_log("ERROR", "服务器连接失败。"))
            result_status = "error"
            return "error"

        result = json.loads(res_vote.text)
        if result['message'] == 'OK':
            print(to_log("INFO", "帖子ID：" + post_id + " —— 点赞成功。"))
        else:
            print(to_log("ERROR", "帖子ID：" + post_id + " —— 点赞失败！"))
            result_status = "error"
        
        if count != 9:
            time.sleep(random.uniform(timesleep_1, timesleep_2))
        
        count += 1
    
    ## 分享最后一帖
    sharePost(post_id)

    print(to_log("INFO", "帖子相关操作结束。"))


## 分享：
def sharePost(post_id):
    global header
    global result_status

    header["DS"] = get_DS()
    URL_post_share = "https://api-takumi.mihoyo.com/apihub/api/getShareConf?entity_id={}&entity_type=1".format(post_id)
    try:
        res_share = s.get(URL_post_share, headers=header, timeout=net_timeout)
    except:
        print(to_log("ERROR", "服务器连接失败。"))
        result_status = "error"
        return "error"
    result = json.loads(res_share.text)
    if result['message'] == 'OK':
        print(to_log("INFO", "帖子ID：" + post_id + " —— 转发成功。"))
    else:
        print(to_log("ERROR", "帖子ID：" + post_id + " —— 转发失败！"))
        result_status = "error"



def start(userdata, setting):

    global header
    global timesleep_1
    global timesleep_2
    global net_timeout
    global result_status

    result_status = None

    stuid = userdata["uid"]
    stoken = userdata["stoken"]
    id = userdata["id"]
    if stuid == '' or None:
        print(to_log("ERROR", "请设置用户Cookies数据！"))
        return "error"
    elif stoken == '' or None:
        print(to_log("ERROR", "请设置用户Cookies数据！"))
        return "error"
    
    module_id = setting["module_id"]
    if module_id == '' or None:
        print(to_log("ERROR", "请设置游戏板块module_id的值！"))
        return "error"
    
    print(to_log("INFO", "用户 uid_{0} - {1}：任务开始。".format(id, stuid)))

    fid_list = {
        '1': '1',
        '2': '26',
        '3': '30',
        '4': '37',
        '5': '52'
    }

    ### 冷却时间范围 (timesleep_1 ~ timesleep_2)
    timesleep_1 = setting["t1"]
    timesleep_2 = setting["t2"]

    if timesleep_1 == '' or None:
        timesleep_1 = 2
        if timesleep_2 == '' or None:
            timesleep_2 = 4
    
    timesleep_1 = float(timesleep_1)
    timesleep_2 = float(timesleep_2)

    net_timeout = setting["timeout"]

    if net_timeout == '' or None:
        net_timeout = 10

    net_timeout = float(net_timeout)

    header["Cookie"] = 'stuid={0};stoken={1};'.format(stuid, stoken)

    ## 签到
    module_id = int(module_id)
    miyoushe_signin(module_id)

    ## 帖子相关：阅读，点赞，分享
    fid = int(fid_list[str(module_id)])
    miyoushe_forumPost(fid)

    print(to_log("INFO", "用户 uid_{0} - {1}：任务结束。".format(id, stuid)))
    if result_status == "error":
        return "error"
    else:
        return "success"
