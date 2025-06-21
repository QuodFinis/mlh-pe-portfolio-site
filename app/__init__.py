from flask import Flask, render_template

app = Flask(__name__)

nav_items = {
    'index': 'Home',
    'hobbies': 'Hobbies'
}

@app.context_processor
def inject_nav_items():
    return dict(nav_items=nav_items)

@app.route('/')
def index():
    return render_template(
        'index.html',
        title="My Portfolio"
    )

@app.route('/hobbies')
def hobbies():
    return render_template(
        'hobbies.html',
        title="Hobbies"
    )
