from flask import (Flask, g, render_template, flash, redirect, url_for,
                  abort)
import forms
import models

DEBUG = True
PORT = 8000
HOST = '0.0.0.0'

app = Flask(__name__)
app.secret_key = 'wiuher283ywhri;whesfiuged9s;whwjvnflei'

@app.before_request
def before_request():
  g.db = models.DATABASE
  g.db.connect()

@app.after_request
def after_request(response):
  g.db.close()
  return response

@app.route('/')
def index():
  """View all the journal entries."""
  entries = models.Entry.select().limit(100)
  return render_template('index.html', entries=entries)


@app.route('/entries')
def view():
  """View all the journal entries."""
  entries = models.Entry.select().limit(100)
  return render_template('index.html', entries=entries)


@app.route('/entries/new', methods=('GET', 'POST'))
def create():
  """Creates a new Entry."""
  form = forms.EntryForm()
  if form.validate_on_submit():
    models.Entry.create(title=form.title.data.strip(),
                        created=form.create.data,
                        time_spent=form.timespent.data,
                        learned=form.learned.data.strip(),
                        to_remember=form.to_remember.data.strip())
    flash("This entry has been created!", "success")
    return redirect(url_for('index'))
  return render_template('new.html', form=form)


@app.route('/entries/<int:id>', methods=('GET', 'POST'))
def details(id):
  """Gives the details for an entry."""
  entries = models.Entry.select().where(models.Entry.id == id)
  if entries.count() == 0:
    abort(404)
  return render_template("detail.html", entries=entries)


@app.route('/entries/<int:id>/edit', methods=('GET', 'POST'))
def update():
  """Edits an entry."""
  entry = models.Entry.select().where(models.Entry.id == id)
  if entry.count() == 0:
    abort(404)
  form = forms.EntryForm()
  if form.validate_on_submit():
    models.Entry.update(title=form.title.data.strip(),
                        created=form.create.data,
                        time_spent=form.timespent.data,
                        learned=form.learned.data.strip(),
                        to_remember=form.to_remember.data.strip())
    flash("This entry has been updated!", "success")
    return redirect(url_for('index'))
  return render_template("edit.html", form=form, entry=entry)


@app.route('/entries/<int:id>/delete', methods=('GET', 'POST'))
def delete():
  """Deletes an entry."""
  entry = models.Entry.select().where(models.Entry.id == id)
  if entry.count() == 0:
    abort(404)
  entry.delete_instance()
  flash("This entry has been deleted!", "success")
  return redirect(url_for('index'))


if __name__ == "__main__":
  models.initialize()
  try:
    models.Entry.create_entry(
      title="First journal",
      time_spent=2,
      learned="Python!",
      to_remember="online resources")
  except ValueError:
    pass
  app.run(debug=DEBUG, host=HOST, port=PORT)


