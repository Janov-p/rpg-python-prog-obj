### import
import math
import random
from datetime import date
class Stat:
    """ stat of the player """
    def __init__(self,dictArgs):
        self.strength  = dictArgs['strength']
        self.magic  = dictArgs['magic']
        self.agility  = dictArgs['agility']
        self.speed  = dictArgs['speed']
        self.charisma  = dictArgs['charisma']
        self.chance  = dictArgs['chance']
        self.endurance = random.randint(self.strength+self.agility,2 * (self.strength + self.agility))
        self.life_point = random.randint(self.endurance,2 * self.endurance)
        self.attack = self.strength + self.magic + self.agility
        self.defense = self.agility + self.speed + self.endurance
    
    @property
    def strength(self):
        print "strength: "
        return self._strength

    @strength.setter
    def strength(self, v):
        print "strength upgrade"
        self._strength  =  v
    
    def __str__(self):
        return str(self.__dict__)

class Classe:
    """ class type """
    def __init__(self,name,stat):
        self._name = name
        self._stat = stat
    
    def __str__(self):
        return str(self._name)

class Race:
    """ race type """
    def __init__(self,name,stat):
        self._name = name
        self._stat = stat
    
    def __str__(self):
        return str(self._name)

class Avatar:
    """ general class """
    id = 0
    def __init__(self,targs):
        self._nom = targs['name']
        self._race = targs['race']
        self._classe = targs['classe']
        self._bag = targs['bag']
        self._equipment = targs['equipment']
        self._element = targs['element']
        self._lvl = 1
        self._stat = Stat({'strength':1, 'magic':1,'agility':1,'speed':1,'charisma':0,'chance':0})
        Avatar.id += 1
        self.sumStat()
        self._life = self._stat.life_point

    def getBag(self):
        return self._bag._lItems

    def initiative(self):
        min = self._stat.speed
        max = self._stat.agility + self._stat.chance + self._stat.speed
        return random.randint(min,max) 

    def damages(self):
        critique = random.randint(0,self._stat.chance)
        min = 0 
        max = self._stat.attack
        if (critique > self._stat.chance / 2):
            print ("full damages")
            maxDam = random.randint(max, 2 * max)
        else:
            maxDam = random.randint(min,max)
        print self._nom + " done " + str(maxDam)
        return maxDam
    
    def defense(self,v):
        min = self._stat.agility
        max = self._stat.agility + self._stat.chance + self._stat.speed
        duck = random.randint(min,max)
        damage = 0
        if (duck == max):
            print ("the shot is dodged")
        elif (duck > max / 2):
            print ("partial dodge")
            damage /= 2
        else:
            damage = v
        damage -= self._stat.defense
        if (damage < 0):
            damage = 0
        if (damage > self._life):
            self._life = 0
            print ("You are dead")
        else:
            self._life -= damage
        print "life point: ",self._life," / ",self._stat.life_point

    def __str__(self):
        show = str(self._nom)
        return show

    def sumStat(self):
        equiment = 0
        for i in self._stat.__dict__:
            for j in self._equipment:
                equiment += j._stat.__dict__[i]
            self._stat.__dict__[i] = self._race._stat.__dict__[i] + self._classe._stat.__dict__[i] + equiment

class Mobs(Avatar):
    def __init__(self,targs):
        Avatar.__init__(self,targs)
        self._type = targs["type"]

    def __str__(self):
        output = "Mobs " + self._type + " " + self._nom
        return output

