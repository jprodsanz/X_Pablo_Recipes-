from flask import render_template,redirect, session, request, flash, url_for
from flask_app import app
from flask_app.models.registrant import Registrant
from flask_bcrypt import Bcrypt 
bcrypt = Bcrypt(app)


@app.route('/')
def home():
    return render_template('register.html')

@app.route('/register', methods=['POST'])
def register():

    if not Registrant.validate_register(request.form):
        return redirect('/')

    data = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": bcrypt.generate_password_hash(request.form['password'])
    }

    id = Registrant.save(data)
    session['registrant_id'] = id

    return redirect('/recipes/dashboard')

@app.route('/home')
def home_2():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    registrant = Registrant.get_by_email(request.form)

    if not registrant: 
        flash("Invalid Email", "login")
        return redirect('/')
    if not bcrypt.check_password_hash(registrant.password, request.form['password']):
        flash ("Invalid Password", "login")
        return redirect('/')
    session['registrant_id'] = registrant.id
    return redirect('/recipes/dashboard')

@app.route('/dashboard')
def dashboard():
    if 'registrant_id' not in session: 
        return redirect('/logout')
    data= {
        'id': session['registrant_id']
    }
    return render_template('dashboard.html', registrant=Registrant.get_by_id(data))

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')
    