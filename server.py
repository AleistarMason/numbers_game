from flask import Flask, render_template, redirect, request, session
import random

app = Flask(__name__)
app.secret_key = "abcdefghijclkmnop"

@app.route('/')
def index():
    if session.get('max_num') == None:
        session['guess_amount'] = 5
        session['init_guess_amount'] = 5
        session['max_num'] = 100
    if session.get('answer') and session.get('guess'):
        width = 300
        height = 300
        results = ""
        color = "darkslategrey"
        if session.get('guess') > session['answer']:
            results = "Too High"
            color = 'red'
        elif session.get('guess') < session['answer']:
            results = 'Too Low'
            color = 'red'
        elif session.get('guess') == session['answer']:
            results = 'You Got It Right!!!'
            color = 'green'
    else:
        session['answer'] = random.randint(1, session['max_num'])
        session['total_guesses'] = 0
        session['complete'] = False
        width = 0
        height = 0
        results = ""
        color = "darkslategrey"
    print(session)
    return render_template('index.html', width = width, height = height, color = color, results = results )

@app.route('/leaderboard')
def leaderboard():
    print(session['winners'])
    return render_template('leaderboard.html')

@app.route('/leaderboard_submission', methods=['POST'])
def leaderboard_submission():
    if session.get('winners') == None:
        session['winners'] = []
    list = session['winners']
    list.append({
        'player_name': request.form['name'],
        'total_guesses': int(session['total_guesses']),
        'max_num': int(session['max_num'])
    })
    session['winners'] = list
    for player in session['winners']:
        print(player)
    return redirect('/leaderboard')

@app.route('/win', methods=['POST'])
def winner():
    session['leaderboard_submit'] = True
    return redirect('/')

@app.route('/difficulty', methods=['POST'])
def difficulty():
    session['guess_amount']= int(request.form['guess_amount'])
    session['init_guess_amount'] = int(request.form['guess_amount'])
    session['max_num'] = int(request.form['num'])
    session['total_guesses'] = 0
    session['answer'] = random.randint(1, session['max_num'] )
    session['complete'] = False
    return redirect('/')

@app.route('/guess', methods=['POST'])
def guess():
    session['guess_amount'] -= 1
    session['total_guesses'] += 1
    session['guess'] = int(request.form['guess'])
    if int(request.form['guess']) == session['answer'] or session['guess_amount'] <= 0:
        session['complete'] = True
    return redirect('/')

@app.route('/replay', methods=['POST'])
def replay():
    if session.get('total_guesses'):
        session.pop('total_guesses')
    if session.get('guess'):
        session.pop('guess')
    if session.get('anwser'):
        session.pop('answer')
    session['guess_amount'] = session['init_guess_amount']
    session['complete'] = False
    session['leaderboard_submit'] = False
    return redirect('/')

@app.route('/reset', methods=['POST'])
def reset():
    for key in list(session.keys()):
        session.pop(key)
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)