class Hero(Avatar):
    def __init__(self,targs):
        Avatar.__init__(self,targs)
        self._xp = 1
        self._profession = targs['profession']
        self._lvl = self.lvl()

    def lvl(self):
        lvl = math.floor(self._xp/100)
        if (lvl < 1):
            lvl = 1
        if (lvl > self._lvl):
            print "### new level ###"
            self.newLvl()
        return lvl

    def newLvl(self):
        for i in self._stat.__dict__:
            self._stat.__dict__[i] += 5
        self._life = self._stat.life_point
        print "### stats upgrade ###"

    def setXP(self,xp):
        self._xp += xp
        self._lvl = self.lvl()

    def __str__(self):
        output = "joueur " + self._nom + " de niveau " + str(self._lvl) + " classe " + str(self._classe) + " race " + str(self._race) 
        return output

    def save(self):
        fileName = str(date.today())+"_"+str(Hero.id)+"_"+str(self._nom)+".txt"
        f = open(fileName,"w+")
        f.write(self._nom + "\n")
        f.write(self._race._name + "\n")
        f.write(self._classe._name + "\n")
        f.write("lvl: " + str(self._lvl) + "\n")
        f.write("xp: " + str(self._xp) + "\n")    
        for i in self._stat.__dict__:
            output = str(i) + " " + str(self._stat.__dict__[i])
            f.write(output + "\n")
        for i in self._equipment:
            f.write(str(i) + "\n")
        for i in self.getBag():
            f.write(str(i) + "\n")
        f.close()

    def saveXML(self):
        fileName = str(date.today())+"_"+str(Hero.id)+"_"+str(self._nom)+".xml"
        f = open(fileName,"w+")
        xml = "<?xml version='1.0' encoding='UTF-8'?>"
        xml += "<avatar id='"+ str(Hero.id) +"'>"
        xml += "<name>" + self._nom + "</name>"
        xml += "<race>" + self._race._name + "</race>"
        xml += "<level>" + self._classe._name + "</level>"
        xml += "<xp>" + str(self._lvl) + "</xp>"
        xml += "<name>" + str(self._xp) + "</name>"
        xml += "<stats>"    
        for i in self._stat.__dict__:
            xml += "<" + str(i) + ">" + str(self._stat.__dict__[i]) + "</" + str(i) + ">"
        xml += "</stats>"
        xml += "<equipments>"
        it = 1
        for i in self._equipment:
            xml += "<item_" + str(it) + ">" + i._name + "</item_" + str(it) + ">"
            it += 1
        xml += "</equipments>"
        xml += "<bag>"
        it = 1
        for i in self.getBag():
            xml += "<item_" + str(it) + ">" + i._name + "</item_" + str(it) + ">"
            it += 1
        xml += "</bag>"
        xml += "</avatar>"
        f.write(xml)
        f.close()

    @staticmethod
    def load():
        pass
        
class Item:
    """ object class """
    nbr = 0
    def __init__(self,targs,stat):
        self._name = targs['name']
        self._type = targs['type']
        self._space = targs['space']
        self._stat = stat
        Item.nbr += 1
    
    def __str__(self):
        return str(self._name)

class Equipment(Item):
    def __init__(self,targs,stat):
        Item.__init__(self,targs,stat)
        self._lClasses = targs['classList']
        self._place = targs['place']

class Bag:
    """ Bag class to save Items """
    def __init__(self,args):
        self._sizeMax = args['sizeMax']
        self._lItems = args['items']
        self._size = len(self._lItems)
    
    def addItem(self,i):
        if (self._size < self._sizeMax):
            self._lItems.append(i)
            self._size += 1
        else:
            return False
    
    def delItem(self,i):
        self._lItems.pop(i)
        self._size -= 1

    def __str__(self):
        output = ""
        for i in self._lItems: 
            output += str(i)
        return output  

class Quest:
    """ class for manage quest """
    def __init__(self,targs):
        self._lAvatar = targs['lAvatar']
        self._lvl = targs['lvl']
        self._itemGift = targs['gift']

    def run(self,hero):
        round = 1
        output = ""
        if (len(self._lAvatar) == 1):
            output += "### PVP MODE ####"
            print "### PVP MODE ####"
            player = self._lAvatar[0]
            output += "\n" + player._nom + " VS " + hero._nom
            print player._nom + " VS " + hero._nom
            while (player._life > 0 ) and (hero._life > 0 ):
                output += "\n" + "Round " + str(round)
                print "# Round " + str(round) + " # "
                print "# PV de " + hero._nom + " " + str(hero._life)
                output += "\n" + "# PV de " + hero._nom + " " + str(hero._life)
                print "# PV de " + player._nom + " " + str(player._life)
                output += "\n" + "# PV de " + player._nom + " " + str(player._life)
                if (player.initiative() > hero.initiative):
                    output += "\n" + player._nom + " begin"
                    print player._nom + " begin"
                    hero.defense(player.damages())
                    if (hero._life <= 0):
                        output += "\n" + player._nom + " win"
                        print player._nom + " win"
                    else:
                        player.defense(hero.damages())
                else:
                    output += "\n" + hero._nom + " begin"
                    print hero._nom + " begin"
                    player.defense(hero.damages())
                    if (player._life <= 0):
                        output += "\n" + hero._nom + " win"
                        print hero._nom + " win"
                    else:
                        hero.defense(player.damages())
                round += 1
            if (hero._life <= 0):
                output += "\n" + player._nom + " win"
                print player._nom + " win"
                player.setXP(10*self._lvl)
                player._bag.addItem(self._itemGift)
            else:
                output += "\n" + hero._nom + " win"
                print hero._nom + " win"
                hero.setXP(10*self._lvl)
                hero._bag.addItem(self._itemGift)                
        else:
            output += "\n" + "### Quest MODE ####"
            print "### Quest MODE ####"
            for player in self._lAvatar:
                output += "\n" + player._nom + " VS " + hero._nom
                print player._nom + " VS " + hero._nom
                while (player._life > 0 ) and (hero._life > 0 ):
                    output += "\n" + "Round " + str(round)
                    print "Round " + str(round)
                    print "# Round " + str(round) + " # "
                    print "# PV de " + hero._nom + " " + str(hero._life)
                    output += "\n" + "# PV de " + hero._nom + " " + str(hero._life)
                    print "# PV de " + player._nom + " " + str(player._life)
                    output += "\n" + "# PV de " + player._nom + " " + str(player._life)
                    if (player.initiative() > hero.initiative):
                        output += "\n" + player._nom + " begin"
                        print player._nom + " begin"
                        tmpDegats = player.damages()
                        hero.defense(tmpDegats)
                        output += "\n" + player._nom + " degats " + str(tmpDegats)
                        print player._nom + " degats " + str(tmpDegats)
                        if (hero._life <= 0):
                            output += "\n" + player._nom + " win"
                            print player._nom + " win"
                        else:
                            tmpDegats = hero.damages()
                            player.defense(tmpDegats)
                            output += "\n" + hero._nom + " degats " + str(tmpDegats)
                            print hero._nom + " degats " + str(tmpDegats)
                    else:
                        output += "\n" + hero._nom + " begin"
                        print hero._nom + " begin"
                        tmpDegats = hero.damages()
                        player.defense(tmpDegats)
                        output += "\n" + hero._nom + " degats " + str(tmpDegats)
                        print hero._nom + " degats " + str(tmpDegats)
                        if (player._life <= 0):
                            output += "\n" + hero._nom + " win"
                            print hero._nom + " win"
                        else:
                            tmpDegats = player.damages()
                            hero.defense(tmpDegats)
                            output += "\n" + player._nom + " degats " + str(tmpDegats)
                            print player._nom + " degats " + str(tmpDegats)
                    round += 1
            if (hero._life <= 0):
                output += "\n" + "You loose"
                print "You loose"
            else:
                output += "\n" + hero._nom + " win"
                print hero._nom + " win"
                hero.setXP(10 * len(self._lAvatar) * self._lvl)
                hero._bag.addItem(self._itemGift)
            return output

    def __str__(self):
        return self._itemGift

