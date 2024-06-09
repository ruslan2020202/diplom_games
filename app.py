import time

from flask import Flask, render_template, request, url_for, redirect, session, make_response, jsonify
from flask_migrate import Migrate
from flask_cors import CORS
from flask_marshmallow import Marshmallow

from config import Config
from models import db, User, Score, get_rating
from schema import user_schema

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
Migrate(app, db)
CORS(app)
Marshmallow(app)


def add_user(email: str) -> None:
    session['user'] = email


def get_user() -> int | None:
    return session.get('user', None)


@app.route('/')
def index():
    return render_template('glav.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        try:
            name = request.form.get('name')
            email = request.form.get('email')
            password = request.form.get('password')
            search = User.find_by_email(email)
            if not search:
                User(name=name, email=email, password=password).save()
                time.sleep(2)
                user_id = User.find_by_email(email).id
                Score(user_id=user_id).save()
            else:
                return render_template('123.html', error_message='Пользователь с такой почтой уже существует')
            return redirect(url_for("login"))
        except Exception as e:
            print(e)
    return render_template('123.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        search = User.find_by_email(email)
        if search and search.password == password:
            add_user(search.id)
            return redirect(url_for('main'))
        else:
            return render_template('login.html', error_message='Неправильный логин или пароль')
    return render_template('login.html')


@app.route('/main')
def main():
    return render_template('fon.html')


# крестики нолики
@app.get('/crestiki_noliki')
def crestiki_noliki():
    if get_user() is None:
        return redirect(url_for('signup'))
    return render_template('index.html')


@app.route('/rules/crestiki_noliki')
def rules_crestiki_noliki():
    return render_template('prxo.html')


# змейка

@app.route('/zmeyka')
def zmeyka():
    if get_user() is None:
        return redirect(url_for('signup'))
    return render_template('zmey.html')


@app.route('/rules/zmeyka')
def rules_zmeyka():
    return render_template('zm.html')


# 2048

@app.route('/game2048')
def game2048():
    if get_user() is None:
        return redirect(url_for('signup'))
    return render_template('2048.html')


@app.route('/rules/game2048')
def rules_game2048():
    return render_template('pr2048.html')


# Bricks n Balls

@app.route('/BricksnBalls')
def bricksn_balls():
    if get_user() is None:
        return redirect(url_for('signup'))
    return render_template('2d.html')


@app.route('/rules/BricksnBalls')
def rules_bricksn_balls():
    return render_template('2dpr.html')


# tetris

@app.route('/tetris')
def tetris():
    if get_user() is None:
        return redirect(url_for('signup'))
    return render_template('tet.html')


@app.route('/rules/tetris')
def rules_tetris():
    return render_template('prtet.html')


# settings
@app.route('/add_point_snake', methods=['POST'])
def add_point_snake():
    try:
        point = request.json
        score = Score.query.filter_by(user_id=get_user()).first()
        if score.point_snake < int(point['maxScore']):
            score.point_snake = point['maxScore']
        score.save()
        return make_response(jsonify({'success': True}), 200)
    except Exception as e:
        print(e)
        return make_response(jsonify({'failed': True, 'message': str(e)}), 500)


@app.route('/add_point_bb', methods=['POST'])
def add_point_bb():
    try:
        point = request.json
        score = Score.query.filter_by(user_id=get_user()).first()
        if score.point_bricks < int(point['HIGH_SCORE']):
            score.point_bricks = point['HIGH_SCORE']
        score.save()
        return make_response(jsonify({'success': True}), 200)
    except Exception as e:
        print(e)
        return make_response(jsonify({'failed': True, 'message': str(e)}), 500)


@app.route('/add_point_tetris', methods=['POST'])
def add_point_tetris():
    try:
        point = request.json
        score = Score.query.filter_by(user_id=get_user()).first()
        if score.point_tetris < int(point['score_high']):
            score.point_tetris = point['score_high']
        score.save()
        return make_response(jsonify({'success': True}), 200)
    except Exception as e:
        print(e)
        return make_response(jsonify({'failed': True, 'message': str(e)}), 500)


@app.get('/rating')
def rating():
    return user_schema.dump(get_rating())


if __name__ == '__main__':
    app.run()
