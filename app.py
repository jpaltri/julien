# app.py
from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from datetime import datetime
import json
from config import Config
from flask_wtf import FlaskForm, CSRFProtect
from flask_wtf.file import FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, ValidationError, EmailField, URLField, TextAreaField, FileField, HiddenField, SelectField, DateTimeField, DateTimeLocalField, SelectMultipleField, DecimalRangeField, IntegerRangeField, IntegerField
from wtforms.validators import DataRequired, Email, EqualTo, Length, URL, Optional, NumberRange
from email.message import EmailMessage
import smtplib
import os

app = Flask(__name__)
app.config.from_object(Config)
csrf = CSRFProtect(app)
#
class SubscribeForm(FlaskForm):
    name = StringField('Name', validators=[
        DataRequired(message="Please enter your name"),
        Length(min=2, max=100, message="Name must be between 2 and 100 characters")
    ])
    email = EmailField('Email', validators=[
        DataRequired(message="Please enter your email"),
        Email(message="Please enter a valid email address")
    ])

# Store subscribers
subscribers = []

def load_data():
        
    try:
        with open('books.json', 'r') as f:
            books = json.load(f)
    except FileNotFoundError:
        # Sample books data
        books = [
            {
                "id": 1,
                "title": "The 4-Hour Work Week",
                "author": "Tim Ferriss",
                "category": "Personal Growth",
                "description": "Hands down, my all-time favorite book. Tim Ferriss nails it with practical, no-nonsense life hacks for boosting productivity. The guy’s a genius at getting stuff done, and this book completely flipped how I approach time management and delegation. From killer concepts like the 80/20 Pareto principle to weekly challenges that push you out of your comfort zone and spark growth, Ferriss packs it all into this game-changing 376-page gem.",                
                "image": "default_book.jpg"
            },
            {
                "id": 2,
                "title": "Atomic Habits",
                "author": "James Clear",
                "category": "Personal Growth",
                "description": "An absolute must-read for anyone looking to level up their productivity or nail down solid routines and habits. This book totally reshaped how I think about habits, with the key takeaway that we \"are\" our habits: '40 to 50 percent of our daily actions come from habit.' Blending sharp science, clear theory, and practical tips, it’s the perfect guide to kickstarting small, stacking habits that compound over time and propel you toward your goals.",
                "image": "default_book.jpg"
            },
            {
                "id": 3,
                "title": "Influence: The Psychology of Persuasion",
                "author": "Robert Cialdini",
                "category": "Psychology",
                "description": "This book is a straight-up classic for understanding why people say 'yes.' Robert Cialdini, a psych wizard, breaks down six universal principles of persuasion—like reciprocity and scarcity—that shape our decisions. Packed with real-world examples and sneaky insights, it’s a must-read for anyone looking to master the art of influence, whether you’re in sales, marketing, or just trying to win an argument. Absolute gold.",
                "image": "default_book.jpg"
            },
            {
                "id": 4,
                "title": "The Lean Startup",
                "author": "Eric Ries",
                "category": "Entrepreneurship",
                "description": "A total game-changer for anyone dreaming of launching a business. Eric Ries drops straight-up practical wisdom on building startups that don’t just survive but thrive. His big idea? Stop wasting time on perfect plans and start testing fast with the build-measure-learn loop. Packed with real-world examples and actionable steps, this book’s a must-read for entrepreneurs who want to move smart and stay lean while crushing it.",
                "image": "default_book.jpg"
            },
            {
                "id": 5,
                "title": "Scarcity Brain: Fix Your Craving Mindset and Rewire Your Habits to Thrive with Enough",
                "author": "Michael Easter",
                "category": "Science",
                "description": "This book dives deep into why we’re wired to crave more, starting with the neurotransmitter behind slot machine addiction. Michael Easter breaks down the science of our 'scarcity brain' and serves up practical hacks to rewire your habits. It’s a mind-blowing mix of neuroscience, real-life stories, and no-BS advice to help you ditch the endless chase and thrive with what you’ve got. A must for anyone stuck in the craving trap.",
                "image": "default_book.jpg"
            },
            {
                "id": 6,
                "title": "Way of the Wolf: Straight Line Selling",
                "author": "Jordan Belfort",
                "category": "Sales",
                "description": "Hands down the best sales book out there. Jordan Belfort, the real-deal Wolf of Wall Street, lays out his straight-line selling system with zero fluff. It’s like a masterclass in closing deals, packed with killer techniques to build trust, handle objections, and skyrocket your sales game. Whether you’re a rookie or a pro, this book’s a goldmine for mastering the art of persuasion.",
                "image": "default_book.jpg"
            },
            {
                "id": 7,
                "title": "Make It Stick: The Science of Successful Learning",
                "author": "Rosamund Stone Zander and Benjamin Zander",
                "category": "Personal Growth",
                "description": "If you want to learn smarter, this book’s your new best friend. Rosamund and Benjamin Zander unpack the science of how we actually retain knowledge, debunking old-school study myths along the way. With practical strategies like spaced repetition and real-world examples, it’s a no-nonsense guide to making learning stick for good. Perfect for students, pros, or anyone looking to level up their brain game.",
                "image": "default_book.jpg"
            },
            {
                "id": 8,
                "title": "The Outsiders: Eight Unconventional CEOs and Their Radically Rational Blueprint for Success",
                "author": "William N. Thorndike Jr.",
                "category": "Business",
                "description": "William Thorndike Jr. dives into the stories of eight CEOs who ignored the usual playbook and built insanely successful companies. From capital allocation to bold moves, it’s packed with insights you won’t find in typical business books. If you’re into smart, outside-the-box strategies for crushing it in business, this one’s a must-read.",
                "image": "default_book.jpg"
            },
            {
                "id": 9,
                "title": "Never Split the Difference",
                "author": "Chris Voss",
                "category": "Psychology",
                "description": "Chris Voss, a former FBI hostage negotiator, delivers a killer negotiation playbook. This book’s not about compromising—it’s about dominating deals and conversations with sharp psychological tactics. From mirroring to tactical empathy, Voss lays it out with real-life stories and practical tips you can use anywhere, from boardrooms to daily life. If you want to master getting what you want, this is your go-to. Pro tip: grab the audiobook—Voss’s voice nails the negotiation tonality.",                 
                "image": "default_book.jpg"
            },
            {
                "id": 10,
                "title": "How to Win Friends and Influence People",
                "author": "Dale Carnegie",
                "category": "Psychology",
                "description": "One of my all-time favorite books, period. Dale Carnegie’s classic is the ultimate guide to building relationships and winning people over. Packed with timeless advice like genuinely listening and making others feel valued, it’s a masterclass in human connection. Whether you’re networking, leading, or just trying to be a better human, this book’s practical wisdom will stick with you for life.",
                "image": "default_book.jpg"
            }
        ]
    
    return books