def main():
    ### RACE
    statElfe = Stat({'strength':5, 'magic':10,'agility':10,'speed':5,'charisma':5,'chance':5})
    elfe = Race('Elfe',statElfe)
    statHuman = Stat({'strength':10, 'magic':10,'agility':5,'speed':5,'charisma':5,'chance':5})
    human = Race('Human',statHuman)
    statDwarf = Stat({'strength':10, 'magic':0,'agility':10,'speed':5,'charisma':5,'chance':10})
    dwarf = Race('Dwarf',statDwarf)
    statOrc = Stat({'strength':15, 'magic':0,'agility':5,'speed':10,'charisma':5,'chance':5})
    orc = Race('Orc',statOrc)
    ### CLASS
    statWizard = Stat({'strength':0, 'magic':10,'agility':0,'speed':0,'charisma':10,'chance':10})
    wizard = Race('Wizard',statWizard)
    statWarrior = Stat({'strength':10, 'magic':0,'agility':5,'speed':5,'charisma':5,'chance':5})
    warrior = Race('Warrior',statWarrior)
    ### ITEMS
    statSword = Stat({'strength':5, 'magic':0,'agility':5,'speed':5,'charisma':0,'chance':5})
    sword = Equipment({'classList':'warrior','place':'hand','name':'dragon sword','type':'sword','space':2,},statSword)
    statBaton = Stat({'strength':0, 'magic':10,'agility':0,'speed':5,'charisma':0,'chance':5})
    baton = Equipment({'classList':'wizard','place':'hand','name':'wizard baton','type':'baton','space':2,},statBaton)
    statPotion = Stat({'strength':0, 'magic':0,'agility':0,'speed':0,'charisma':0,'chance':0})
    Potion = Item({'name':'life potion','type':'potion','space':2,},statPotion)
    ### BAG
    myBag = Bag({"sizeMax":20,"items":[Potion,Potion]})
    ### MOBS
    mechant1 = Mobs({'name':'orc 1','race':orc,'classe':warrior,'bag':myBag,'equipment':[sword],'element':'Fire','type':'soldier'})
    mechant2 = Mobs({'name':'orc 2','race':orc,'classe':warrior,'bag':myBag,'equipment':[sword],'element':'Fire','type':'soldier'})
    hero1 = Hero({'name':'Jean','race':elfe,'classe':wizard,'bag':myBag,'equipment':[baton],'element':'Fire','profession':'chomeur'})
    hero2 = Hero({'name':'Pierre','race':human,'classe':warrior,'bag':myBag,'equipment':[sword],'element':'Fire','profession':'chomeur'})
    hero1.save()
    hero1.saveXML()
    ### QUEST 
    firstQuest = Quest({'lAvatar':[mechant1,mechant2],'lvl':2,'gift':sword})
    #firstQuest = Quest({'lAvatar':[hero2],'lvl':2,'gift':sword})
    #firstQuest.run(hero1)

if __name__ == "__main__":
    # execute only if run as a script
    main()