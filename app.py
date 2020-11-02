from flask import Flask, render_template, request, redirect, url_for, jsonify
import pandas as pd
from dbsetup import *
from data_manipulation import *
import json

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config["DEBUG"] = True

(host, user, password, database) = get_creds('ideas_db')


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        selectedValue = request.form['consent']
        selectedValue = selectedValue.replace(' ', '_')
        if selectedValue == 'I_do_not_agree':
            return redirect(url_for('exit'))
        else:
            return redirect(url_for('instructions'))
    return render_template('index.html')


@app.route('/exit', methods=['GET', 'POST'])
def exit():
    return render_template('exit.html')


@app.route('/instructions', methods=['GET', 'POST'])
def instructions():
    if request.method == 'POST':
        if 'Continue' in request.form['directions']:
            return redirect(url_for('english_test'))
    return render_template('instructions.html')

@app.route('/english_test', methods=['GET', 'POST'])
def english_test():
    if request.method == 'POST':
        first_question = request.form['first_question']
        second_question = request.form['second_question']
        third_question = request.form['third_question']
        fourth_question = request.form['fourth_question']
        if (first_question == 'on' and second_question == 'the eighth' and third_question == 'a little' and fourth_question == 'can do, cannot do'):
            return redirect(url_for('app_display'))
        else:
            return redirect(url_for('app_display_failed'))
    return render_template('english_test.html')


@app.route('/app_display_failed', methods=['GET', 'POST'])
def app_display_failed():
    conn = connect(host, user, password, database)
    questionsd_df = pd.read_csv('questions.csv')
    questions = questionsd_df['questions'].tolist()
    data_list = get_randomSample(conn, 15)
    return render_template('app_display_failed.html', data=data_list, questions=questions)

@app.route('/failed_results', methods=['GET', 'POST'])
def failed_results():
    (host_code, user_code, password_code, database_code) = get_creds('password_db')
    conn_userCode = connect(host_code, user_code, password_code, database_code)
    if request.method == 'POST':
        user_passcode = get_userCode(conn_userCode)
        update_failed(conn_userCode, user_passcode)
    return render_template('failed_results.html', user_passcode=user_passcode)



@app.route('/app_display', methods=['GET', 'POST'])
def app_display():
    conn = connect(host, user, password, database)
    (data_list, id_list) = get_SampleIdeas(conn, 10, 15)
    questionsd_df = pd.read_csv('questions.csv')
    questions = questionsd_df['questions'].tolist()
    if len(id_list) > 0:
        return render_template('app_display.html', data=data_list, questions=questions, id_list = id_list)
    else:
        redirect(url_for('get_ratings'))


@app.route('/result', methods=['GET', 'POST'])
def get_results():
    (host_code, user_code, password_code, database_code) = get_creds('password_db')
    conn_userCode = connect(host_code, user_code, password_code, database_code)
    conn = connect(host, user, password, database)
    if request.method == 'POST':
        result_dict = request.form.to_dict()
        all_ideas = get_allIdeas(result_dict)
        update_ViewCount(conn, all_ideas)
        (novel, original, feasible) = sort_results(result_dict)
        if len(novel) != 0:
            update_novel(conn, novel)
        else:
            None
        if len(original) != 0:
            update_original(conn, original)
        else:
            None
        if len(feasible) != 0:
            update_feasible(conn, feasible)
        else:
            None
    user_passcode = get_userCode(conn_userCode)
    update_success(conn_userCode, user_passcode)
    return render_template('result.html', user_passcode=user_passcode)


@app.route('/get_ratings', methods=['GET', 'POST'])
def get_ratings():
    (host_code, user_code, password_code, database_code) = get_creds('password_db')
    conn_userCode = connect(host_code, user_code, password_code, database_code)
    if request.method == 'POST':
        difficulty_rating = request.form['difficulty_rating']
        certainty_rating = request.form['certainty_rating']
        user_passcode = request.form['user_passcode']
        update_UserCode(conn_userCode, user_passcode)
        update_ratings(conn_userCode, difficulty_rating, certainty_rating, user_passcode)
    return jsonify(dict(redirect='/user_exit'))


@app.route('/user_exit', methods=['GET', 'POST'])
def user_exit():
    return render_template('user_exit.html')


if __name__ == '__main__':
    app.run(debug=True)
