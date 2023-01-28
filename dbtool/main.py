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
#from flask_login import login_required, current_user
from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired, FileAllowed
from wtforms import FileField, StringField, PasswordField
from wtforms.validators import DataRequired
from .cevidblib.master import Master
from .cevidblib.config import Settings
import os
import datetime

bp = Blueprint('main', __name__)

class FileForm(FlaskForm):
    """ main form """
    user_ = StringField("User", validators=[DataRequired()])
    pass_ = PasswordField("Pass", validators=[DataRequired()])
    file_ = FileField("Datei", validators=[FileRequired(), FileAllowed(['xlsx'], "Nur XLSX Dateien erlaubt")])


@bp.route('/', methods=('GET', 'POST'))
def index():
    form = FileForm()
    if form.validate_on_submit():
        user_ = form.user_.data
        if user_ in current_app.config["USER"]:
            file_ = form.file_.data
            filename = f"{user_}.xlsx"
            fullname = os.path.join(current_app.config["TMP_PATH"], filename)
            file_.save(fullname)
            try:
                master = Master(settings=Settings(os.path.join(current_app.instance_path, current_app.config["USER"][user_])))
                master.run(user_, form.pass_.data, fullname, None)
                return send_file(fullname, attachment_filename=filename)
            except Exception as e:
                flash("Error: "+str(e.args), "danger")
            return redirect(url_for('main.index'))
        flash("Login failed", "warning")
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
#  - do not create backups: needs refactoring of master
#    refactoring could maybe avoid saving completely?
#  - delete files as soon as possible again
#  - think about setup that limits access
#  - propper layout/css

