import json
import os.path

import models
import project
import pytz
from project import format_time


def test_format_time():
    timezone = pytz.timezone('US/Pacific')
    assert format_time(timezone, 2022, month=8, day=4, hour=10) == '2022-08-04T17:00:00.000Z'
    assert format_time(pytz.utc, 2022, month=8, day=4, hour=10) == '2022-08-04T10:00:00.000Z'


def test_get_xp_percentages():
    player_with_gains = get_test_data()
    xp_percentages = project.get_xp_percentages(player_with_gains)
    print(xp_percentages)
    assert xp_percentages['Overall']['Player1'] == 0
    assert xp_percentages['Overall']['Player2'] == 25
    assert xp_percentages['Overall']['Player3'] == 75


def test_get_stats():
    player_with_gains = get_test_data()
    stats = project.get_stats(player_with_gains)
    print(stats)
    assert stats['Overall']['Player1'] == 2
    assert stats['Overall']['Player2'] == 1
    assert stats['Overall']['Player3'] == 0


def get_test_data():
    p1 = models.Player('Player1', 'Guthix')
    p2 = models.Player('Player2', 'Guthix')
    p3 = models.Player('Player3', 'Saradomin')

    with open(os.path.join('test_files', 'p1.json')) as f:
        json1 = f.read()
    with open(os.path.join('test_files', 'p2.json')) as f:
        json2 = f.read()
    with open(os.path.join('test_files', 'p3.json')) as f:
        json3 = f.read()

    pg1 = models.PlayerGains(p1.name, '2022-08-04T17:00:00.000Z', '2022-08-23T17:00:00.000Z')
    pg2 = models.PlayerGains(p2.name, '2022-08-04T17:00:00.000Z', '2022-08-23T17:00:00.000Z')
    pg3 = models.PlayerGains(p3.name, '2022-08-04T17:00:00.000Z', '2022-08-23T17:00:00.000Z')

    pg1.data = json.loads(json1)
    pg2.data = json.loads(json2)
    pg3.data = json.loads(json3)

    player_with_gains = [
        (p1, pg1),
        (p2, pg2),
        (p3, pg3)
    ]

    return player_with_gains
