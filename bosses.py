import os.path

from PIL import Image

class Boss:
    def __init__(self, name, icon, first_key, second_key):
        self.name = name
        self.icon = icon
        self.first_key = first_key
        self.second_key = second_key

bosses = (
    Boss("Tempoross", Image.open(os.path.join("images", "bosses", "tempoross.png")), "tempoross", "kills"),
    Boss("Wintertodt", Image.open(os.path.join("images", "bosses", "wintertodt.png")), "wintertodt", "kills"),
    Boss("Hespori", Image.open(os.path.join("images", "bosses", "hespori.png")), "hespori", "kills"),
    Boss("GOTR", Image.open(os.path.join("images", "bosses", "guardians_of_the_rift.png")), "guardians_of_the_rift", "score"),
    Boss("Zalcano", Image.open(os.path.join("images", "bosses", "zalcano.png")), "zalcano", "kills")
)