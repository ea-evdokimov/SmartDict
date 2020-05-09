import os
import unittest

from app import app, db, MyTranslate, tr

class BsicTest(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['DEBUG'] = False
        
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        
        self.app = app.test_client()
        
        db.drop_all()
        db.create_all()

        self.assertEqual(app.debug, False)

    def tearDown(self):
        pass
    
    def test_data_base(self):
        input_word = "hello"
        
        new_word = MyTranslate(original=input_word, translated="Привет")
        
        db.drop_all()
        db.create_all()
        
        translated = tr.translate(input_word, dest='ru').text
        
        self.assertEqual(translated, "Привет")

        db.session.add(new_word)
        db.session.commit()
        
        first = MyTranslate.query.first()
        self.assertEqual(first.original, input_word)

        self.assertEqual(first.translated, translated)

    def test_transl(self):
        input1 = "new" 
        input2 = "car"
        input3 = "experiment"

        a = tr.translate(input1, dest='ru').text
        b = tr.translate(input2, dest='ru').text
        c = tr.translate(input3, dest='ru').text
        
        self.assertEqual(a, "новый")
        self.assertEqual(b, "машина")
        self.assertEqual(c, "эксперимент")

    def test_del_data_base(self):
        db.drop_all()
        db.create_all()
        
        input_word = "hello"
        new_word = MyTranslate(original=input_word, translated="Привет")
        translated = tr.translate(input_word, dest='ru').text
        
        self.assertEqual(translated, "Привет")

        db.session.add(new_word)
        db.session.commit()
        
        first = MyTranslate.query.first()
        self.assertEqual(first.original, input_word)
        self.assertEqual(first.translated, translated)


        input_word = "car"
        translated = tr.translate(input_word, dest='ru').text
        new_word = MyTranslate(original=input_word, translated=translated)
        db.session.add(new_word)

        word_to_delete = MyTranslate.query.get_or_404(1)
        db.session.delete(word_to_delete)
        db.session.commit()

        first = MyTranslate.query.first()
        self.assertEqual(first.original, input_word)
        self.assertEqual(first.translated, "машина")

        word_to_delete = MyTranslate.query.get_or_404(2)
        db.session.delete(word_to_delete)
        db.session.commit()

        self.assertEqual(MyTranslate.query.first(), None)
        
if __name__ == "__main__":
    unittest.main()