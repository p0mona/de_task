from helpers import Exporter
import xml.etree.ElementTree as et
import os
import pytest
import json

@pytest.fixture()
def test_data():
    data = {
        'q1': {
            'task': "SELECT * FROM users WHERE id < 50",
            'results': [{'id': 12, 'name': "Kate"}, {'id': 46, 'name': "Maciej"}]
        },
        'q2': {
            'task': "SELECT COUNT(*) FROM users",
            'results': [{'count': 78}]
        }
    }
    return data

@pytest.fixture()
def test_exporter(test_data):
    return Exporter(test_data, str('query_results'))

@pytest.fixture(autouse=True)
def cleanup_files():
    for ext in ['.json', '.xml']:
        if os.path.exists('query_results' + ext):
            os.remove("query_results" + ext)

class TestExporter():
    def test_export(self, test_exporter):
        test_exporter.export_json()

        assert os.path.exists('query_results.json')

        if os.path.exists('query_results.json'):
            os.remove("query_results.json")

        test_exporter.export_xml()

        assert os.path.exists('query_results.xml')

    def test_results_of_export_json(self, test_exporter):
        test_exporter.export_json()

        with open('query_results.json', 'r') as f:
            data = json.load(f)

        assert data['q1']['results'][0]['id'] == 12
        assert data['q1']['results'][1]['name'] == 'Maciej'
        assert data['q2']['results'][0]['count'] == 78

    def test_results_of_export_xml(self, test_exporter):
        test_exporter.export_xml()
        tree = et.parse('query_results.xml')
        root = tree.getroot()

        query_elem_1 = root.find("query[@name='q1']")
        results_el_1 = query_elem_1.find('results')

        if results_el_1 is not None:
            rows = results_el_1.findall('row')

            assert rows[0].find('id').text == '12'
            assert rows[0].find('name').text == 'Kate'
        
        query_elem_2 = root.find("query[@name='q2']")
        results_el_2 = query_elem_2.find('results')
            
        if results_el_2 is not None:
            rows = results_el_2.findall('row')
            assert rows[0].find('count').text == '78'