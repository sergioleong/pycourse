from random import randint

class Character:
    def __init__(self, name : str, hp : int, strength : int, money : int):
        self.name = name
        self.hp = hp
        self.hp_total = hp
        self.status = 'alive'
        self.strength = strength
        self.money = money
    
    def __str__(self):
        return f"{self.name} - {self.hp}/{self.hp_total}"

    def attack_turn(self):
        return max(0,randint(self.strength-1,self.strength+1)), "physical"

    def defense_turn(self, damage : int, type : str):
        if damage >= self.hp:
            self.hp = 0
            self.status = 'dead'
        else:
            self.hp -= damage
    
    def alive(self) -> str:
        return self.status != 'dead'
        
    def battle(self, other : 'Character'):
        while True:
            if not self.alive():
                return False
            a_damage, a_type = self.attack_turn()
            print(f"{self.name} attacked for {a_damage} {a_type} damage")
            other.defense_turn(a_damage,a_type)
            print(f"{other}")

            if not other.alive():
                return True
            b_damage, b_type = other.attack_turn()
            print(f"{other.name} attacked for {b_damage} {b_type} damage")
            self.defense_turn(b_damage,b_type)
            print(f"{self}")

class GhostType(Character):
    def attack_turn(self):
        return max(0,randint(self.strength-1,self.strength+1)), "magic"

    def defense_turn(self, damage : int, type : str):
        if type == "magic":
            super().defense_turn(damage,type)

class WallType(Character):
    def attack_turn(self):
        self.hp +=randint(self.strength-1,self.strength+1)
        return 0, "physical"

class Player(Character):
    def __init__(self, name : str, hp : int, strength : int, money : int, magic : int, healing : int):
        super().__init__(name,hp,strength,money)
        self.magic = magic
        self.healing = healing

    def attack_turn(self):
        choice = ""
        while choice not in ["1","2", "3"]:
            choice = input("(1) Attack\n(2) Magic\n(3) Heal")
        if choice == "1":
            return max(0,randint(self.strength-1,self.strength+1)), "physical"
        if choice == "2":
            return max(0,randint(self.magic-1,self.magic+1)), "magic"
        if choice == "3":
            self.hp +=randint(self.healing-1,self.healing+1)
            return 0, "physical"
    
    def winMoney(self,money : int):
        self.money += money


def main(argv):
    player = Character("player", hp=100, strength=5, money=100)
    enemy = Character("goblin", hp=10, strength=3, money=5)
    print(f'Start combat against {enemy}')
    if player.battle(enemy):
        print(f"{player.name} won!")
    else:
        print(f"{enemy.name} won!")


    player = Character("player", hp=100, strength=5, money=100)
    while player.alive():
        enemy_type = randint(0,4)
        if enemy_type == 0:
            enemy = Character("goblin", hp=10, strength=3, money=5)
        elif enemy_type == 1:
            enemy = Character("orc", hp=30, strength=6, money=20)
        elif enemy_type == 2:
            enemy = GhostType("ghost", hp=10, strength=5, money=10)
        elif enemy_type == 3:
            enemy = GhostType("litch", hp=30, strength=8, money=50)
        else :
            enemy = WallType("wall", hp=20, strength=2, money=100)
        print(f'Start combat against {enemy}')
        if player.battle(enemy):
            print(f"{player.name} won!")
        else:
            print(f"{enemy.name} won!")


    player = Player("player", hp=100, strength=5, magic=3, healing=10, money=100)

    print(f'''We have our player and we can see that this object is of type Player:
    {type(player)}
    isinstance(player, Player): {isinstance(player, Player)}
But at the same time it's also instance of Character class because of inheritance:
    isinstance(player, Character): {isinstance(player, Character)}
    
    ''')

    while player.alive():
        enemy_type = randint(0,4)
        if enemy_type == 0:
            enemy = Character("goblin", hp=10, strength=3, money=5)
        elif enemy_type == 1:
            enemy = Character("orc", hp=30, strength=6, money=20)
        elif enemy_type == 2:
            enemy = GhostType("ghost", hp=10, strength=5, money=10)
        elif enemy_type == 3:
            enemy = GhostType("litch", hp=30, strength=8, money=50)
        else :
            enemy = WallType("wall", hp=20, strength=2, money=100)
        print(f'Start combat against {enemy}')
        if player.battle(enemy):
            print(f"{player.name} won!")
            player.winMoney(enemy.money)
        else:
            print(f"{enemy.name} won!")
    print(f'Player is dead, but has earned ${player.money} from the enemies.')
