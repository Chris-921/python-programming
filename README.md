# python-programming

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

---

Language: Python

Compiler: Visual Studio Code

Author: Zilong Guo

Date: Jun - Aug 2022

---

** This repo only includes sample code and algorithms written by Zilong. The project ideas are from the UCB CS61A class.
