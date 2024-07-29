from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///newflask.db'
db = SQLAlchemy(app)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(300), nullable=False)
    text = db.Column(db.Text, nullable=False)


@app.route("/index")
@app.route("/")
def index():
    return render_template('index.html')

@app.route ("/posts")
def posts():
    posts = Post.query.all()
    return render_template('posts.html', posts=posts)


@app.route("/create", methods=['POST', 'GET'])
def create():
    if request.method == 'POST':
        title = request.form['title']
        text = request.form['text']

        post = Post(title=title, text=text)

        try:
            db.session.add(post)
            db.session.commit()
            return redirect('/posts')
        except:
            return 'An error occurred while adding the article!'

    else:
        return render_template("create.html")


@app.route ('/delete/<int:post_id>', methods=['POST', ])
def delete(post_id):
    post = Post.query.get(post_id)
    if post:
        try:
            db.session.delete(post)
            db.session.commit()
            return redirect('/')
        except:
            return 'An error occurred while deleting the article!'
    else:
        return 'Post not found.', 404

if __name__ == '__main__':
    app.run(debug=True)
