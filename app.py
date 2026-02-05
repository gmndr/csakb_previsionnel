import os
from flask import Flask, render_template, request, redirect, url_for, session, jsonify, send_file
from datetime import datetime
from exports import generate_exports
import storage

app = Flask(__name__)
app.secret_key = 'csakb-secret-key-2025'

# Initialisation du stockage
storage.init_storage()

# Création du dossier d'exports si nécessaire
if not os.path.exists('exports'):
    os.makedirs('exports')

@app.route('/')
def index():
    sections = storage.get_sections()
    return render_template('index.html', sections=sections)

@app.route('/select_section', methods=['POST'])
def select_section():
    section_name = request.form.get('section_name')
    if section_name:
        session['section_name'] = section_name
        return redirect(url_for('dashboard'))
    return redirect(url_for('index'))

@app.route('/dashboard')
def dashboard():
    if 'section_name' not in session:
        return redirect(url_for('index'))

    section_name = session['section_name']
    templates = []
    responses = {}

    for theme_id in range(1, 5):
        template = storage.get_template(theme_id)
        if template:
            templates.append(template)
            resp = storage.get_response(section_name, theme_id)
            if resp and resp.get('template_version') == template['version']:
                responses[theme_id] = resp['data']
            else:
                responses[theme_id] = {}

    return render_template('dashboard.html',
                           section_name=section_name,
                           templates=templates,
                           responses=responses)

@app.route('/save_all_responses', methods=['POST'])
def save_all_responses():
    if 'section_name' not in session:
        return jsonify({'success': False, 'message': 'Session expirée'}), 401

    payload = request.get_json()
    section_name = session['section_name']

    for theme_data in payload.get('themes', []):
        theme_id = int(theme_data.get('theme_id'))
        template_version = int(theme_data.get('template_version'))
        data = theme_data.get('data')
        storage.save_response(section_name, theme_id, None, template_version, data)

    return jsonify({'success': True})

@app.route('/save_response', methods=['POST'])
def save_response():
    if 'section_name' not in session:
        return jsonify({'success': False, 'message': 'Session expirée'}), 401

    payload = request.get_json()
    theme_id = int(payload.get('theme_id'))
    template_version = int(payload.get('template_version'))
    data = payload.get('data')

    storage.save_response(session['section_name'], theme_id, None, template_version, data)

    return jsonify({'success': True})

@app.route('/export/xlsx')
def export_xlsx():
    if 'section_name' not in session: return redirect(url_for('index'))
    xlsx_path, _ = generate_exports(session['section_name'])
    if not xlsx_path: return "Erreur lors de la génération", 500
    return send_file(xlsx_path, as_attachment=True)

@app.route('/export/pdf')
def export_pdf():
    if 'section_name' not in session: return redirect(url_for('index'))
    _, pdf_path = generate_exports(session['section_name'])
    if not pdf_path: return "Erreur lors de la génération", 500
    return send_file(pdf_path, as_attachment=True)

@app.route('/form/<int:theme_id>')
def form_view(theme_id):
    # Les formulaires sont maintenant tous sur le dashboard à la suite
    return redirect(url_for('dashboard'))

# Auth admin simple
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        password = request.form.get('password')
        if password == 'admin123':
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
            storage.add_section(name)

    sections = storage.get_sections()
    return render_template('admin_sections.html', sections=sections)

@app.route('/admin/sections/delete/<path:name>')
def delete_section(name):
    if not session.get('is_admin'): return redirect(url_for('admin_login'))
    storage.delete_section(name)
    return redirect(url_for('admin_sections'))

@app.route('/admin/forms')
def admin_forms():
    if not session.get('is_admin'): return redirect(url_for('admin_login'))
    templates = storage.get_all_active_templates()
    return render_template('admin_forms.html', templates=templates)

@app.route('/admin/edit_form/<int:theme_id>', methods=['GET', 'POST'])
def admin_edit_form(theme_id):
    if not session.get('is_admin'): return redirect(url_for('admin_login'))

    current_template = storage.get_template(theme_id)

    if request.method == 'POST':
        new_structure = current_template['structure'].copy()

        if new_structure['type'] == 'budget':
            for g_idx, group in enumerate(new_structure['groups']):
                for f_idx, field in enumerate(group['fields']):
                    new_label = request.form.get(f"label_{field['id']}")
                    if new_label:
                        new_structure['groups'][g_idx]['fields'][f_idx]['label'] = new_label

                    new_mult = request.form.get(f"mult_{field['id']}")
                    if new_mult is not None and 'multiplier' in field:
                        new_structure['groups'][g_idx]['fields'][f_idx]['multiplier'] = float(new_mult)

                    new_formula = request.form.get(f"formula_{field['id']}")
                    if new_formula is not None and 'formula' in field:
                        new_structure['groups'][g_idx]['fields'][f_idx]['formula'] = new_formula

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

        storage.save_template_version(theme_id, new_structure)
        return redirect(url_for('admin_forms'))

    return render_template('admin_edit_form.html', template=current_template)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
