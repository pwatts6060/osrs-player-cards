import os.path
from datetime import datetime

import pytz
from PIL import Image

import models
import skills
from bosses import bosses
from card import Card


def get_stats(player_with_gains):
    stats = dict()
    for skill in skills.skills_tuple:
        player_xps = []
        for pwg in player_with_gains:
            xp = pwg[1].data[skills.key_for(skill)]['experience']['gained']
            player_xps.append((pwg[0].name, xp))
        player_xps.sort(key=lambda x: x[1], reverse=True)
        tied = False
        tied_rank = 1
        stats[skill] = dict()
        for i, boss_kc in enumerate(player_xps):
            if i + 1 >= len(player_xps):
                stats[skill][boss_kc[0]] = tied_rank if tied else i
                break
            next_player_xp = player_xps[i + 1]
            if boss_kc[1] != next_player_xp[1]:
                tied_rank = i + 1
                tied = False
            else:
                tied = True
            stats[skill][boss_kc[0]] = tied_rank if tied else i
    for boss in bosses:
        boss_kcs = []
        for pwg in player_with_gains:
            xp = pwg[1].data[boss.first_key][boss.second_key]['gained']
            boss_kcs.append((pwg[0].name, xp))
        boss_kcs.sort(key=lambda x: x[1], reverse=True)
        tied = False
        tied_rank = 1
        stats[boss.first_key] = dict()
        for i, boss_kc in enumerate(boss_kcs):
            if i + 1 >= len(boss_kcs):
                stats[boss.first_key][boss_kc[0]] = tied_rank if tied else i
                break
            next_player_xp = boss_kcs[i + 1]
            if boss_kc[1] != next_player_xp[1]:
                tied_rank = i + 1
                tied = False
            else:
                tied = True
            stats[boss.first_key][boss_kc[0]] = tied_rank if tied else i
    return stats


def get_xp_percentages(player_with_gains):
    xp_percentages = dict()
    for skill in skills.skills_tuple:
        total_xp = 0
        xp_percentages[skill] = dict()
        for pwg in player_with_gains:
            xp = pwg[1].data[skills.key_for(skill)]['experience']['gained']
            total_xp += xp
        for pwg in player_with_gains:
            xp = pwg[1].data[skills.key_for(skill)]['experience']['gained']
            xp_percentages[skill][pwg[0].name] = 100 * xp / total_xp
    for boss in bosses:
        total_kc = 0
        xp_percentages[boss.first_key] = dict()
        for pwg in player_with_gains:
            kc = pwg[1].data[boss.first_key][boss.second_key]['gained']
            total_kc += kc
        for pwg in player_with_gains:
            kc = pwg[1].data[boss.first_key][boss.second_key]['gained']
            xp_percentages[boss.first_key][pwg[0].name] = 100 * kc / total_kc if total_kc else 0
    return xp_percentages


def format_time(timezone, year, month, day, hour):
    dt = timezone.localize(datetime(year, month, day, hour))
    dt = pytz.utc.normalize(dt)
    return dt.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'


def main():
    timezone = pytz.timezone('US/Pacific')
    start = format_time(timezone, 2022, month=8, day=4, hour=10)
    end = format_time(timezone, 2022, month=8, day=22, hour=10)

    guthix = Image.open(os.path.join("images", "Guthix_symbol.png"))
    saradomin = Image.open(os.path.join("images", "Saradomin_symbol.png"))

    id = 14542
    comp = models.Competition(id)
    comp.load_file()
    if not comp.players:
        comp = models.Competition(id)
        comp.update()
        comp.save_file()
    player_with_gains = []
    player_with_gains_guthix = []
    player_with_gains_sara = []
    for player in comp.players.values():
        player_gains = models.PlayerGains(player.name, start, end)
        player_gains.load_file()
        if not player_gains.data:
            player_gains.update()
            player_gains.save_file()
        player_with_gains.append((player, player_gains))
        if player.team == "Guthix":
            player_with_gains_guthix.append((player, player_gains))
        else:
            player_with_gains_sara.append((player, player_gains))

    stats_all = get_stats(player_with_gains)
    stats_guthix = get_stats(player_with_gains_guthix)
    stats_sara = get_stats(player_with_gains_sara)

    xp_percentages_all = get_xp_percentages(player_with_gains)
    xp_percentages_guthix = get_xp_percentages(player_with_gains_guthix)
    xp_percentages_sara = get_xp_percentages(player_with_gains_sara)

    for pwg in player_with_gains:
        player = pwg[0]
        player_gains = pwg[1]

        if player.team == "Guthix":
            icon = guthix
            icon_pos = (1200, 415)
            icon_large = icon.resize((icon.width * 2, icon.height * 2))
            stats_team = stats_guthix
            xp_percentages_team = xp_percentages_guthix
        else:
            icon = saradomin
            icon_pos = (1156, 420)
            icon_large = icon.resize((int(icon.width * 1.8), int(icon.height * 1.8)))
            stats_team = stats_sara
            xp_percentages_team = xp_percentages_sara

        card = Card(player.name, player_gains, icon_large, icon_pos, stats_all, stats_team, xp_percentages_all, xp_percentages_team)
        card.output()


if __name__ == "__main__":
    main()