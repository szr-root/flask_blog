import hashlib

from flask import Blueprint, render_template, request, redirect, url_for, jsonify, session
from werkzeug.security import generate_password_hash, check_password_hash

from apps.user.model import User
from apps.user.smssend import SmsSendAPIDemo
from ext import db

user_bp = Blueprint('user', __name__, url_prefix='/user')


@user_bp.route('/')
def index():
    # 1。 cookie获取方式
    # uid = request.cookies.get('uid', None)

    # 2.session获取,session底层默认拿取传递值
    uid = session.get('uid')
    if uid:
        user = User.query.get(uid)
        return render_template('user/index.html', user=user)
    else:
        return render_template('user/index.html')


@user_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        repassword = request.form.get('repassword')
        phone = request.form.get('phone')
        email = request.form.get('email')
        if password == repassword:
            user = User()
            user.username = username
            user.password = generate_password_hash(password)
            user.phone = phone
            user.email = email
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('user.index'))
    else:
        return render_template('user/register.html')


@user_bp.route('/checkphone', methods=['GET', 'POST'])
def check_phone():
    phone = request.args.get('phone')
    print(phone)
    user = User.query.filter(User.phone == phone).all()
    print(user)
    # code:400 不能用   200 :可以用
    if len(user) > 0:
        return jsonify(code=400, msg='此号码已被注册')
    else:
        return jsonify(code=200, msg='此号码可用')


@user_bp.route('/login', methods=['GET', 'POST'])
def login():
    f = request.args.get('f')
    if f == 1: #用户名密码登录
        if request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')
            users = User.query.filter(User.username == username).all()
            for user in users:
                flag = check_password_hash(user.password, password)
                if flag:
                    # # 1设置cookie
                    # response = redirect(url_for('user.index'))
                    # response.set_cookie('uid', str(user.id), max_age=1800)
                    # return response

                    # 2。session
                    session['uid'] = user.id
                    return redirect(url_for('user.index'))
            else:
                return render_template('user/login.html', msg='用户名或者密码有误!')
        return render_template('user/login.html')
    elif f == 2:
        pass


@user_bp.route('sendMsg')
def send_message():
    phone = request.args.get('phone')
    SECRET_ID = "a9fb91f3c983848c2107816212bf38b2"  # 产品密钥ID，产品标识
    SECRET_KEY = "2488a6dda29f945314a65798d20fdf29"  # 产品私有密钥，服务端生成签名信息使用，请严格保管，避免泄露
    BUSINESS_ID = "36099b3a8f2b4188b6b1a7cf0e9deadd"  # 业务ID，易盾根据产品业务特点分配
    api = SmsSendAPIDemo(SECRET_ID, SECRET_KEY, BUSINESS_ID)
    params = {
        "mobile": phone,
        "templateId": "10084",
        "paramType": "json",
        "params": "json格式字符串"
        # 国际短信对应的国际编码(非国际短信接入请注释掉该行代码)
        # "internationalCode": "对应的国家编码"
    }
    ret = api.send(params)
    if ret is not None:
        if ret["code"] == 200:
            taskId = ret["data"]["taskId"]
            print("taskId = %s" % taskId)
        else:
            print("ERROR: ret.code=%s,msg=%s" % (ret['code'], ret['msg']))


@user_bp.route('/logout')
def logout():
    # cookie删除
    # response = redirect(url_for('user.index'))
    # response.delete_cookie('uid')

    # 2。session退出
    # del session['uid']  # 不会删除session空间
    session.clear()  # 删除所有
    return redirect(url_for('user.index'))
