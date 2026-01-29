import pytest
from app import app, db
from models import Section, FormTemplate, FormResponse

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.app_context():
        db.drop_all()
        db.create_all()
        # Setup initial data
        s1 = Section(name="Test Section")
        db.session.add(s1)
        t1 = FormTemplate(theme=1, version=1, structure={"type": "budget", "groups": []}, is_active=True)
        db.session.add(t1)
        db.session.commit()

    with app.test_client() as client:
        yield client

def test_index(client):
    rv = client.get('/')
    assert b"Bienvenue" in rv.data
    assert b"Test Section" in rv.data

def test_select_section(client):
    rv = client.post('/select_section', data={'section_id': '1'}, follow_redirects=True)
    assert b"Tableau de bord - Test Section" in rv.data

def test_save_response(client):
    with client.session_transaction() as sess:
        sess['section_id'] = 1

    rv = client.post('/save_response', json={
        'template_id': 1,
        'data': {'field_1': 'value_1'}
    })
    assert rv.get_json()['success'] is True

    with app.app_context():
        resp = FormResponse.query.filter_by(section_id=1, template_id=1).first()
        assert resp.data['field_1'] == 'value_1'

def test_admin_login(client):
    rv = client.post('/admin/login', data={'password': 'wrong'}, follow_redirects=True)
    assert b"Acc\xc3\xa8s Admin" in rv.data # "Accès Admin" encoding

    rv = client.post('/admin/login', data={'password': 'admin123'}, follow_redirects=True)
    assert b"Tableau de bord Administrateur" in rv.data

def test_export(client):
    with client.session_transaction() as sess:
        sess['section_id'] = 1
        sess['section_name'] = "Test Section"

    # Save some data first
    client.post('/save_response', json={
        'template_id': 1,
        'data': {'fed': 'FFT'}
    })

    rv = client.get('/export/xlsx')
    assert rv.status_code == 200
    assert rv.mimetype == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'

    rv = client.get('/export/pdf')
    assert rv.status_code == 200
    assert rv.mimetype == 'application/pdf'
