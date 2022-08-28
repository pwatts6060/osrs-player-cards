import os

from PIL import Image, ImageDraw

import skills
from bosses import bosses


class Card:
    def __init__(self, player, player_gains, icon, icon_pos, overall_ranks, team_ranks, xp_percentages, xp_percentages_team):
        self.player = player
        self.player_gains = player_gains
        self.icon = icon
        self.icon_pos = icon_pos
        self.overall_ranks = overall_ranks
        self.team_ranks = team_ranks
        self.xp_percentages = xp_percentages
        self.xp_percentages_team = xp_percentages_team

    skill_icons = {}

    @classmethod
    def get_skill_icon(cls, skill):
        if not cls.skill_icons:
            cls.load_skill_icons()
        return cls.skill_icons[skill]

    @classmethod
    def load_skill_icons(cls):
        for skill in skills.skills_tuple:
            im = Image.open(os.path.join("images", "skills", skills.key_for(skill) + ".png"))
            cls.skill_icons[skill] = im


    def output(self):

        username = self.player
        im = Image.open("template.png")
        im.paste(self.icon, self.icon_pos, self.icon.convert("RGBA"))

        d = ImageDraw.Draw(im)

        from PIL import ImageFont
        font = ImageFont.truetype("./runescape.ttf", 46)
        d.text((im.width / 2, 45), f"OSRS Advice Skilling Competition Aug 2022 - {username}", (0, 0, 0), font=font,
               anchor="mm")

        # Skill table
        font = ImageFont.truetype("./runescape.ttf", 26)
        start_w = 50
        start_h = 92
        x = start_w
        y = start_h
        x_off = 680
        y_off = 35
        d.text((x, y), "Skill", (0, 0, 0), font=font, anchor="lm")
        d.text((x + x_off, y), "Skill", (0, 0, 0), font=font, anchor="lm")
        x += 230
        d.text((x, y), "XP", (0, 0, 0), font=font, anchor="rm")
        d.text((x + x_off, y), "XP", (0, 0, 0), font=font, anchor="rm")
        x += 70
        d.text((x, y), "EHP", (0, 0, 0), font=font, anchor="rm")
        d.text((x + x_off, y), "EHP", (0, 0, 0), font=font, anchor="rm")
        x += 70
        d.text((x, y), "Levels", (0, 0, 0), font=font, anchor="rm")
        d.text((x + x_off, y), "Levels", (0, 0, 0), font=font, anchor="rm")
        x += 100
        d.text((x, y), "Rank/%", (0, 0, 0), font=font, anchor="rm")
        d.text((x + x_off, y), "Rank/%", (0, 0, 0), font=font, anchor="rm")
        x += 150
        d.text((x, y), "Team rank/%", (0, 0, 0), font=font, anchor="rm")
        d.text((x + x_off, y), "Team rank/%", (0, 0, 0), font=font, anchor="rm")
        font = ImageFont.truetype("./runescape.ttf", 24)
        y += y_off
        overall_level_gain = 0
        for i, skill in enumerate(skills.skills_tuple):
            x = start_w
            if i >= len(skills.skills_tuple) // 2 + 5:
                x += x_off
            if i == len(skills.skills_tuple) // 2 + 5:
                y = start_h + y_off

            icon = Card.get_skill_icon(skill)
            im.paste(icon, (x - 18 - icon.width // 2, y - icon.height // 2), icon.convert("RGBA"))

            skill_data = self.player_gains.data[skills.key_for(skill)]
            xp_gain = skill_data['experience']['gained']
            ehp = skill_data['ehp']['gained']
            level_gain = skills.levels_gained(skill_data['experience']['start'], skill_data['experience']['end'])
            overall_level_gain += level_gain
            d.text((x, y), f"{skill}:", (0, 0, 0), font=font, anchor="lm")

            x += 230
            if xp_gain > 0:
                d.text((x, y), f"+{xp_gain:,}", (0, 0, 0), font=font, anchor="rm")

            x += 70
            if xp_gain > 0:
                d.text((x, y), f"+{ehp:,.2f}", (0, 0, 0), font=font, anchor="rm")

            x += 70
            if level_gain > 0 and skill != 'Overall':
                d.text((x, y), f"+{level_gain}", (0, 0, 0), font=font, anchor="rm")

            x += 100
            d.text((x, y), f"{self.overall_ranks[skill][username]+1}/{self.xp_percentages[skill][username]:.2f}%", (0, 0, 0), font=font, anchor="rm")

            x += 150
            d.text((x, y), f"{self.team_ranks[skill][username]+1}/{self.xp_percentages_team[skill][username]:.2f}%", (0, 0, 0), font=font, anchor="rm")

            y += y_off

        if overall_level_gain > 0:
            d.text((x - x_off - 255, start_h + y_off), f"+{overall_level_gain}", (0, 0, 0), font=font, anchor="rm")

        # Bosses
        font = ImageFont.truetype("./runescape.ttf", 26)
        y = 440
        x = start_w + x_off
        d.text((x, y), "Boss", (0, 0, 0), font=font, anchor="lm")
        x += 170
        d.text((x, y), "Kills", (0, 0, 0), font=font, anchor="rm")

        x += 100
        d.text((x, y), "Rank/%", (0, 0, 0), font=font, anchor="rm")

        x += 150
        d.text((x, y), "Team rank/%", (0, 0, 0), font=font, anchor="rm")

        font = ImageFont.truetype("./runescape.ttf", 24)
        for boss in bosses:
            y += y_off
            x = start_w + x_off
            im.paste(boss.icon, (x - 18 - boss.icon.width // 2, y - boss.icon.height // 2), boss.icon.convert("RGBA"))

            d.text((x, y), boss.name, (0, 0, 0), font=font, anchor="lm")

            x += 170
            d.text((x, y), f"+{self.player_gains.data[boss.first_key][boss.second_key]['gained']}", (0, 0, 0), font=font,
                   anchor="rm")

            x += 100
            d.text((x, y), f"{self.overall_ranks[boss.first_key][username]+1}/{self.xp_percentages[boss.first_key][username]:.2f}%", (0, 0, 0), font=font, anchor="rm")

            x += 150
            d.text((x, y), f"{self.team_ranks[boss.first_key][username]+1}/{self.xp_percentages_team[boss.first_key][username]:.2f}%", (0, 0, 0), font=font, anchor="rm")

        im.save(f"./cards/{username}.png")