from flask import Flask, render_template, redirect, request
import datetime

from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField, BooleanField, FileField, StringField, \
    IntegerField, DateField, RadioField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = 'futa_loli_neco_trap'
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(days=365)


class TargetForm(FlaskForm):
    cover = FileField('Загрузить обложку', validators=[DataRequired()])
    name = StringField('Название сбора', validators=[DataRequired()])
    cost = IntegerField('Сумма, ₽', validators=[DataRequired()])
    target = StringField('Цель', validators=[DataRequired()])
    description = StringField('Описание', validators=[DataRequired()])
    account = StringField('Куда получать деньги', validators=[DataRequired()])
    submit = SubmitField('Далее')


class TargetMoreForm(FlaskForm):
    author = StringField('Автор', validators=[DataRequired()])
    type = RadioField('Сбор завершится', choices=[('0', 'Когда соберём сумму'),
                                                  ('1', 'В определённую дату')], validators=[DataRequired()])
    date = DateField('Дата окончания', validators=[DataRequired()])
    submit = SubmitField('Создать сбор')


class RegularForm(FlaskForm):
    cover = FileField('Загрузить обложку', validators=[DataRequired()])
    name = StringField('Название сбора', validators=[DataRequired()])
    cost = IntegerField('Сумма, ₽', validators=[DataRequired()])
    target = StringField('Цель', validators=[DataRequired()])
    description = StringField('Описание', validators=[DataRequired()])
    account = StringField('Куда получать деньги', validators=[DataRequired()])
    author = StringField('Автор', validators=[DataRequired()])
    submit = SubmitField('Далее')


@app.route('/')
def index():
    params = dict()
    params['title'] = "Пожертвования"
    return render_template('index.html', **params)


@app.route('/choosing_type')
def choosing_type():
    params = dict()
    params['title'] = "Пожертвования"
    return render_template('choosing_type.html', **params)


@app.route('/target', methods=['GET', 'POST'])
def target():
    form = TargetForm()
    params = dict()
    params['title'] = "Целевой сбор"
    params['form'] = form
    if form.validate_on_submit():
        print(f'{form.cover.data}, {form.name.data}, {form.cost.data}, {form.target.data},'
              f' {form.description.data}, {form.account.data},')
        return redirect("/target/more")
    return render_template('target.html', **params)


@app.route('/target/more', methods=['GET', 'POST'])
def target_more():
    form = TargetMoreForm()
    params = dict()
    params['title'] = "Целевой сбор"
    params['form'] = form
    if form.submit() and request.method == 'POST' and form.type.data in ['0', '1']:
        print(f'{form.author.data}, {form.type.data}, {form.date.data}')
        return redirect("/success")
    return render_template('target_more.html', **params)


@app.route('/regular', methods=['GET', 'POST'])
def regular():
    form = RegularForm()
    params = dict()
    params['title'] = "Целевой сбор"
    params['form'] = form
    if form.validate_on_submit():
        print(f'{form.cover.data}, {form.name.data}, {form.cost.data}, {form.target.data},'
              f' {form.description.data}, {form.account.data}, {form.author.data}')
        return redirect("/success")
    return render_template('regular.html', **params)


@app.route('/success')
def success():
    params = dict()
    params['title'] = "Пожертвования"
    return render_template('success.html', **params)


@app.errorhandler(404)
def not_found(error):
    params = dict()
    params['title'] = "Страница не найдена"
    params['cause'] = "Страница не найдена"
    return render_template('service/error.html', **params)


@app.errorhandler(500)
def not_found(error):
    params = dict()
    params['title'] = "Ошибка сервера"
    params['cause'] = "Ошибка сервера"
    return render_template('service/error.html', **params)


def main():
    app.run(port=8080, host='127.0.0.1')


if __name__ == '__main__':
    main()
