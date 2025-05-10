from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from .models import Note, Tags
from . import db
import json
from flask import make_response

def nocache(view):
    def no_cache_wrapper(*args, **kwargs):
        response = make_response(view(*args, **kwargs))
        response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "0"
        return response
    no_cache_wrapper.__name__ = view.__name__
    return no_cache_wrapper


views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
@nocache
def home():
    if request.method == 'POST':
        note = request.form.get('note')
        tag = request.form.get('tag')
        if len(note) < 1:
            flash('Note is too short!', category='error')
        else:
            
            existing_tag = Tags.query.filter_by(tag=tag).first()
            if not existing_tag:
                existing_tag = Tags(tag=tag)
                db.session.add(existing_tag)
                db.session.commit()  # Commit here to generate the tag.id

            new_note = Note(data=note, user_id=current_user.id, tag_id=existing_tag.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added!', category='success')
            return redirect(url_for('views.home'))
        
    return render_template('home.html', user=current_user, notes=current_user.notes)

@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
            flash('Note deleted!', category='success')
    return jsonify({})

@views.route('/search-notes', methods=['POST'])
@login_required
@nocache
def search_notes():
    search_query = request.form.get('searchInput')

    if not search_query:
        flash('Please enter a search term.', category='error')
        return render_template('home.html', user=current_user, notes=current_user.notes)

    if len(search_query) < 3:
        flash('Search term is too short!', category='error')
        return render_template('home.html', user=current_user, notes=current_user.notes)

    notes = Note.query.filter(Note.data.contains(search_query), Note.user_id == current_user.id).all()

    return render_template('home.html', user=current_user, search_notes=notes, search=search_query)


@views.route('/edit-note', methods=['GET', 'POST'])
@login_required
def edit_note():
    if request.method == 'GET':
        note_id = request.args.get('noteId')
        note = Note.query.get(note_id)
        if note and note.user_id == current_user.id:
            return render_template('home.html', user=current_user, edit_note=note, notes=current_user.notes)
        else:
            flash('Note not found or access denied.', category='error')
            return redirect(url_for('views.home'))

    if request.method == 'POST':
        new_note = request.form.get('note')
        note_id = request.form.get('note_id')

        if len(new_note) < 1:
            flash('Note is too short!', category='error')
            return redirect(url_for('views.home'))

        note = Note.query.get(note_id)
        if note and note.user_id == current_user.id:
            note.data = new_note
            db.session.commit()
            flash('Note updated!', category='success')
        else:
            flash('Note not found or access denied.', category='error')

        return redirect(url_for('views.home'))

