from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

app.config['SECRET_KEY'] = 'your_secret_key_here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/form', methods=['GET','POST'])
def form():
    if request.method == 'POST':
        return redirect(url_for('dashboard'))
    return render_template('form.html', form=form)

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

if __name__ == '__main__':
    app.run(debug=True)