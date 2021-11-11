from togglsgu.lib.lib import get_config

def test_get_config():
    config = get_config('test.yaml')
    expected = {
        'email': 'a',
        'workspace_id': 'b',
        'api_token': 'c',
        'sgu_username': 'd',
        'output_file_name': 'e'
        }
    assert config == expected
