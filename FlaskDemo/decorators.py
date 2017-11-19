import functools
from flask import session, redirect, url_for


# 登陆限制装饰器
def login_required(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if session.get('user_id'):
            return func(*args, **kwargs)
        else:
            return redirect(url_for('login'))
    return wrapper