import requests
import csv
import pickle
import datetime


class Competition:

    def __init__(self, competition_id):
        self.competition_id = competition_id
        self.players = {}

    def __str__(self):
        text = str(self.competition_id)
        for p in self.players.values():
            text += " " + str(p)
        return text

    def update(self):
        url = f"https://api.wiseoldman.net/competitions/{self.competition_id}/csv?table=participants"
        response = requests.get(url)
        if response.status_code != 200:
            return None

        content = response.content.decode("utf-8")

        reader = csv.DictReader(content.splitlines())
        for row in reader:
            # {
            # 'Rank': '1',
            # 'Username': 'Iron Aff',
            # 'Team': 'Saradomin',
            # 'Start': '5981683',
            # 'End': '7598877',
            # 'Gained': '1617194',
            # 'Last Updated': '08-05-2022 16:59'
            # }
            player = self.players.get(row["Username"])
            if not player:
                player = Player(row["Username"], row["Team"])
                self.players[player.name] = player

            newXp = int(row["Gained"])
            timestamp = datetime.datetime.strptime(row["Last Updated"], "%m-%d-%Y %H:%M")
            if player.xp_times:
                last = player.xp_times[-1]
                # player has not been updated at all
                if (last[1] == newXp and last[0] == timestamp):
                    continue

                # player has been updated but xp is the same
                if (last[1] == newXp and last[0] != timestamp and len(player.xp_times) >= 2):
                    # If there are 3 data points all with same xp, remove middle one
                    second_last = player.xp_times[-2]
                    if second_last[1] == newXp:
                        player.xp_times[-1] = (timestamp, newXp)
                        continue

            player.xp_times.append((timestamp, newXp))

    def save_file(self):
        with open(f"./competition{self.competition_id}.pickle", "wb") as f:
            pickle.dump(self, f, -1)

    def load_file(self):
        try:
            competition = pickle.load(open(f"./competition{self.competition_id}.pickle", "rb", -1))
        except FileNotFoundError:
            return
        self.competition_id = competition.competition_id
        self.players = competition.players


class Player:
    def __init__(self, name, team):
        self.name = name
        self.xp_times = []
        self.team = team

    def __str__(self):
        return f"{self.name} {self.team} {self.xp_times}"


class PlayerGains:
    def __init__(self, name, start, end):
        self.name = name
        self.start = start
        self.end = end
        self.data = {}

    def update(self):
        url = f"https://api.wiseoldman.net/players/username/{self.name}/gained/"
        payload = {
            'startDate': self.start,
            'endDate': self.end
        }
        r = requests.get(url, params=payload)
        if r.status_code == 200:
            gains = r.json()
            self.data = gains["data"]

    def save_file(self):
        with open(f"players/{self.name}.pickle", "wb") as f:
            pickle.dump(self, f, -1)

    def load_file(self):
        try:
            player_gains = pickle.load(open(f"players/{self.name}.pickle", "rb", -1))
        except FileNotFoundError:
            return
        self.name = player_gains.name
        self.start = player_gains.start
        self.end = player_gains.end
        self.data = player_gains.data
