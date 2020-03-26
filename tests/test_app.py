from .context import coronabot


def test_app(capsys, example_fixture):
    # pylint: disable=W0612,W0613
    coronabot.CoronaBot.run()
    captured = capsys.readouterr()
    print(captured.out)
    assert "<code>|       Location" in captured.out
