import random


affirm = ["yes", "y"]


def adpr_calculator(cls, lvl, enh, mod):
    """
    average damage-per-round calculator is intended to calculate the average amount of damage your class should expect
    to do in a round of combat, given that you hit all of your attacks in that round. It also takes into account SOME
    special actions certain pathfinder classes are capable of, such as Power Attack, sneak attack, and perhaps rage and
    others in the future. Maybe even Two-weapon fighting if i decide i hate myself, but that will likely take it's own
    function entirely.
        Likely by asking the user at the start of the function then hoisting the issue off to that function, much as i'd
        like to hoist the issue of creating that function on to literally anybody else.

    :param cls: The Pathfinder class you are playing as

    :param lvl: What level you are in this class (no multi-classing allowed, that's for cheaty cheaters and would be an
    absolute PIMA to account for, I may make another function to account for it but until then NO CHEAT! 1 class! ONE(1)

    :param enh: Your weapon enhancement modifier, such as a Longsword +1. Only matters for damage, not to-hit, so i
    don't have to care about masterwork weirdness with this function

    :param mod: this is your damage modifier, usually strength unless you're doing some dex weirdness, but that's okay
    cuz a mod is a mod and can be accounted for!

    :return: it takes your weapon's damage dice, finds it's average, adds your weapon enhancement and damage modifier,
    then multiplies that result by how many times you could attack that round based off of your class's BAB and your
    level
    """

    cls = cls.lower()  # SlAYer -> slayer
    bab = bab_calculator(cls, lvl)
    pa_mod = 0
    die = input("input weapon's damage dice in following format xdy (eg: 1d12 or 2d4): ")
    two_hand = str(input("is this being wielded with both hands?: "))  # okay NOW i should maybe care if it's DEX or STR
    if two_hand.lower() in affirm:
        two_hand = True
    else:
        two_hand = False
    # to_hit = bab + enh + mod
    avg_dmg = avg_dmg_calculator(enh, mod, die, two_hand)
    pa = input("Are you using Power Attack? ")
    if pa.lower() in affirm:
        pa_mod = 1 + int(bab / 4)
    if two_hand:
        avg_dmg += pa_mod * 3
    else:
        avg_dmg += pa_mod * 2
    if cls == "slayer" or cls == "rogue":
        sneak_attack = input("Are you using sneak attack?: ")
        if sneak_attack.lower() in affirm:
            if cls == "slayer":
                avg_dmg += (3.5 * int(lvl / 3))
            elif cls == "rogue":
                avg_dmg += (3.5 * int((lvl + 1) / 2))
    avg_dmg *= int(1 + ((bab - 1) / 5))

    print(f"Your average expected damage per round, assuming all attacks hit is {avg_dmg}")


def bab_calculator(cls, lvl):
    """
    calculates the Base Attack Bonus (BAB) for your Pathfinder class given your level
    note: only works for single class. Multiclass is cheating. cheater.
    :param cls: your pathfinder class
    :param lvl: how many levels you have in that class
    :return: your BAB
    """
    if cls == 'sorcerer' or cls == "wizard" or cls == "arcanist" or cls == "witch":
        return int(lvl * .5)
    elif cls == "barbarian" or cls == "fighter" or cls == "brawler" or cls == "slayer" or cls == "paladin":
        return lvl
    elif cls == "bloodrager" or cls == "ranger" or cls == "swashbuckler" or cls == "gunslinger":
        return lvl
    else:
        return int(lvl * (3 / 4))
        # ^ This represents 16 classes I now don't have to name. Yes it accepts a made up a class, but if you're making
        # up a class, chances are it was gunna be 3/4 BAB anyways.


