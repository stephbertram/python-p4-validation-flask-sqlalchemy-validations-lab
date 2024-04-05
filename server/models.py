from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    @validates("name")
    def validate_name(self, _, name):
        if not name:
            raise ValueError("Name has to be present.")
        # filtering the results to only include rows where the name column matches the name variable that we passed as an argument
        if Author.query.filter_by(name=name).first():
            raise ValueError ("Name must be unique.")
        return name
    
    @validates("phone_number")
    def validate_phone_number(self, _, phone_number):
        if not isinstance(phone_number, str) or len(phone_number) != 10 or not phone_number.isdigit():
            raise ValueError('Phone numbers must be ten digits.')
        return phone_number
        

    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'

class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators  
    @validates("content")
    def validate_content(self, _, content):
        if len(content) < 250:
            raise ValueError("Post must be at least 250 characters long.")
        else:
            return content
        
    @validates("summary")
    def validate_summary(self, _, summary):
        if len(summary) > 250:
            raise ValueError("Post summary may be a maximum of 250 characters.")
        else:
            return summary
        
    # @validates('content', 'summary')
    # def validate_length(self, key, string):
    #     if key == 'content':
    #         if len(string) < 250:
    #             raise ValueError("Post content must be at least 250 characters long.")
    #     if key == 'summary':
    #         if len(string) > 250:
    #             raise ValueError("Summary must be less than 250 characters long.")
    #     return string
        
    @validates("category")
    def validate_category(self, _, category):
        if category not in ["Fiction", "Non-Fiction"]:
            raise ValueError("Category must be Fiction or Non-Fiction.")
        return category
    
    @validates("title")
    def validate_title(self, _, title):
        clickbait_words = ["Won't Believe", "Secret", "Top", "Guess"]
        # generator expression, "word in title" checks if current word ("word") is present in "title" string
        # any short circuits (stops iterating) as soon as it finds a "True" value
        if not any(word in title for word in clickbait_words):
            raise ValueError("Post title must contain one of the following words: 'Won't Believe', 'Secret', 'Top', 'Guess'.")
        return title


    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'
