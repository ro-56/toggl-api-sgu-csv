from togglsgu.lib import lib


def test_get_config():
    config = lib.get_config('docs/test.yaml')
    expected = {
            'email': 'email@mail.com',
            'workspace_id': 123456789,
            'api_token': 'LoremIpsumDolorSitAmetConsecteturAdipiscingElit',
            'sgu_username': 'LoremIpsum',
            'output_file_name': 'output.csv'
        }
    assert config == expected
    return None
