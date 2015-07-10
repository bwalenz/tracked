from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask import jsonify
import flask_admin as admin
from flask_admin.contrib import sqla
from flask import Response
import json

app = Flask(__name__)


app.config['SECRET_KEY'] = 'tracked_secret_omg'
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://tracked_user:pw_tracked@localhost/tracked"
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

# Flask views
@app.route('/')
def index():
    return '<a href="/admin/">Click me to get to Admin!</a>'

@app.route('/papers')
def papers():
    papers = ReadPaper.query.all()
    paper_list = []
    for paper in papers:
        tag_str = ""
        for tag in paper.paper.tags:
            tag_str += '<a href = "/tag/' + str(tag.tag.id) + '">' + tag.tag.text + '</a>, '
        paper_dict = {"date":str(paper.date), "pass_number":str(paper.pass_number), "title":paper.paper.title, "url":paper.paper.url, "tags":tag_str}
        paper_list.append(paper_dict)
    jp = json.dumps(paper_list)
    return Response(jp,  mimetype='application/json')
    #return json_papers

class IndexPage(admin.AdminIndexView):
    @admin.expose('/')
    def index(self):
        papers = ReadPaper.query.all()
        return self.render('admin/index.html', read_papers=papers)

class Paper(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(255), unique=True)
    title = db.Column(db.Text, unique=True)
    citation = db.Column(db.Text)
    tags = db.relationship("PaperTag")
    def __unicode__(self):
        return self.title

class ReadPaper(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    paper_id = db.Column(db.Integer, db.ForeignKey(Paper.id))
    paper = db.relationship(Paper)
    pass_number = db.Column(db.Integer)
    date = db.Column(db.Date)

    def __unicode__(self):
        return self.pass_number

class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(255), unique=True)

    def __unicode__(self):
        return self.text

class PaperTag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey(Tag.id))
    paper_id = db.Column(db.Integer, db.ForeignKey(Paper.id))
    paper = db.relationship(Paper)
    tag = db.relationship(Tag)

    def __unicode__(self):
        return self.paper.title + " : " + self.tag.text

admin = admin.Admin(app, index_view=IndexPage(), name='Tracked', template_mode='bootstrap3')

#admin.add_view(PaperAdmin(Paper, db.session))
admin.add_view(sqla.ModelView(Paper, db.session))
admin.add_view(sqla.ModelView(ReadPaper, db.session))
admin.add_view(sqla.ModelView(Tag, db.session))
admin.add_view(sqla.ModelView(PaperTag, db.session))

if __name__ == '__main__':
    #db.drop_all()
    #db.create_all()
    app.run(host='0.0.0.0', debug=True)
