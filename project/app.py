from flask import Flask, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
from googletrans import Translator
D = {}
MAX_ID = 100

tr = Translator()

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db = SQLAlchemy(app)


class MyTranslate(db.Model):
   id = db.Column(db.Integer, primary_key=True)
   original = db.Column(db.String(100), nullable=False)
   translated = db.Column(db.String(100), default="")
   
   def __repr__(self):
      return f"Word('{self.original}', '{self.translated}')"


@app.route('/', methods=["POST", "GET"])
def index():
   if len(D) == 0:
      db.drop_all()
      db.create_all()
   if request.method == "POST":
      input_word = request.form["input"]

      if input_word != "" and not input_word in D.keys():
         # print(input_word)
         translated = tr.translate(input_word, dest='ru').text
         # print(translated)
         if input_word != translated:
            new_word = MyTranslate(original=input_word, translated=translated)

            try:
               db.session.add(new_word)
               db.session.commit()
               D[input_word] = 1
               return redirect(request.url) 
            except:
               return 'Problem with database'
      
      if input_word in D.keys():
         D[input_word] += 1

      return redirect(request.url)
   else:
      words = MyTranslate.query.order_by(-MyTranslate.id).all()
      return render_template('index.html', words=words)


@app.route('/delete/<int:id>')
def delete(id):
   word_to_delete = MyTranslate.query.get_or_404(id)

   try:
      db.session.delete(word_to_delete)
      db.session.commit()
      orig = word_to_delete.original
      del D[orig]

      return redirect('/')
   except:
      return 'Problem with database'

@app.route('/list', methods=["POST", "GET"])
def new_list():
   words = MyTranslate.query.order_by(MyTranslate.id).all()
   return render_template('table.html', words=words)

@app.route('/stat', methods=["POST", "GET"])
def new_stat():
   return D