books = load_data()



def send_blog_signup_email(email, name):

    smtp_server = 'smtp.gmail.com'
    smtp_port = 587  # Use 465 for SSL
    smtp_username = 'julpal99@gmail.com'
    smtp_password = app.config.get('smtp_password', os.getenv('smtp_password'))
    sender_email = 'Julien <julpal99@gmail.com>'

    try:
         # Create the email
        msg = EmailMessage()
        msg['From'] = sender_email
        msg['To'] = "julpal1999@gmail.com"
        msg['Subject'] = f"{name} Just Signed Up for the Personal BLOG Newsletter!"

        text=f"""
Hi JP,

{name} just signed up with {email} to your Blog newsletter.
"""
        msg.set_content(text)
        print(f"Email message: {msg}")
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_username, smtp_password)
            print("SMTP connection successful!")
            server.send_message(msg)

        print(f"Email successfully sent to {email}")
    except Exception as e:
        print(f"Error sending email: {e}")
        raise



@app.route('/')
@app.route('/blog')
def blog():
    import requests
    import os
    form = SubscribeForm()

    query = """
    {
        posts {
            title
            id
            slug
            date
            tags
            coverImage {
                url
            }
            excerpt
            content {
                html
            }
            author {
                name
                picture {
                    url
                }
            }
        }
    }
    """

    endpoint = app.config.get('HYGRAPH_ENDPOINT', os.getenv('HYGRAPH_ENDPOINT'))
    token = app.config.get('HYGRAPH_PERMANENTAUTH_TOKEN', os.getenv('HYGRAPH_PERMANENTAUTH_TOKEN'))

    if not endpoint or not token:
        return "Missing API credentials", 500  # Fail early if env variables are missing

    headers = {'Authorization': f'Bearer {token}'}
    response = requests.post(endpoint, json={'query': query}, headers=headers)

    # Debugging: Check response
    print(response.status_code)
    print(response.text)

    if response.status_code != 200:
        return f"Error: {response.status_code}", 500

    response_data = response.json()

    # Ensure response contains 'data' and 'posts'
    if 'data' not in response_data or 'posts' not in response_data['data']:
        return "Invalid response from Hygraph", 500

    posts = response_data['data']['posts']
    # List of unique tags
    unique_tags = list(set(tag for post in posts for tag in post['tags']))
    print(f"Unique tags: {unique_tags}")  # Debugging: Print unique tags (unique_tags)

    page = request.args.get('page', 1, type=int)
    search_query = request.args.get('search', '')
    
    # Filter posts based on search query if provided
    filtered_posts = posts
    if search_query:
        filtered_posts = [post for post in posts if search_query.lower() in post['title'].lower() or 
                         search_query.lower() in post['subtitle'].lower()]
    
    category = request.args.get('category', 'All')
    if category != 'All':
        filtered_posts = [post for post in posts if category in post['tags']]

    # Pagination
    per_page = 5
    start_idx = (page - 1) * per_page
    end_idx = start_idx + per_page
    paginated_posts = filtered_posts[start_idx:end_idx]
    total_pages = (len(filtered_posts) + per_page - 1) // per_page

    if request.method == 'POST':
        email = form.email.data
        name = form.name.data
        return render_template('blog.html', title="Blog Look", form=form)
    
    return render_template('blog.html', 
                           posts=paginated_posts, 
                           unique_tags=unique_tags,
                           page=page, 
                           total_pages=total_pages, 
                           search_query=search_query, 
                           form=form,
                           title='Blog',
                           selected_category=category)

