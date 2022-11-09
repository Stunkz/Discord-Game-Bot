import discord
from crtoolkit import JsonData, DatabaseHandler
from monster import *
from items import *

playerlist = {}

def createPlayer(message):

    db = DatabaseHandler("PlayerData.db")
    db.connectToDb()
    id = message.author.id
    for ID in db.executeQueries("SELECT * FROM PlayerData"):
        if ID[0] == id:
            return 'Ta mere la pute'
    db.executeQueries(
        f"INSERT INTO PlayerData (PlayerID, Gold, Stage, HP) VALUES ({ id }, { 10 }, { 0 }, { 10 })"
    )
    db.commitChanges()
    db.executeQueries(
        f"INSERT INTO Inventory (PlayerID, ItemID, ItemLVL) VALUES ({ id }, { 1 }, { 1 })"
    )
    db.commitChanges()
    db.closeDb()
    playerlist.update({id: Player(id)})
    return 'Désolé Frérot'

def loadData():

    global playerlist
    playerlist = {}
    db = DatabaseHandler("PlayerData.db")
    db.connectToDb()

    for ID in db.executeQueries("SELECT * FROM PlayerData"):
        playerlist.update({ID[0]: Player(ID[0])})

    print(playerlist)
    db.closeDb()


class Player:

    def __init__(self, id):
        db = DatabaseHandler("PlayerData.db")
        db.connectToDb()
        dataList = [(playerID, gold, stage, hp) for (playerID, gold, stage, hp) in db.executeQueries("SELECT * FROM PlayerData") if playerID == id][0]
        dataInventoryList = [(playerID, itemID, itemLVL) for (playerID, itemID, itemLVL) in db.executeQueries("SELECT * FROM Inventory") if playerID == id]
        self.pv = dataList[3]
        self.gold = dataList[1]
        self.stage = dataList[2]
        self.id = id
        #Equipement order : Sword, Helmet, Chestplate, Leggings, Boots
        self.equippement = [None, None, None, None, None]
        print(dataInventoryList)
        db.closeDb()

    def updateData(self):
        db = DatabaseHandler("PlayerData.db")
        db.connectToDb()
        db.executeQueries(
            f"UPDATE PlayerData SET HP={self.pv}, Gold = {self.gold}, Stage = {self.stage} WHERE PlayerID={self.id}"
        )
        db.commitChanges()
        db.closeDb()

    def equip(self, inventorySlotID):
        itemOrder = ['Sword', 'Helmet', 'Chestplate', 'Leggins', 'Boots']
        try:
            itemToEquip = self.getInventory(False)[inventorySlotID-1]
            self.equippement[itemOrder.index(itemToEquip.itemType)] = itemToEquip
        except Exception as error:
            print(error)

    def getInventory(self,text):
        db = DatabaseHandler("PlayerData.db")
        db.connectToDb()
        dataInventoryList = [(playerID, itemID, itemLVL) for (playerID, itemID, itemLVL) in db.executeQueries("SELECT * FROM Inventory") if playerID == self.id]
        itemText = "Inventaire : \n\n"
        inventoryList = []
        slotID = 1
        for i in dataInventoryList:
            itemText = itemText + itemList[i[1]]().getInfo() + "Slot ID : " + str(slotID) + "\n\n"
            inventoryList.append(itemList[i[1]]())
            slotID += 1
        db.closeDb()
        if text == True:
            return itemText
        else:
            return inventoryList

    def getEquippement(self):
        itemText = "Equippement : \n\n"
        for i in self.equippement:
            if i:
                itemText = itemText + i.getInfo() + "\n\n"
        return itemText

    def getGold(self):
        return f'Vous avez {self.gold} d\'or'

    def getHP(self):
        return f'Vous avez {self.pv} PV'

    def getStage(self):
        return f'Vous etes à l\'étage {self.stage}'

def fight(message):
    enemy = monsterList[int(message.content.split()[1])]()
    player = playerlist[message.author.id]
    combat = ""
    tour=0
    while True:
        tour+=1
        if player.equippement[0] == None:
            combat += itemList[0]().action(enemy, player, tour)
        else:
            combat += player.equippement[0].action(enemy, player, tour)
        if enemy.pv <= 0:
            combat += "L'enemie a perdu"
            break
        if player.pv <= 0:
            combat += "Vous avez perdu"
            break
        combat += enemy.action(enemy, player, tour)
    player.updateData()
    return combat


class MyClient(discord.Client):

    async def on_ready(self):
        print('Ready')
        loadData()


    async def on_message(self, message):
        if message.author == self.user:
            return

        if  message.content.split()[0] == '!create':
            await message.channel.send(createPlayer(message))

        if  message.content.split()[0] == '!gold':
            await message.channel.send(playerlist[message.author.id].getGold())

        if  message.content.split()[0] == '!stage':
            await message.channel.send(playerlist[message.author.id].getStage())

        if  message.content.split()[0] == '!pv':
            await message.channel.send(playerlist[message.author.id].getHP())

        if  message.content.split()[0] == '!addpv':
            playerlist[message.author.id].pv += 10
            playerlist[message.author.id].updateData()

        if message.content.split()[0] == '!fight':
            await message.channel.send(fight(message))

        if  message.content.split()[0] == '!equip':
            playerlist[message.author.id].equip(int(message.content.split()[1]))

        if  message.content.split()[0] == '!inventory':
            await message.channel.send(playerlist[message.author.id].getInventory(True))

        if  message.content.split()[0] == '!equippement':
            await message.channel.send(playerlist[message.author.id].getEquippement())


client = MyClient()
client.run('MTAzMzExOTQ4MjEyMzY0OTA3Ng.GSobFb.tnLLx33HcGd3Dih-tBJ7qp2HHXPqDHjX195wjg')
