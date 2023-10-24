import random
from ucb import main, interact, trace
from collections import OrderedDict

################
# Core Classes #
################


class Place:
    """A Place holds insects and has an exit to another Place."""
    is_hive = False

    def __init__(self, name, exit=None):
        """Create a Place with the given NAME and EXIT.

        name -- A string; the name of this Place.
        exit -- The Place reached by exiting this Place (may be None).
        """
        self.name = name
        self.exit = exit
        self.bees = []        # A list of Bees
        self.ant = None       # An Ant
        self.entrance = None  # A Place
        if self.exit:
            self.exit.entrance = self

    def add_insect(self, insect):
        ...

    def remove_insect(self, insect):
        ...

    def __str__(self):
       ...


class Insect:
    """An Insect, the base class of Ant and Bee, has health and a Place."""

    damage = 0
    is_waterproof = False

    def __init__(self, health, place=None):
        """Create an Insect with a health amount and a starting PLACE."""
        self.health = health
        self.place = place  # set by Place.add_insect and Place.remove_insect

    def reduce_health(self, amount):
        """Reduce health by AMOUNT, and remove the insect from its place if it
        has no health remaining.

        >>> test_insect = Insect(5)
        >>> test_insect.reduce_health(2)
        >>> test_insect.health
        3
        """
        self.health -= amount
        if self.health <= 0:
            self.death_callback()
            self.place.remove_insect(self)

    def action(self, gamestate):
        ...

    def add_to(self, place):
        """Add this Insect to the given Place

        By default just sets the place attribute, but this should be overriden in the subclasses
            to manipulate the relevant attributes of Place
        """
        self.place = place

    def remove_from(self, place):
        self.place = None

    def __repr__(self):
        cname = type(self).__name__
        return '{0}({1}, {2})'.format(cname, self.health, self.place)


class Ant(Insect):
    """An Ant occupies a place and does work for the colony."""

    implemented = False
    food_cost = 0
    is_container = False
    blocks_path = True
    doubled = False

    def __init__(self, health=1):
        """Create an Insect with a HEALTH quantity."""
        super().__init__(health)

    @classmethod
    def construct(cls, gamestate):
        """Create an Ant for a given GameState, or return None if not possible."""
        ...

    def can_contain(self, other):
        ...

    def store_ant(self, other):
        ...

    def remove_ant(self, other):
        ...

    def add_to(self, place):
        if place.ant is None:
            place.ant = self
        else:
            assert place.ant is None or place.ant.can_contain(
                self) or self.can_contain(place.ant), 'Two ants in {0}'.format(place)
            if self.is_container and self.can_contain(place.ant):
                self.store_ant(place.ant)
                place.ant = self
            if place.ant.is_container and place.ant.can_contain(self):
                place.ant.store_ant(self)
        Insect.add_to(self, place)

    def remove_from(self, place):
        if place.ant is self:
            place.ant = None
        elif place.ant is None:
            assert False, '{0} is not in {1}'.format(self, place)
        else:
            place.ant.remove_ant(self)
        Insect.remove_from(self, place)

    def double(self):
        """Double this ants's damage, if it has not already been doubled."""
        self.damage *= 2


class HarvesterAnt(Ant):
    """HarvesterAnt produces 1 additional food per turn for the colony."""
    food_cost = 2
    name = 'Harvester'
    implemented = True

    def action(self, gamestate):
        """Produce 1 additional food for the colony.
        gamestate -- The GameState, used to access game state information.
        """
        gamestate.food += 1


class ThrowerAnt(Ant):
    """ThrowerAnt throws a leaf each turn at the nearest Bee in its range."""

    name = 'Thrower'
    implemented = True
    damage = 1
    upper_bound = float('inf')
    lower_bound = -1
    food_cost = 3

    def nearest_bee(self):
        """Return the nearest Bee in a Place that is not the HIVE, connected to
        the ThrowerAnt's Place by following entrances.

        This method returns None if there is no such Bee (or none in range).
        """
        i = 0
        iter_place = self.place
        while iter_place.entrance:
            if i > self.upper_bound:
                return None
            if not iter_place.is_hive:
                if iter_place.bees and i >= self.lower_bound:
                    return random_bee(iter_place.bees)
            i += 1
            iter_place = iter_place.entrance
        return None

    def throw_at(self, target):
        """Throw a leaf at the TARGET Bee, reducing its health."""
       ...

    ...


def random_bee(bees):
    """Return a random bee from a list of bees, or return None if bees is empty."""
    assert isinstance(bees, list), "random_bee's argument should be a list but was a %s" % type(bees).__name__
    if bees:
        return random.choice(bees)

##############
# Extensions #
##############


class ShortThrower(ThrowerAnt):
    """A ThrowerAnt that only throws leaves at Bees at most 3 places away."""

    name = 'Short'
    food_cost = 2
    implemented = True  
    upper_bound = 3


class LongThrower(ThrowerAnt):
    """A ThrowerAnt that only throws leaves at Bees at least 5 places away."""

    name = 'Long'
    food_cost = 2
    implemented = True
    lower_bound = 5


class FireAnt(Ant):
    """FireAnt cooks any Bee in its Place when it expires."""
    name = 'Fire'
    damage = 3
    food_cost = 5
    implemented = True

    def __init__(self, health=3):
        ...

    def reduce_health(self, amount):
        """Reduce health by AMOUNT, and remove the FireAnt from its place if it
        has no health remaining.

        Make sure to reduce the health of each bee in the current place, and apply
        the additional damage if the fire ant dies.
        """
        for b in list(self.place.bees):
            b.reduce_health(amount)
        if amount >= self.health:
            for i in list(self.place.bees):
                i.reduce_health(self.damage)
            super().reduce_health(amount)
        else:
            super().reduce_health(amount)

