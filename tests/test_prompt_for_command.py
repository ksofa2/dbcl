from dbcl.command_line import prompt_for_command


def test_prompt(mocker):
    mock_prompt = mocker.patch('dbcl.command_line.prompt')

    prompt_for_command(None)

    assert mock_prompt.called
