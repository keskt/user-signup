from flask import Flask, request, redirect
import cgi
import os
import jinja2

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape=True)

app = Flask(__name__)
app.config['DEBUG'] = True

@app.route("/")
def display_form():
    template = jinja_env.get_template('home.html')
    return template.render()
   
def not_empty(textString):
    if textString and textString.strip():
        return True
    else:
        return False

def has_space(textString):
    if " " in textString: #contains a space
        return True
    else:
        return False

def has_char(textString, character):
    count1 = 0
    for char in textString:
        if char == character:
            count1 = count1 + 1
    if count1 == 1:
        return True
    else:
        return False

@app.route("/", methods=['POST'])
def validate_signup():
    username = request.form['username']
    password = request.form['password']
    verify = request.form['verify']
    email = request.form['email']

    username_error = '' 
    password_error = ''
    verify_error = ''
    email_error = ''

    if not not_empty(username):
        username_error = 'Not a valid username'
        username = ''
    elif has_space(username):
        username_error = 'Not a valid username'
        username = ''
    elif len(username) > 20 or len(username) < 3:
        username_error = 'Not a valid username'
        username = ''
    
    if not not_empty(password):
        password_error = 'Not a valid password'
        password = ''
    elif has_space(password):
        password_error = 'Not a valid password'
        password = ''
    elif len(password) > 20 or len(password) < 3:
        password_error = 'Not a valid password'
        password = ''
    
    if not not_empty(verify):
        verify_error = 'Not a valid password'
        verify = ''
    elif verify != password:
        verify_error = 'Passwords do not match'
        verify = ''
    
    if not_empty(email):
        if has_space(email):  
            email_error = 'Not a valid email'
            email = ''
        elif len(email) > 20 or len(email) < 3:
            email_error = 'Not a valid email'
            email = ''
        elif '@' not in email or '.' not in email:
            email_error = 'Not a valid email'
            email = ''
        elif has_char(email, "@") == False:
            email_error = 'Not a valid email'
            email = ''
        elif has_char(email, ".") == False:
            email_error = 'Not a valid email'
            email = ''

    if not username_error and not password_error and not verify_error and not email_error:
        username = request.form['username']
        return redirect('/welcome?username={0}'.format(username))
    else:
        template = jinja_env.get_template('home.html')
        return template.render(username_error=username_error,
            password_error=password_error, verify_error=verify_error, email_error=email_error, 
            username=username, email=email)

@app.route('/welcome')
def valid_signup():
    username = request.args.get('username')
    template = jinja_env.get_template('welcome.html')
    return template.render(username=username)

app.run()