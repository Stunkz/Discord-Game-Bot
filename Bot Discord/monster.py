class testMonster:

    def __init__(self):
        self.pv=10
        self.damage=1

    def action(self, enemy, player, tour):
        text = ''
        text += f'Player : {player.pv} -{self.damage} \n'
        player.pv -= self.damage
        return text


monsterList = {1:testMonster}