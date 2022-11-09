import random

class punch:

    def __init__(self):
        self.damage = 1
        self.itemType = 'Sword'

    def action(self, enemy, player, tour):
        text = ''
        text += f'Enemy : {enemy.pv} -{self.damage} \n'
        enemy.pv -= self.damage
        return text

class woodenSword:

    def __init__(self):
        self.damage = 2
        self.itemType = 'Sword'
        self.level = 1
        self.description = f"Common WoodenSword : \nDescripton : Cette épée n'a rien de spéciale\nDégat : {self.damage}\nLVL : {self.level}\n"

    def getInfo(self):
        return self.description

    def action(self,enemy,player,tour):
        text = ''
        text += f'Enemy : {enemy.pv} -{self.damage} \n'
        enemy.pv -= self.damage
        return text


class woodenDagger:

    def __init__(self):
        self.damage = 2
        self.pourcentage = 10.0
        self.itemType = 'Sword'
        self.level = 1
        self.description = f"Common WoodenDagger : \nDescripton : Cette courte épée a {self.pourcentage}% de chance d'infliger un deuxième coup\nDégat : {self.damage}\nLVL : {self.level}\n"

    def getInfo(self):
        return self.description

    def action(self,enemy,player,tour):
        text = ''
        text += f'Enemy : {enemy.pv} -{self.damage} \n'
        enemy.pv -= self.damage
        if (random.randint(1,1000)/10) <= 10.0 :
            text += f'Enemy : {enemy.pv} -{self.damage} (deuxieme coup de dague) \n'
            enemy.pv -= self.damage
        return text

class stoneDagger:

    def __init__(self):
        self.damage = 3
        self.pourcentage = 11.0
        self.itemType = 'Sword'
        self.level = 1
        self.description = f"Common StoneSword : \nDescripton : Cette courte épée a {self.pourcentage}% de chance d'infliger un deuxième coup\nDégat : {self.damage}\nLVL : {self.level}\n"

    def getInfo(self):
        return self.description

    def action(self,enemy,player,tour):
        text = ''
        text += f'Enemy : {enemy.pv} -{self.damage} \n'
        enemy.pv -= self.damage
        if (random.randint(1, 1000) / 10) <= 10.0:
            text += f'Enemy : {enemy.pv} -{self.damage} (deuxieme coup de dague) \n'
            enemy.pv -= self.damage
        return text

class pineSword:

    def __init__(self):
        self.damage = 4
        self.itemType = 'Sword'
        self.level = 1
        self.description = f"Common PineSword : \nDescripton : Cette épée faite en bois de sapin est plus tranchante\nDégat : {self.damage}\nLVL : {self.level}\n"

    def getInfo(self):
        return self.description

    def action(self,enemy,player,tour):
        text = ''
        text += f'Enemy : {enemy.pv} -{self.damage} \n'
        enemy.pv -= self.damage
        return text

itemList = { 0 : punch, 1 : woodenSword, 2 : woodenDagger, 3 : stoneDagger, 4 : pineSword }