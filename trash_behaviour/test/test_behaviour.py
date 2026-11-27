"""Smoke test: the approach command on the cases that matter."""

from trash_behaviour.approach_node import command

P = {"search_turn": 0.3, "k_turn": 1.0, "k_drive": 0.5, "max_drive": 0.1, "stop_dist": 0.3, "safety_dist": 0.2}


def test_search_approach_stop():
    assert command(None, 5.0, P) == (0.0, 0.3)  # no target: turn on the spot
    lin, ang = command((0.2, 1.0), 5.0, P)  # target ahead, a bit to the right
    assert lin == 0.1 and ang < 0
    assert command((0.0, 1.0), 0.1, P)[0] == 0.0  # obstacle: no forward motion
    assert command((0.0, 0.25), 5.0, P)[0] == 0.0  # arrived
