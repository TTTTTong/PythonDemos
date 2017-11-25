from threading import Thread
from flask_mail import Message, Mail


def send_email(app, **kwargs):
    msg = Message(app.config['FLASKY_MAIL_SUBJECT_PREFIX']+' NewUser', sender=app.config['MAIL_USERNAME'],
                  recipients=[app.config['MAIL_SEND_TO']])
    # msg.body = render_template(template+'.txt', **kwargs)
    # msg.html = render_template(template+'.html', **kwargs)
    msg.body = 'testing'
    msg.html = '<b>testing</b>'

    thread = Thread(target=send_async_email, args=[app, msg])
    thread.start()


def send_async_email(app, msg):
    with app.app_context():
        mail = Mail(app)
        mail.send(msg)