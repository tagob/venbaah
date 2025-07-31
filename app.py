from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, send_from_directory
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Email, Length
import os
import json
import sqlite3
from datetime import datetime
from werkzeug.utils import secure_filename
import uuid

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-change-in-production'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs('static/css', exist_ok=True)
os.makedirs('static/images', exist_ok=True)
os.makedirs('templates', exist_ok=True)

# Database setup
def init_db():
    conn = sqlite3.connect('venbaah.db')
    cursor = conn.cursor()
    
    # Contact submissions table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS contact_submissions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            subject TEXT,
            message TEXT NOT NULL,
            submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Uploaded books table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            description TEXT,
            filename TEXT NOT NULL,
            original_filename TEXT NOT NULL,
            uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()

# Forms
class ContactForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=100)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    subject = StringField('Subject', validators=[Length(max=200)])
    message = TextAreaField('Message', validators=[DataRequired(), Length(min=10, max=1000)])
    submit = SubmitField('Send Message')

class BookUploadForm(FlaskForm):
    title = StringField('Book Title', validators=[DataRequired(), Length(min=2, max=200)])
    author = StringField('Author', validators=[DataRequired(), Length(min=2, max=100)])
    description = TextAreaField('Description', validators=[Length(max=500)])
    file = FileField('PDF File', validators=[
        FileRequired(),
        FileAllowed(['pdf'], 'Only PDF files are allowed!')
    ])
    submit = SubmitField('Upload Book')

# Routes
@app.route('/')
def home():
    # Get featured books from database
    conn = sqlite3.connect('venbaah.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM books ORDER BY uploaded_at DESC LIMIT 3')
    featured_books = cursor.fetchall()
    conn.close()
    
    return render_template('index.html', featured_books=featured_books)

@app.route('/archives')
def archives():
    # Get all books from database
    conn = sqlite3.connect('venbaah.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM books ORDER BY uploaded_at DESC')
    books = cursor.fetchall()
    conn.close()
    
    return render_template('archives.html', books=books)

@app.route('/editorial')
def editorial():
    return render_template('editorial.html')

@app.route('/manuscript')
def manuscript():
    return render_template('manuscript.html')

@app.route('/policies')
def policies():
    return render_template('policies.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    
    if form.validate_on_submit():
        # Store in database
        conn = sqlite3.connect('venbaah.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO contact_submissions (name, email, subject, message)
            VALUES (?, ?, ?, ?)
        ''', (form.name.data, form.email.data, form.subject.data, form.message.data))
        conn.commit()
        conn.close()
        
        flash('Thank you for your message! We will get back to you soon.', 'success')
        return redirect(url_for('contact'))
    
    return render_template('contact.html', form=form)

@app.route('/upload-book', methods=['GET', 'POST'])
def upload_book():
    form = BookUploadForm()
    
    if form.validate_on_submit():
        file = form.file.data
        if file:
            # Generate unique filename
            filename = str(uuid.uuid4()) + '.pdf'
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            
            # Store in database
            conn = sqlite3.connect('venbaah.db')
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO books (title, author, description, filename, original_filename)
                VALUES (?, ?, ?, ?, ?)
            ''', (form.title.data, form.author.data, form.description.data, 
                  filename, secure_filename(file.filename)))
            conn.commit()
            conn.close()
            
            flash('Book uploaded successfully!', 'success')
            return redirect(url_for('archives'))
    
    return render_template('upload_book.html', form=form)

@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)

@app.route('/view/<filename>')
def view_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# API endpoints
@app.route('/api/books')
def api_books():
    conn = sqlite3.connect('venbaah.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM books ORDER BY uploaded_at DESC')
    books = cursor.fetchall()
    conn.close()
    
    books_list = []
    for book in books:
        books_list.append({
            'id': book[0],
            'title': book[1],
            'author': book[2],
            'description': book[3],
            'filename': book[4],
            'original_filename': book[5],
            'uploaded_at': book[6]
        })
    
    return jsonify(books_list)

@app.route('/api/contact-submissions')
def api_contact_submissions():
    conn = sqlite3.connect('venbaah.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM contact_submissions ORDER BY submitted_at DESC')
    submissions = cursor.fetchall()
    conn.close()
    
    submissions_list = []
    for submission in submissions:
        submissions_list.append({
            'id': submission[0],
            'name': submission[1],
            'email': submission[2],
            'subject': submission[3],
            'message': submission[4],
            'submitted_at': submission[5]
        })
    
    return jsonify(submissions_list)

# Error handlers
@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500

if __name__ == '__main__':
    init_db()
    app.run(debug=True)