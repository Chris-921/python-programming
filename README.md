## Introduction 
 
Welcome to the Abstraction Techniques for Program Complexity Management repository. This project focuses on advanced abstraction techniques that play a fundamental role in managing and simplifying program complexity.

---

## Key Abstraction Techniques Covered

Techniques include procedural abstraction; control abstraction using recursion, higher-order functions, generators, and streams; data abstraction using interfaces, objects, classes, and generic operators; and language abstraction using interpreters and macros.

---

## Project Description

#### Hog game:
In Hog, two players alternate turns trying to be the first to end a turn with at least 100 total points. On each turn, the current player chooses some number of dice to roll, up to 10. That player's score for the turn is the sum of the dice outcomes. However, a player who rolls too many dice risks:
 * Sow Sad. If any of the dice outcomes is a 1, the current player's score for the turn is 1.
Example 1: The current player rolls 7 dice, 5 of which are 1's. They score 1 point for the turn.
Example 2: The current player rolls 4 dice, all of which are 3's. Since Sow Sad did not occur, they scored 12 points for the turn.

In a normal game of Hog, those are all the rules. To spice up the game, we'll include some special rules:
 * Oink Points. A player who chooses to roll zero dice scores 2 * tens - ones, or 1, whichever is higher; where tens, and ones are the tens and ones digits of the opponent's score
Example 1: The opponent has 46 points, and the current player chooses to roll zero dice. 2 * 4 - 6 = 2; which is greater than 1, so the current player gains 2 points.
Example 2: The opponent has 73 points, and the current player chooses to roll zero dice. 2 * 7 - 3 = 11; which is greater than 1, so the current player gains 11 points.
Example 3: The opponent has 27 points, and the current player chooses to roll zero dice. 2 * 2 - 7 = -3; which is less than or equal to 1, so the current player gains 1 point.
Example 4: The opponent has 7 points, and the current player chooses to roll zero dice. 2 * 0 - 7 = -7; which is less than or equal to 1, so the current player gains 1 point.

 * Pigs on Prime. If, after rolling, the current player's score is a prime number, they gain enough points such that their score instantly increases to the next prime number
Example:
  Both players start out at 0. (0, 0)
  Player 0 rolls 2 dice and gets 5 points. (5, 0)
  5 is a prime number, so Player 0 instantly gains two points, so that their score increases to 7 (7, 0)
  Player 1 then takes their turn.

#### Cat game:
A program that measures typing speed. Additionally, it will implement typing autocorrect, which is a feature that attempts to correct the spelling of a word after a user types it. This project is inspired by typeracer.

Part 1: Typing

Part 2: Autocorrect

Part 3: Multiplayer

demo: https://cats.cs61a.org/  

#### Ant game:
In this project, I created a tower defense game called Ants Vs. SomeBees. As the ant queen, you populate your colony with the bravest ants you can muster. Your ants must protect their queen from the evil bees that invade your territory. Irritate the bees enough by throwing leaves at them, and they will be vanquished. Fail to pester the airborne intruders adequately, and your queen will succumb to the bees' wrath. This game is inspired by PopCap Games' Plants Vs. Zombies.

* rules:
  
A game of Ants Vs. SomeBees consists of a series of turns. In each turn, new bees may enter the ant colony. Then, new ants are placed to defend their colony. Finally, all insects (ants, then bees) take individual actions. Bees either try to move toward the end of the tunnel or sting ants in their way. Ants perform a different action depending on their type, such as collecting more food or throwing leaves at the bees. The game ends either when a bee reaches the end of the tunnel (you lose), the bees destroy the QueenAnt if it exists (you lose), or the entire bee fleet has been vanquished (you win).

* concepts:
  
The Colony. This is where the game takes place. The colony consists of several Places that are chained together to form a tunnel where bees can travel through. The colony also has some quantity of food which can be expended in order to place an ant in a tunnel.

Places. A place links to another place to form a tunnel. The player can put a single ant into each place. However, there can be many bees in a single place.

The Hive. This is the place where bees originate. Bees exit the beehive to enter the ant colony.

Ants. Players place an ant into the colony by selecting from the available ant types at the top of the screen. Each type of ant takes a different action and requires a different amount of colony food to place. The two most basic ant types are the HarvesterAnt, which adds one food to the colony during each turn, and the ThrowerAnt, which throws a leaf at a bee each turn. You will be implementing many more!

Bees. In this game, bees are the antagonistic forces that the player must defend the ant colony from. Each turn, a bee either advances to the next place in the tunnel if no ant is in its way, or it stings the ant in its way. Bees win when at least one bee reaches the end of a tunnel.

#### Card game：
This game is inspired by the similarly named Magic: The Gathering. The goals of this are to practice object-oriented programming as well as to try implementing a shorter game than some of the other projects in this repo.

* rules:

There are two players. Each player has a hand of cards and a deck, and at the start of each round, each player draws a random card from their deck. If a player's deck is empty when they try to draw, they will automatically lose the game.

Cards have a name, an attack value, and a defense value. Each round, each player chooses one card to play from their own hands. The cards' power values are then calculated and compared. The card with the higher power wins the round. Each played card's power value is calculated as follows:

(player card's attack) - (opponent card's defense)

For example, let's say Player 1 plays a card with 2000 attack and 1000 defense and Player 2 plays a card with 1500 attack and 3000 defense. Their cards' powers are calculated as:

P1: 2000 - 3000 = 2000 - 3000 = -1000
P2: 1500 - 1000 = 1500 - 1000 = 500
So Player 2 would win this round.

The first player to win 8 rounds wins the match!

---

Language: Python

Compiler: Visual Studio Code

Author: Zilong Guo

Date: Jun - Aug 2022

---

** This repo only includes sample code and algorithms written by Zilong. The project ideas are from the UCB CS61A class.
