from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

db = SQLAlchemy()

class AnalysisJob(db.Model):
    """Model for storing repository analysis jobs"""
    __tablename__ = 'analysis_jobs'
    
    id = db.Column(db.Integer, primary_key=True)
    repo_url = db.Column(db.String(500), nullable=False)
    status = db.Column(db.String(50), default='pending')  # pending, processing, completed, failed
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    result = db.Column(db.Text)  # JSON string containing the generated documentation
    error_message = db.Column(db.Text)
    
    def __repr__(self):
        return f'<AnalysisJob {self.id}: {self.repo_url}>'
    
    def to_dict(self):
        """Convert the job to a dictionary"""
        return {
            'id': self.id,
            'repo_url': self.repo_url,
            'status': self.status,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'result': json.loads(self.result) if self.result else None,
            'error_message': self.error_message
        }

class RepositoryCache(db.Model):
    """Model for caching repository analysis results"""
    __tablename__ = 'repository_cache'
    
    id = db.Column(db.Integer, primary_key=True)
    repo_url = db.Column(db.String(500), unique=True, nullable=False)
    repo_hash = db.Column(db.String(64), nullable=False)  # Git commit hash
    analysis_data = db.Column(db.Text)  # JSON string containing cached analysis
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    expires_at = db.Column(db.DateTime)
    
    def __repr__(self):
        return f'<RepositoryCache {self.repo_url}>'

class UserFeedback(db.Model):
    """Model for storing user feedback on generated documentation"""
    __tablename__ = 'user_feedback'
    
    id = db.Column(db.Integer, primary_key=True)
    job_id = db.Column(db.Integer, db.ForeignKey('analysis_jobs.id'), nullable=False)
    rating = db.Column(db.Integer)  # 1-5 star rating
    feedback_text = db.Column(db.Text)
    improvement_suggestions = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    job = db.relationship('AnalysisJob', backref=db.backref('feedback', lazy=True))
    
    def __repr__(self):
        return f'<UserFeedback {self.id}: Rating {self.rating}>'
