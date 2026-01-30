import pytest
import os
import shutil
import storage
from app import app

@pytest.fixture
def client():
    # Setup temporary data directory for tests
    test_data_dir = 'data_test'
    app.config['TESTING'] = True
    storage.DATA_DIR = test_data_dir
    storage.SECTIONS_FILE = os.path.join(test_data_dir, 'sections.json')
    storage.TEMPLATES_DIR = os.path.join(test_data_dir, 'templates')
    storage.RESPONSES_DIR = os.path.join(test_data_dir, 'responses')

    if os.path.exists(test_data_dir):
        shutil.rmtree(test_data_dir)
    storage.init_storage()

    # Setup initial data
    storage.add_section("Test Section")
    storage.save_template_version(1, {"type": "budget", "groups": []}, version=1)

    with app.test_client() as client:
        yield client

    # Teardown
    if os.path.exists(test_data_dir):
        shutil.rmtree(test_data_dir)

def test_index(client):
    rv = client.get('/')
    assert b"Bienvenue" in rv.data
    assert b"Test Section" in rv.data

def test_select_section(client):
    rv = client.post('/select_section', data={'section_name': 'Test Section'}, follow_redirects=True)
    assert b"Tableau de bord - Test Section" in rv.data

def test_save_response(client):
    with client.session_transaction() as sess:
        sess['section_name'] = "Test Section"

    rv = client.post('/save_response', json={
        'theme_id': 1,
        'template_version': 1,
        'data': {'field_1': 'value_1'}
    })
    assert rv.get_json()['success'] is True

    resp = storage.get_response("Test Section", 1)
    assert resp['data']['field_1'] == 'value_1'

def test_admin_login(client):
    rv = client.post('/admin/login', data={'password': 'wrong'}, follow_redirects=True)
    assert b"Acc\xc3\xa8s Admin" in rv.data

    rv = client.post('/admin/login', data={'password': 'admin123'}, follow_redirects=True)
    assert b"Tableau de bord Administrateur" in rv.data

def test_export(client):
    with client.session_transaction() as sess:
        sess['section_name'] = "Test Section"

    # Save some data first
    client.post('/save_response', json={
        'theme_id': 1,
        'template_version': 1,
        'data': {'fed': 'FFT'}
    })

    rv = client.get('/export/xlsx')
    assert rv.status_code == 200
    assert rv.mimetype == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'

    rv = client.get('/export/pdf')
    assert rv.status_code == 200
    assert rv.mimetype == 'application/pdf'
