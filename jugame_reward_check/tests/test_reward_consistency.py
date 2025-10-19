from jugame_reward_check.scripts.reward_compare import compare_rewards_for_uid

def test_u200101_ok():
    ok, msg = compare_rewards_for_uid(200101, "0xF1A7...", 120)
    assert ok, msg

def test_u200102_ok():
    ok, msg = compare_rewards_for_uid(200102, "0x2B44...", 60)
    assert ok, msg

def test_u200103_ok():
    ok, msg = compare_rewards_for_uid(200103, "0xE8e1...", 90)
    assert ok, msg
