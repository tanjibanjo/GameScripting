#Lane Pollock
#8 July 2025
#Class to hold values for character and enemy in text based adventure

class Character:
    def __init__(self, name, health, attack, dex, type):
        self.name = name
        self.health = health
        self.attack = attack
        self.dex = dex
        self.type = type

class Enemy:
    def __init__(self, name, health, attack, used, score):
        self.name = name
        self.health = health
        self.attack = attack
        self.used = used
        self.score = score
