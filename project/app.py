from flask import Flask, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
from googletrans import Translator

MAX_ID = 100

tr = Translator()

app = Flask(__name__)
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
   if request.method == "POST":
      input_word = request.form["input"]

      if input_word != "":
         # print(input_word)
         translated = tr.translate(input_word, dest='ru').text
         # print(translated)
         new_word = MyTranslate(original=input_word, translated=translated)

         try:
            db.session.add(new_word)
            db.session.commit()
            return redirect(request.url) 
         except:
            return 'Problem with database'
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
      return redirect('/')
   except:
      return 'Problem with database'

