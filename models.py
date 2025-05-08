# models.py
# In a real application, you might use SQLAlchemy or another ORM
# This file is mostly for illustrating the data structure

class BlogPost:
    def __init__(self, id, title, subtitle, date, content, upvotes=0, comments=None):
        self.id = id
        self.title = title
        self.subtitle = subtitle
        self.date = date
        self.content = content
        self.upvotes = upvotes
        self.comments = comments or []
        
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'subtitle': self.subtitle,
            'date': self.date,
            'content': self.content,
            'upvotes': self.upvotes,
            'comments': [comment.to_dict() for comment in self.comments]
        }

class Comment:
    def __init__(self, id, text, author, upvotes=0, replies=None):
        self.id = id
        self.text = text
        self.author = author
        self.upvotes = upvotes
        self.replies = replies or []
        
    def to_dict(self):
        return {
            'id': self.id,
            'text': self.text,
            'author': self.author,
            'upvotes': self.upvotes,
            'replies': [reply.to_dict() for reply in self.replies]
        }

class Book:
    def __init__(self, id, title, author, category, description, image=None):
        self.id = id
        self.title = title
        self.author = author
        self.category = category
        self.description = description
        self.image = image
        
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'author': self.author,
            'category': self.category,
            'description': self.description,
            'image': self.image
        }