import os
from flask import Flask, render_template, request, redirect, url_for, session, jsonify, send_file
from models import db, Section, FormTemplate, FormResponse
from datetime import datetime
from exports import generate_exports
import zipfile
import io

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'csakb-secret-key-2025'

db.init_app(app)

# Création des dossiers si nécessaires
if not os.path.exists('exports'):
    os.makedirs('exports')

@app.route('/')
def index():
    sections = Section.query.all()
    return render_template('index.html', sections=sections)

@app.route('/select_section', methods=['POST'])
def select_section():
    section_id = request.form.get('section_id')
    if section_id:
        section = Section.query.get(section_id)
        if section:
            session['section_id'] = section_id
            session['section_name'] = section.name
            return redirect(url_for('dashboard'))
    return redirect(url_for('index'))

@app.route('/dashboard')
def dashboard():
    if 'section_id' not in session:
        return redirect(url_for('index'))
    section = Section.query.get(session['section_id'])
    return render_template('dashboard.html', section=section)

@app.route('/save_response', methods=['POST'])
def save_response():
    if 'section_id' not in session:
        return jsonify({'success': False, 'message': 'Session expirée'}), 401

    payload = request.get_json()
    template_id = payload.get('template_id')
    data = payload.get('data')

    response = FormResponse.query.filter_by(section_id=session['section_id'], template_id=template_id).first()
    if not response:
        response = FormResponse(section_id=session['section_id'], template_id=template_id, data=data)
        db.session.add(response)
    else:
        response.data = data
        response.last_updated = datetime.utcnow()

    db.session.commit()
    return jsonify({'success': True})

@app.route('/export/xlsx')
def export_xlsx():
    if 'section_id' not in session: return redirect(url_for('index'))
    xlsx_path, _ = generate_exports(session['section_id'])
    if not xlsx_path: return "Erreur lors de la génération", 500
    return send_file(xlsx_path, as_attachment=True)

@app.route('/export/pdf')
def export_pdf():
    if 'section_id' not in session: return redirect(url_for('index'))
    _, pdf_path = generate_exports(session['section_id'])
    if not pdf_path: return "Erreur lors de la génération", 500
    return send_file(pdf_path, as_attachment=True)

@app.route('/form/<int:theme_id>')
def form_view(theme_id):
    if 'section_id' not in session:
        return redirect(url_for('index'))

    section_id = session['section_id']
    template = FormTemplate.query.filter_by(theme=theme_id, is_active=True).order_by(FormTemplate.version.desc()).first()

    if not template:
        return "Formulaire non configuré", 404

    response = FormResponse.query.filter_by(section_id=section_id, template_id=template.id).first()
    data = response.data if response else {}

    return render_template('form.html', theme_id=theme_id, template=template, data=data)

# Auth admin simple
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        password = request.form.get('password')
        if password == 'admin123': # Mot de passe en dur
            session['is_admin'] = True
            return redirect(url_for('admin_dashboard'))
    return render_template('admin_login.html')

@app.route('/admin')
def admin_dashboard():
    if not session.get('is_admin'):
        return redirect(url_for('admin_login'))
    return render_template('admin_dashboard.html')

@app.route('/admin/sections', methods=['GET', 'POST'])
def admin_sections():
    if not session.get('is_admin'): return redirect(url_for('admin_login'))

    if request.method == 'POST':
        name = request.form.get('name')
        if name:
            db.session.add(Section(name=name))
            db.session.commit()

    sections = Section.query.all()
    return render_template('admin_sections.html', sections=sections)

@app.route('/admin/sections/delete/<int:id>')
def delete_section(id):
    if not session.get('is_admin'): return redirect(url_for('admin_login'))
    section = Section.query.get(id)
    if section:
        db.session.delete(section)
        db.session.commit()
    return redirect(url_for('admin_sections'))

@app.route('/admin/forms')
def admin_forms():
    if not session.get('is_admin'): return redirect(url_for('admin_login'))
    templates = FormTemplate.query.filter_by(is_active=True).all()
    return render_template('admin_forms.html', templates=templates)

@app.route('/admin/edit_form/<int:theme_id>', methods=['GET', 'POST'])
def admin_edit_form(theme_id):
    if not session.get('is_admin'): return redirect(url_for('admin_login'))

    current_template = FormTemplate.query.filter_by(theme=theme_id, is_active=True).first()

    if request.method == 'POST':
        # Création d'une nouvelle version
        new_structure = current_template.structure.copy()

        # Mise à jour des labels (logique simplifiée)
        if new_structure['type'] == 'budget':
            for g_idx, group in enumerate(new_structure['groups']):
                for f_idx, field in enumerate(group['fields']):
                    new_label = request.form.get(f"label_{field['id']}")
                    if new_label:
                        new_structure['groups'][g_idx]['fields'][f_idx]['label'] = new_label

        elif new_structure['type'] == 'fixed_table':
            for r_idx, row in enumerate(new_structure['rows']):
                new_label = request.form.get(f"label_{row['id']}")
                if new_label:
                    new_structure['rows'][r_idx]['label'] = new_label

        elif new_structure['type'] == 'dynamic_table':
            for c_idx, col in enumerate(new_structure['cols']):
                new_label = request.form.get(f"label_{col['id']}")
                if new_label:
                    new_structure['cols'][c_idx]['label'] = new_label

        # Désactiver l'ancienne version
        current_template.is_active = False

        # Créer la nouvelle
        new_template = FormTemplate(
            theme=theme_id,
            version=current_template.version + 1,
            structure=new_structure,
            is_active=True
        )
        db.session.add(new_template)
        db.session.commit()
        return redirect(url_for('admin_forms'))

    return render_template('admin_edit_form.html', template=current_template)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5000)
