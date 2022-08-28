from skills import level_for_xp


def test_level_for_xp():
    assert level_for_xp(0) == 1
    assert level_for_xp(82) == 1
    assert level_for_xp(83) == 2
    assert level_for_xp(85) == 2
    assert level_for_xp(188884000) == 125
    assert level_for_xp(199000000) == 126