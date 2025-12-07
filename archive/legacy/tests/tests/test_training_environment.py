from mulle.engine.training_environment import TrainingEnvironment


def test_reset_sets_up_single_round():
    env = TrainingEnvironment(seed=1)
    obs = env.reset()

    assert len(obs.hand) == 8
    assert obs.opponent_cards == 8
    # A non-empty list means the environment can generate playable actions
    assert obs.legal_actions


def test_step_advances_state_and_returns_reward():
    env = TrainingEnvironment(seed=2)
    obs = env.reset()
    starting_cards = len(obs.hand)

    action = obs.legal_actions[0] if obs.legal_actions else None
    obs, reward, done, info = env.step(action)

    assert len(obs.hand) == starting_cards - 1
    assert isinstance(reward, float)
    assert not done
    assert "player_action" in info


def test_episode_runs_to_completion():
    env = TrainingEnvironment(seed=3)
    obs = env.reset()
    done = False
    steps = 0

    while not done:
        action = obs.legal_actions[0] if obs.legal_actions else None
        obs, reward, done, info = env.step(action)
        steps += 1
        # Hard upper bound to avoid infinite loops in case of regression
        assert steps < 20

    assert done
    assert "scores" in info
