# Venbaah Poetry Journal - Flask Backend

A clean and elegant Flask backend for the Venbaah Tamil poetry journal website.

## Features

- **Complete Website Structure**: Home, Archives, Editorial, Manuscript Guidelines, Policies, and Contact pages
- **File Upload System**: Upload and manage PDF books/papers
- **Contact Form**: Store contact submissions in SQLite database
- **Responsive Design**: Mobile-friendly layout with beautiful typography
- **Database Integration**: SQLite for storing books and contact submissions
- **Static File Serving**: CSS, images, and uploaded files
- **Form Validation**: Secure form handling with Flask-WTF
- **API Endpoints**: JSON APIs for books and contact submissions

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
python app.py
```

3. Visit `http://localhost:5000` to view the website

## Project Structure

```
venbaah/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── venbaah.db            # SQLite database (created automatically)
├── templates/            # HTML templates
│   ├── base.html         # Base template
│   ├── index.html        # Homepage
│   ├── archives.html     # Archives page
│   ├── contact.html      # Contact form
│   ├── editorial.html    # Editorial board
│   ├── manuscript.html   # Submission guidelines
│   ├── policies.html     # Publication policies
│   ├── upload_book.html  # Book upload form
│   ├── 404.html          # Error pages
│   └── 500.html
├── static/               # Static assets
│   ├── css/
│   │   └── style.css     # Main stylesheet
│   └── images/           # Images and logos
└── uploads/              # Uploaded PDF files
```

## Key Routes

- `/` - Homepage with featured books
- `/archives` - Browse all uploaded books
- `/editorial` - Editorial board information
- `/manuscript` - Submission guidelines
- `/policies` - Publication policies
- `/contact` - Contact form
- `/upload-book` - Upload new books/papers
- `/api/books` - JSON API for books
- `/api/contact-submissions` - JSON API for contact submissions

## Database Schema

### Books Table
- `id` - Primary key
- `title` - Book title
- `author` - Author name
- `description` - Book description
- `filename` - Stored filename
- `original_filename` - Original filename
- `uploaded_at` - Upload timestamp

### Contact Submissions Table
- `id` - Primary key
- `name` - Contact name
- `email` - Contact email
- `subject` - Message subject
- `message` - Message content
- `submitted_at` - Submission timestamp

## Configuration

Update the following in `app.py` for production:
- Change `SECRET_KEY` to a secure random key
- Configure proper file upload limits
- Set up proper database backup
- Configure email notifications for contact forms

## Deployment

For production deployment:
1. Set `debug=False` in `app.run()`
2. Use a production WSGI server like Gunicorn
3. Configure proper file permissions for uploads
4. Set up database backups
5. Configure SSL/HTTPS

## Features

- **Beautiful Design**: Warm earthy colors with elegant typography
- **Tamil Support**: Proper Tamil font rendering
- **Responsive Layout**: Works on all devices
- **File Management**: Secure PDF upload and download
- **Form Validation**: Comprehensive form validation
- **Error Handling**: Custom 404 and 500 error pages
- **Flash Messages**: User feedback for actions
- **API Support**: RESTful endpoints for data access

## License

© 2023 Venbaah Publications. All rights reserved.