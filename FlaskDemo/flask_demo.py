from flask import render_template, request, redirect, url_for, session, g, flash
from flask_login import login_required, login_user, logout_user
from sqlalchemy import or_
import sys
from FlaskDemo import create_app, login_manager
from FlaskDemo.models import User, Question, Comment
sys.path.append('/Users/tongxiaoyu/Documents/Work/Code/PythonDemos')
from FlaskDemo.exts import db

app = create_app()


@app.route('/')
def index():
    content = {
        'questions': Question.query.order_by('-create_time').all()
    }
    return render_template('index.html', **content)


@app.before_request
def before_qequest():
    user_id = session.get('user_id')
    if user_id:
        user = User.query.filter(User.id == user_id).first()
        if user:
            g.user = user


@app.context_processor
def my_context_processor():
    if hasattr(g, 'user'):
            return {'user': g.user}
    # context 钩子函数即使无结果也要返回空字典
    return {}


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


'''
视图函数
'''


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        phone = request.form.get('phone')
        password = request.form.get('password')
        user = User.query.filter(User.phone == phone).first()

        if user and user.verify_password(password):
            # send_email(app)

            login_user(user)
            return redirect(url_for('index'))
        else:
            flash('The username or password is wrong')
            return redirect(url_for('login'))


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
                flash('The username or password is wrong')
                return u'not samed password'
            else:
                user = User(phone=phone, user=name, password=password1)
                db.session.add(user)
                db.session.commit()

                return redirect(url_for('login'))


@app.route('/logout')
def logout():
    # session.pop('user_id')
    # del session['user_id']
    # 删除所有
    # session.clear()
    logout_user()
    return redirect(url_for('index'))


@app.route('/question', methods=['GET', 'POST'])
@login_required
def question():
    if request.method == 'GET':
        return render_template('question.html')
    else:
        title = request.form.get('title')
        content = request.form.get('content')
        newquestion = Question(title=title, content=content)

        # user_id = session.get('user_id')
        # user = User.query.filter(User.id == user_id).first()
        newquestion.author = g.user

        db.session.add(newquestion)
        db.session.commit()
        return redirect(url_for('index'))


@app.route('/detail/<question_id>')
def detail(question_id):
    question_model = Question.query.filter(Question.id == question_id).first()
    return render_template('detail.html', question=question_model)


@app.route('/add_comment', methods=['POST'])
@login_required
def add_comment():
    content = request.form.get('comment')
    question_id = request.form.get('question_id')

    # author_id = session.get('user_id')
    # user = User.query.filter(User.id == author_id).first()
    question_model = Question.query.filter(Question.id == question_id).first()

    comment = Comment(content=content, author=g.user, question=question_model)

    db.session.add(comment)
    db.session.commit()
    return redirect(url_for('detail', question_id=question_id))


@app.route('/search')
def search():
    q = request.args.get('q')
    # 或
    questions = Question.query.filter(or_(Question.title.contains(q),
                                          Question.content.contains(q))).order_by('-create_time')
    # 与
    # questions = Question.query.filter(Question.title.contains(q),
    #                                       Question.content.contains(q)).order_by('-create_time')
    return render_template('index.html', questions=questions)


if __name__ == '__main__':
    app.run()