def avg_dmg_calculator(enh, mod, die, two_hand):
    """
    this function seeks to calculate the average expected damage you do in a single attack given your damage modifiers,
    your weapon's damage die/dice, and whether or not the weapon is being wielded in one or 2 hands.

    :param enh: Your weapon enhancement modifier, such as a Longsword +1. Only matters for damage, not to-hit, so i
    don't have to care about masterwork weirdness with this function

    :param mod: this is your damage modifier, usually strength unless you're doing some dex weirdness, but that's okay
    cuz a mod is a mod and can be accounted for!

    :param die: Your weapon's damage die/dice taken in the form of XdY (eg 1d6 or 2d4)

    :param two_hand: boolean to determine if the weapon is being held in 2 hands. The function assumes that actually
    maters because otherwise i would have to curl up into a ball and cry as i contemplated every life choice that
    brought me to this moment.

    :return: the average expected damage on any given hit
    """
    d_parser = die.split('d')
    dice = int(d_parser[0])
    dmg_die = int(d_parser[1])
    avg_dmg = 0
    while dice > 0:
        avg_dmg += (dmg_die + 1) / 2
        dice -= 1
    if two_hand:
        mod = int(mod * 1.5)
    avg_dmg += enh + mod
    return avg_dmg


# Given number of hits in a round, and a weapons damage dice, enhancement mod, and players damage modifier
# function "rolls the damage dice" and outputs possible damage that round
def damage_calc(enh, mod, die, two_hand):
    """
    Average shmaverage pfft, you don't care how much damage you'll _usually_ do you wanna see those big numbers that
    actually mean something! well thanks to this function (and random number generators) you can find out!

    this function acts exactly as avg_dmg_calculator except it actually rolls the dice instead of spitting out an
    average.
    :param enh: see avg_dmg_calculator
    :param mod: see avg_dmg_calculator
    :param die: see avg_dmg_calculator
    :param two_hand: see avg_dmg_calculator

    :return: the damage you did with this particular hit.
    """
    d_parser = die.split('d')
    dice = int(d_parser[0])
    dmg_die = int(d_parser[1])
    dmg = 0
    if two_hand:
        mod = int(mod * 1.5)
    while dice > 0:
        dmg += random.randrange(1, dmg_die + 1)
        dice -= 1
        dmg += enh + mod
    return dmg


def round_dmg_calculator(cls, lvl, enh, mod, hits):
    """
    This function acts exactly as adpr_calculator, except it calls dmg_calculator for each attack the player can do to
    calculate the amount of damage you actually did in that round

    :param cls: see adpr_calculator

    :param lvl: see adpr_calculator

    :param enh: see adpr_calculator*
        except actually i _do_ need to care about masterwork weirdness with this function. shit.

    :param mod: see adpr_calculator

    :param hits: so, turns out, you don't actually always hit every single attack, so this function takes how many times
    you hit your opponent as a parameter to calculate how much damage instead of doing BAB math.

    :return: How much damage you did in that round.
    """
    cls = cls.lower()
    dmg = 0
    bab = bab_calculator(cls, lvl)
    pa_mod = 0  # Power Attack Modifier
    die = input("input weapon's damage dice in following format xdy (eg: 1d12 or 2d4): ")
    two_hand = str(input("is this being wielded with both hands?: "))
    if two_hand.lower() in affirm:
        two_hand = True
    else:
        two_hand = False
    pa = input("Are you using Power Attack? ")
    if pa.lower() in affirm:
        pa_mod = 1 + int(bab / 4)
    while hits > 0:
        dmg += damage_calc(enh, mod, die, two_hand)
        if two_hand and pa:
            dmg += pa_mod * 3
        elif pa:
            dmg += pa_mod * 2
        if cls == "slayer" or cls == "rogue":
            sneak_attack = input("Are you using sneak attack?: ")
            if sneak_attack.lower() in affirm:
                if cls == "slayer":
                    slayer_sneak_dice = int(lvl / 3)
                    while slayer_sneak_dice > 0:
                        dmg += random.randrange(1, 7)
                        slayer_sneak_dice -= 1
                elif cls == "rogue":
                    rogue_sneak_dice = int((lvl + 1) / 2)
                    while rogue_sneak_dice > 0:
                        dmg += random.randrange(1, 7)
                        rogue_sneak_dice -= 1
        hits -= 1

    print(f"You dealt a total of {dmg} damage this round.")

if __name__ == '__main__':
    p_class = input("What pathfinder class are you playing?: ")
    p_lvl = int(input("What level are you in that class?: "))
    p_enh = int(input("What is your weapon's enhancement modifier (DO NOT ADD THE '+'): "))
    p_str = int(input("What is your strength modifier (DO NOT ADD THE '+'): "))
    p_hits = int(input("How many times did you hit the opponent this round?: "))
    round_dmg_calculator(p_class, p_lvl, p_enh, p_str, p_hits)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
