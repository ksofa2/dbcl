import pytest

from dbcl.command_line import process_comand, _command_prefix, NoSuchTableError


@pytest.fixture(autouse=True)
def clear_env(monkeypatch):
    monkeypatch.delenv('DATABASE_URL', raising=False)


@pytest.mark.parametrize('command', (
    '%s%s' % (_command_prefix, cmd) for cmd in
    ('comand_nope', 'command_wrong')))
def test_bad_command(command, capsys):

    process_comand(command, None, None)

    out, err = capsys.readouterr()
    assert out.startswith('Bad command')


info_too_many = ['%s%s' % (_command_prefix, cmd) for cmd in
                 ['info too many', 'info way too many args']]


def test_info_no_args(mocker, capsys):
    mock_args = mocker.MagicMock()
    mock_args.database_url = 'test_db_url'
    mock_metadata = mocker.patch('dbcl.command_line.MetaData')

    process_comand('%sinfo' % _command_prefix, None, mock_args)

    assert mock_metadata.return_value.reflect.called
    out, err = capsys.readouterr()
    assert 'Database URL' in out
    assert 'Tables' in out


def test_info_one_arg(mocker, capsys):
    mock_args = mocker.MagicMock()
    mock_args.database_url = 'test_db_url'
    mock_table = mocker.patch('dbcl.command_line.Table')
    mock_print_data = mocker.patch('dbcl.command_line.print_data')

    process_comand('%sinfo table_name' % _command_prefix, None, mock_args)

    assert mock_table.called
    assert mock_print_data.called


def test_info_missing_table(mocker, capsys):
    mock_args = mocker.MagicMock()
    mock_args.database_url = 'test_db_url'
    mock_table = mocker.patch('dbcl.command_line.Table',
                              side_effect=NoSuchTableError)
    mock_print_data = mocker.patch('dbcl.command_line.print_data')

    process_comand('%sinfo table_name' % _command_prefix, None, mock_args)

    assert mock_table.called
    assert not mock_print_data.called
    out, err = capsys.readouterr()
    assert out.startswith('No such table')


@pytest.mark.parametrize('command', (
    '%s%s' % (_command_prefix, cmd) for cmd in
    ('info too many', 'info way too many args')))
def test_info_too_many_args(command, capsys):

    process_comand(command, None, None)

    out, err = capsys.readouterr()
    assert out.startswith('usage: ')


#
# def test_with_url_on_command_line(mocker):
#     mock_prompt = mocker.patch('dbcl.command_line.prompt')
#     mock_prompt.return_value = 'test_url_from_input'
#
#     args = get_args(['test_url_from_command_line'])
#
#     assert not mock_prompt.called
#     assert args.database_url == 'test_url_from_command_line'
#
#
# def test_no_args_with_input(mocker):
#     mock_prompt = mocker.patch('dbcl.command_line.prompt')
#     mock_prompt.return_value = 'test_url_from_input'
#
#     args = get_args([])
#
#     mock_prompt.assert_called_with('Connect to []: ')
#     assert args.database_url == 'test_url_from_input'
#
#
# @pytest.mark.parametrize('exc,return_code', (
#     (KeyboardInterrupt, 1),
#     (EOFError, 0),
# ))
# def test_no_args_with_user_cancel(exc, return_code, mocker):
#     mock_prompt = mocker.patch('dbcl.command_line.prompt',
#                                side_effect=exc)
#     with pytest.raises(SystemExit) as excinfo:
#         get_args([])
#
#     assert excinfo.value.code == return_code
#     assert mock_prompt.called
#
#
# @pytest.mark.parametrize('user_input,url', (
#     ('', 'test_url_from_env'),
#     ('test_url_from_input', 'test_url_from_input'),
# ))
# def test_no_args_with_url_in_env(user_input, url, mocker, monkeypatch):
#     monkeypatch.setenv('DATABASE_URL', 'test_url_from_env')
#     mock_prompt = mocker.patch('dbcl.command_line.prompt')
#     mock_prompt.return_value = user_input
#
#     args = get_args([])
#
#     mock_prompt.assert_called_with('Connect to [test_url_from_env]: ')
#     assert args.database_url == url
#
#
# def test_with_url_in_arg_and_env(mocker, monkeypatch):
#     monkeypatch.setenv('DATABASE_URL', 'test_url_from_env')
#     mock_prompt = mocker.patch('dbcl.command_line.prompt')
#     mock_prompt.return_value = 'test_url_from_input'
#
#     args = get_args(['test_url_from_command_line'])
#
#     assert not mock_prompt.called
#     assert args.database_url == 'test_url_from_command_line'
