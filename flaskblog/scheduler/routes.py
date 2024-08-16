from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from flaskblog import db
from flaskblog.models import Post
from flaskblog.posts.forms import PostForm
from flaskblog.models import Scheduler

scheduler = Blueprint('scheduler', __name__)


@scheduler.route("/remainder", methods=['GET', 'POST'])
def remainder():

    scheduler = Scheduler.query.first()
    return render_template('remainder.html', title='Document Remainder', scheduler=scheduler)