class WallAnt(Ant):

    name = 'Wall'
    damage = 0
    food_cost = 4
    implemented = True

    def __init__(self, health=4):
        super().__init__(health)
        
class HungryAnt(Ant):
    chewing_turns = 3
    name = 'Hungry'
    food_cost = 4
    implemented = True

    def __init__(self, health=1):
        super().__init__(health)
        self.turns_to_chew = 0

    def action(self, gamestate):
        if self.turns_to_chew >0:
            self.turns_to_chew -= 1
        else:
            if self.place.bees:
                eaten_bee = random_bee(self.place.bees)
                eaten_bee.reduce_health(eaten_bee.health)
                #self.place.remove_insect(insect)
                self.turns_to_chew = self.chewing_turns



class ContainerAnt(Ant):
    """
    ContainerAnt can share a space with other ants by containing them.
    """
    is_container = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ant_contained = None

    def can_contain(self, other):
        if self.ant_contained is None and not other.is_container:
            return True
        else:
            return False

    def store_ant(self, ant):
        self.ant_contained = ant

    def remove_ant(self, ant):
        if self.ant_contained is not ant:
            assert False, "{} does not contain {}".format(self, ant)
        self.ant_contained = None

    def remove_from(self, place):
        ...

    def action(self, gamestate):
        if self.ant_contained is not None:
            return self.ant_contained.action(gamestate)


class BodyguardAnt(ContainerAnt):
    """BodyguardAnt provides protection to other Ants."""

    name = 'Bodyguard'
    food_cost = 4
    implemented = True 

    def __init__(self, health=2):
        super().__init__(health)

class TankAnt(ContainerAnt):
    name = 'Tank'
    implemented = True
    damage = 1
    food_cost = 6

    def __init__(self, health=2):
        super().__init__(health)

    def action(self, gamestate):
        if self.ant_contained is not None:
            self.ant_contained.action(gamestate)
        for b in self.place.bees[:]:
            b.reduce_health(self.damage)


class Water(Place):
    """Water is a place that can only hold waterproof insects."""

    def add_insect(self, insect):
        """Add an Insect to this place. If the insect is not waterproof, reduce
        its health to 0."""
        super().add_insect(insect)
        if not insect.is_waterproof:
            insect.reduce_health(insect.health)


class ScubaThrower(ThrowerAnt):
    name = 'Scuba'
    implemented = True
    food_cost = 6
    is_waterproof = True
    

class QueenAnt(ScubaThrower):
    """The Queen of the colony. The game is over if a bee enters her place."""
    name = 'Queen'
    food_cost = 7
    implemented = True   
    is_waterproof = True

    @classmethod
    def construct(cls, gamestate):
        """
        Returns a new instance of the Ant class if it is possible to construct, or
        returns None otherwise. Remember to call the construct() method of the superclass!
        """
        if not gamestate.has_queenAnt:
            gamestate.has_queenAnt = True
            return super().construct(gamestate)
        else:
            return None

    def action(self, gamestate):
        """A queen ant throws a leaf, but also doubles the damage of ants
        in her tunnel.
        """
        super().action(gamestate)
        i = self.place.exit
        while i:
            if i.ant is not None:
                if not i.ant.doubled:
                    i.ant.doubled = True
                    i.ant.double()
                if i.ant.is_container and i.ant.ant_contained:
                    if not i.ant.ant_contained.doubled:
                        i.ant.ant_contained.doubled = True
                        i.ant.ant_contained.double()    
            i = i.exit
    def remove_from(self, place):
        return

    def reduce_health(self, amount):
        """Reduce health by AMOUNT, and if the QueenAnt has no health
        remaining, signal the end of the game.
        """
        super().reduce_health(amount)
        if self. health == 0:
            return ants_lose()


class AntRemover(Ant):
    """Allows the player to remove ants from the board in the GUI."""

    name = 'Remover'
    implemented = False

    def __init__(self):
        super().__init__(0)


class Bee(Insect):
    """A Bee moves from place to place, following exits and stinging ants."""

    name = 'Bee'
    damage = 1
    is_slowed = False
    is_scared = False
    slowed_turns = 0
    scared_turns = 0
    is_waterproof = True
    ...

    def blocked(self):
        """Return True if this Bee cannot advance to the next Place."""
        return self.place.ant is not None

    def action(self, gamestate):
        """A Bee's action stings the Ant that blocks its exit if it is blocked,
        or moves to the exit of its current place otherwise.

        gamestate -- The GameState, used to access game state information.
        """
        destination = self.place.exit
        if self.scared_turns == 0:
            self.is_scared = False
        if self.is_scared:
            destination = self.place.entrance
            self.scared_turns -= 1
        else:
            destination = self.place.exit

        if self.is_slowed:
            self.slowed_turns -= 1
            if self.slowed_turns == 0:
                self.is_slowed = False
            if gamestate.time % 2 == 0 and destination is not None and self.health > 0:
                self.move_to(destination)
            else:
                self.scared_turns += 1
    
        else:
            if self.blocked():
                self.sting(self.place.ant)
            elif self.health > 0 and destination is not None:
                self.move_to(destination)

    ...

    def slow(self, length):
        """Slow the bee for a further LENGTH turns."""
        self.slowed_turns += length
        self.is_slowed = True

    def scare(self, length):
        """
        If this Bee has not been scared before, cause it to attempt to
        go backwards LENGTH times.
        """
        if self.is_scared:
            return
        else:
            self.scared_turns += length
            self.is_scared = True


class NinjaAnt(Ant):
  ...

############
# Statuses #
############
...
