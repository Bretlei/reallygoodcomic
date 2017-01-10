import sqlite3
from flask import Flask, render_template, g

app = Flask(__name__, template_folder = 'template')

DATABASE = 'db.db'

db = sqlite3.connect(DATABASE)
db.row_factory = sqlite3.Row

@app.route('/') # www.whatever.com/
def index():
    index_comic = db.execute('SELECT * FROM comics ORDER BY id DESC LIMIT 1').fetchone()

    if index_comic is False:
        return "NO COMICS IN THE DATABASE"

    previous_comic = db.execute('select slug from comics where id = ?', [index_comic['id'] - 1]).fetchone()
    next_comic = db.execute('select slug from comics where id = ?', [index_comic['id'] + 1]).fetchone()
    first_comic = db.execute('select * from comics order by id limit 1').fetchone()
    last_comic = db.execute('select * from comics order by id desc limit 1').fetchone()

    return render_template('index_page.html', comic=index_comic, first=first_comic, last=last_comic, prev=previous_comic, next=next_comic) # When you route to www.whatever.com/ load the index.html template

@app.route('/archive')
def archive():
    archive_comics = db.execute('select * from comics').fetchall()
    return render_template('archive_page.html', arch_comics=archive_comics)

@app.route('/<slug>')
def show_comic(slug):
    comic = db.execute('select * from comics where slug = ?', [slug]).fetchone()

    if comic:
        # Previous / next comic
        previous_comic = db.execute('select slug from comics where id = ?', [comic['id'] - 1]).fetchone()
        next_comic = db.execute('select slug from comics where id = ?', [comic['id'] + 1]).fetchone()
        first_comic = db.execute('select * from comics order by id limit 1').fetchone()
        last_comic = db.execute('select * from comics order by id desc limit 1').fetchone()

        return render_template('comic_page.html', comic=comic, first=first_comic, last=last_comic, prev=previous_comic, next=next_comic)
    else:
        return 'Either found none or too many XD: %d' % len(comics)

if __name__ == '__main__': # Run the fucking app
    app.run(host='0.0.0.0', port=80)
