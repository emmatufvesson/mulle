import json

from mulle.engine.headless_runner import ScriptedAction, load_script, run_headless_session


def test_scripted_actions_drive_first_turns():
    scripted = [
        ScriptedAction(player="Anna", action="discard", card_index=0),
        ScriptedAction(player="Anna", action="discard", card_index=0),
    ]
    result = run_headless_session(rounds=1, seed=3, scripted_actions=scripted)

    first_action = result.omgangen[0].rounds[0].actions[0]
    assert first_action[0] == "Anna"
    assert first_action[1].captured == []
    assert result.cumulative["Anna"] >= 0 and result.cumulative["Bo"] >= 0


def test_load_script_file(tmp_path):
    script_path = tmp_path / "script.json"
    script = [
        {"player": "Anna", "action": "discard", "card_index": 0},
        {"player": "Anna", "action": "auto"},
    ]
    script_path.write_text(json.dumps(script), encoding="utf-8")

    actions = load_script(script_path)
    assert isinstance(actions[0], ScriptedAction)

    result = run_headless_session(rounds=1, seed=4, scripted_actions=actions)
    anna_actions = [name for name, _ in result.omgangen[0].rounds[0].actions if name == "Anna"]
    assert anna_actions[0] == "Anna"
    assert len(result.omgangen[0].rounds) == 6