@app.route('/library')
def library():
    category = request.args.get('category', 'All')
    
    # Filter books by category if not 'All'
    filtered_books = books
    if category != 'All':
        filtered_books = [book for book in books if book['category'] == category]
    
    # Get unique categories for the filter buttons
    categories = ['All'] + list(set(book['category'] for book in books))
    
    return render_template('library.html', books=filtered_books, categories=categories, selected_category=category)

@app.route('/subscribe', methods=['POST'])
def subscribe():
    name = request.form.get('name')
    email = request.form.get('email')
    
    if not name or not email:
        flash('Please provide both name and email.')
        return redirect(request.referrer)
    
    try:
            send_blog_signup_email(email, name)
            print(f"Email successfully sent to {email}")
    except Exception as e:
            print(f"Error sending email: {e}")
    
    flash('Thank you for subscribing!')
    return redirect(request.referrer)

@app.route('/blog/<slug>')
def blog_post(slug):
    import requests
    import html
    import os
    form = SubscribeForm()

    query = f"""
    {{
        post(where: {{slug: "{slug}"}}) {{
            title
            slug
            tags
            id
            date
            coverImage {{
                url
            }}
            excerpt
            content {{
                html
            }}
            author {{
                name
                picture {{
                    url
                }}
            }}
        }}
    }}
    """

    endpoint = app.config.get('HYGRAPH_ENDPOINT', os.getenv('HYGRAPH_ENDPOINT'))
    token = app.config.get('HYGRAPH_PERMANENTAUTH_TOKEN', os.getenv('HYGRAPH_PERMANENTAUTH_TOKEN'))

    if not endpoint or not token:
        return "Missing API credentials", 500  # Fail early if env variables are missing

    headers = {'Authorization': f'Bearer {token}'}
    response = requests.post(endpoint, json={'query': query}, headers=headers)

    # Debugging: Check response
    # print(response.status_code)
    # print(response.text)

    if response.status_code != 200:
        return f"Error: {response.status_code}", 500

    response_data = response.json()

    # Ensure response contains 'data' and 'post'
    if 'data' not in response_data or 'post' not in response_data['data']:
        return "Post not found", 404

    post = response_data['data']['post']

    post['content']['html'] = html.unescape(post['content']['html'])

    print(post)

    if request.method == 'POST':
        email = form.email.data
        name = form.name.data
        last_name = form.last_name.data

        return render_template('blog_post.html', title=post['title'], post=post, form=form)

    return render_template('blog_post.html', title=post['title'], post=post, form=form)

if __name__ == '__main__':
    app.run(debug=True)
