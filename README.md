# OSRS Skilling Competition Player Cards
## Video Demo: https://youtu.be/PyDoMB4k5J8
## Description:

### Context
Old School Runescape (OSRS) is an online multiplayer game which has 26 skills that can be trained.
Training skills grants experience (XP) which can increase your levels in that skill.

I recently participated in a skilling competition with 71 participants split into two teams (Guthix and Saradomin).
Each day, two skills were selected to be trained. The teams with the highest total experience won that skill and earned points.
There were also points from receiving certain rare items which involved defeating certain bosses.

### Objective
This project aims to summarize each player's efforts during the competition in the form of a player card image.
The card lists the following for each skill:
- Skill icon
- Skill name
- Experience gained
- Efficient Hours Played (EHP - )
- Levels gained
- Rank/% - The rank from 1-71 out of all players and the % of the player's experience out of everyone's experience
- Team Rank/% - same as above but restricted to players only in the player's team

The card also lists the following for each boss:
- Boss icon
- Boss name
- Number of kills
- Rank/% - The rank from 1-71 out of all players and the % of the player's kills out of everyone's kills
- Team Rank/% - same as above but restricted to players only in the player's team

The card also displays the team logo in the right bottom corner, a title, and the player's name.

### Implementation

Data is obtained from https://wiseoldman.net/ using their api with the time period for the competition.

#### project.py
Main program that loads the competition data, calculates aggregate statistics, and outputs each card to the "cards" directory.

#### models.py
Contains Competition, PlayerGains, and Player class definitions to load, save, and store player data to the "players" directory.

#### skills.py
Stores the skill list and utilities for calculating levels gained, downloading the skill icons, and getting a lowercase dictionary key for a skill.

#### bosses.py
Defines a Boss class and lists the 5 bosses tracked with name, icon, and the dictionary key to get to the relevant data.

#### card.py
Defines the Card class which takes all the relevant data to create a player card.
This class generates the cards using the Pillow library to overlay images and draw text.

#### test_project.py
This tests some functions from project.py.

#### test_skills.py
This tests some functions from skills.py.

### Player Card Sample
[Sample Card image](cards/rootb.png)