from flask import Flask, request, render_template, redirect, url_for
from flask_login import login_required, login_user, logout_user, current_user, UserMixin, LoginManager
from werkzeug.security import check_password_hash, generate_password_hash
from py2neo import Node, Relationship, Graph, NodeSelector

app = Flask(__name__)
graph = Graph()

login_manager = LoginManager()
login_manager.init_app(app)
# login_manager.login_view = 'signup'


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        result = NodeSelector(graph)
        Existing_user = result.select(request.form['username']).first()
        # print(Existing_user.)
        if not Existing_user:
            if request.form['conf-password'] == request.form['password']:
                hashedpass = generate_password_hash(request.form['password'], salt_length=32)
                user = Node("user", username=request.form['username'], email=request.form['email'], password=hashedpass)
                graph.create(user)
            return 'done'
        return 'This Username already exists! Try another one.'
    else:
        return render_template('signup.html')


if __name__ == '__main__':
    app.run(debug=True)
