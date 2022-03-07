from flask import Blueprint, render_template, request

from apps.article.model import Article
from apps.user.model import User
from ext import db

article_bp = Blueprint('article', __name__)


@article_bp.route('/publish', methods=['GET', 'POST'])
def publish_article():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        uid = request.form.get('uid')
        # 添加文章
        article = Article()
        article.title = title
        article.content = content
        article.user_id = uid
        db.session.add(article)
        db.session.commit()
        return 'ok'
    else:
        users = User.query.filter(User.isdelete == False).all()
        return render_template('article/add_article.html', users=users)

@article_bp.route('/all')
def all_article():
    articles = Article.query.all()
    return render_template('article/all.html',articles=articles)