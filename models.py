from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Section(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)

class FormTemplate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    theme = db.Column(db.Integer, nullable=False) # 1: Budget, 2: Bureau, 3: Formation, 4: Salariés
    version = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    # structure stores the list of fields/rows for the form
    structure = db.Column(db.JSON, nullable=False)

class FormResponse(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    section_id = db.Column(db.Integer, db.ForeignKey('section.id'), nullable=False)
    template_id = db.Column(db.Integer, db.ForeignKey('form_template.id'), nullable=False)
    # data stores { field_id: value }
    data = db.Column(db.JSON, nullable=False)
    last_updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    section = db.relationship('Section', backref='responses')
    template = db.relationship('FormTemplate', backref='responses')
