from flask import (
    Blueprint,
    redirect,
    render_template,
    request,
    url_for,
    flash,
    current_app,
    send_file
)
from flask_login import login_user, login_required, current_user, UserMixin
from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired, FileAllowed
from wtforms import FileField, StringField, PasswordField
from wtforms.validators import DataRequired
from .cevidblib.master import Master
from .cevidblib.config import Settings
import os
import datetime
import requests
import json


bp = Blueprint('main', __name__)

class FileForm(FlaskForm):
    """ main form """
    #user_ = StringField("User", validators=[DataRequired()])
    #pass_ = PasswordField("Pass", validators=[DataRequired()])
    file_ = FileField("Datei", validators=[FileRequired(), FileAllowed(['xlsx'], "Nur XLSX Dateien erlaubt")])


class User(UserMixin):
    pass

@bp.route('/login')
def oauth_login():
    provider = current_app.config["OAUTH"]["provider"]
    c_id = current_app.config["OAUTH"]["id"]
    c_secret = current_app.config["OAUTH"]["secret"]
    callback = url_for("main.handle_callback", _external=True)
    current_app.logger.debug(callback)
    return redirect(f"https://{provider}/oauth/authorize?response_type=code&client_id={c_id}&redirect_uri={callback}&scope=email")

@bp.route('/oauth') #, methods=('GET', 'POST'))
def handle_callback():
    provider = current_app.config["OAUTH"]["provider"]
    c_id = current_app.config["OAUTH"]["id"]
    c_secret = current_app.config["OAUTH"]["secret"]
    callback = url_for("main.handle_callback", _external=True)

    current_app.logger.debug("in callback")
    token_headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    code = request.args.get("code")
    token_data = "&".join([
        'grant_type=authorization_code',
        f'client_id={c_id}',
        f'client_secret={c_secret}',
        f'redirect_uri={callback}',
        f'code={code}',
        ])
    res_token = requests.post(f'https://{provider}/oauth/token', headers=token_headers, data=token_data)
    token = res_token.json()['access_token']
    current_app.logger.debug("token: %s", token)

    mail_headers = {
        'Authorization': f"Bearer {token}",
        'X-Scope': "email",
    }
    res_mail = requests.get(f'https://{provider}/oauth/profile', headers=mail_headers)
    res_mail.raise_for_status()

    user = User()
    user.id = res_mail.json()['email']
    current_app.logger.debug("user id: %s", user.id)
    if user.id in current_app.config["USER"]:
        login_user(user)
        current_app.logger.debug("logged in, redirecting")
        return redirect(url_for('main.index'))
    current_app.logger.warning("login failed")
    return render_template('main/denied.html', user=user.id), 403


@bp.route('/', methods=('GET', 'POST'))
@login_required
def index():
    form = FileForm()
    if form.validate_on_submit():
        current_app.logger.debug("form submission valid")
        user_ = current_user.id
        if user_ in current_app.config["USER"]:
            current_app.logger.debug("user ok")
            file_ = form.file_.data
            filename = f"{user_}.xlsx"
            fullname = os.path.join(current_app.config["TMP_PATH"], filename)
            file_.save(fullname)
            try:
                master = Master(settings=Settings(current_app.config["USER"][user_]))
                master.run(fullname, cert=None, backup=False)
                return send_file(fullname, as_attachment=True, download_name=filename)
            except Exception as e:
                flash("Error: "+str(e.args), "danger")
            return redirect(url_for('main.index'))
    else:
        current_app.logger.error("invalid from submission")
    return render_template('main/page.html', form=form)

@bp.route('/cleanup')
def cleanup():
    """ cleanup old datafiles

    let this be run automatically using cron or systemd timer
    """
    ref_time = datetime.datetime.now() - datetime.timedelta(minutes=2)
    for file_ in os.listdir(current_app.config["TMP_PATH"]):
        fullfile = os.path.join(current_app.config["TMP_PATH"], file_)
        if datetime.datetime.fromtimestamp(os.path.getctime(fullfile)) < ref_time:
            os.remove(fullfile)

    return "OK"

#TODO:
#  - propper layout/css

