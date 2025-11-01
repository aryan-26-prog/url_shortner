from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class ShortURL(db.Model):
    __tablename__ = 'short_urls'
    id = db.Column(db.Integer, primary_key=True)
    short_id = db.Column(db.String(32), unique=True, index=True, nullable=False)
    original_url = db.Column(db.Text, nullable=False)
    custom_alias = db.Column(db.String(100), unique=True, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    click_count = db.Column(db.Integer, default=0)

    clicks = db.relationship('Click', backref='shorturl', cascade="all, delete-orphan")

    def display_id(self):
        return self.custom_alias if self.custom_alias else self.short_id

class Click(db.Model):
    __tablename__ = 'clicks'
    id = db.Column(db.Integer, primary_key=True)
    short_url_id = db.Column(db.Integer, db.ForeignKey('short_urls.id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    ip = db.Column(db.String(100))
    user_agent = db.Column(db.Text)
    referrer = db.Column(db.Text)
