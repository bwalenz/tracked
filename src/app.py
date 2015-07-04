from flask import Flask
from flask_sqlalchemy import SQLAlchemy

import flask_admin as admin
from flask_admin.contrib import sqla
app = Flask(__name__)


app.config['SECRET_KEY'] = 'tracked_secret_omg'
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://tracked_user:pw_tracked@localhost/tracked"
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

# Flask views
@app.route('/')
def index():
    return '<a href="/admin/">Click me to get to Admin!</a>'

class Paper(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(255), unique=True)
    title = db.Column(db.Text, unique=True)
    citation = db.Column(db.Text) 

    def __unicode__(self):
        return self.url

class ReadPaper(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    paper_id = db.Column(db.Integer, db.ForeignKey(Paper.id))
    paper = db.relationship(Paper)
    pass_number = db.Column(db.Integer)
    date = db.Column(db.Date)

    def __unicode__(self):
        return self.pass_number

class PaperAdmin(sqla.ModelView):
    inline_models = (ReadPaper,)

admin = admin.Admin(app, name='Tracked', template_mode='bootstrap3')

#admin.add_view(PaperAdmin(Paper, db.session))
admin.add_view(sqla.ModelView(Paper, db.session))
admin.add_view(sqla.ModelView(ReadPaper, db.session))
if __name__ == '__main__':
    db.drop_all()
    db.create_all()
    app.run(host='0.0.0.0', debug=True)
