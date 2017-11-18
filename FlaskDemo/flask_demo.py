from flask import Flask, render_template, request, redirect, url_for, session
from FlaskDemo import config
import sys
from FlaskDemo.models import User

# sys.path.append('D:\PyCharmWorkSpace')
sys.path.append('/Users/tongxiaoyu/Documents/Work/Code/PythonDemos')
from FlaskDemo.exts import db

app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        phone = request.form.get('phone')
        password = request.form.get('password')
        user = User.query.filter(User.phone == phone).first()

        if user.verify_password(password):
            session['user_id'] = user.id
            session.permanent = True
            return redirect(url_for('index'))
        else:
            return u'wrong!'


@app.route('/registe', methods=['GET', 'POST'])
def registe():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        phone = request.form.get('phone')
        name = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        if User.query.filter(User.phone == phone).first():
            return u'has registed, try another!'
        else:
            if password1 != password2:
                return u'not samed password'
            else:
                user = User(phone=phone, user=name, password=password1)
                db.session.add(user)
                db.session.commit()

                return redirect(url_for('login'))


@app.route('/logout')
def logout():
    session.pop('user_id')
    # del session['user_id']
    # 删除所有
    # session.clear()
    return redirect(url_for('index'))


@app.context_processor
def my_context_processor():
    user_id = session.get('user_id', None)
    if user_id:
        user = User.query.filter(User.id == user_id).first()
        if user:
            return {'user': user}
    # context 钩子函数即使无结果也要返回空字典
    return {}


@app.route('/question')
def question():
    if request.method == 'GET':
        return render_template('question.html')
    else:
        pass


if __name__ == '__main__':
    app.run()