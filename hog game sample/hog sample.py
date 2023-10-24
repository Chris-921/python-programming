"""CS 61A Presents The Game of Hog."""

from dice import six_sided, four_sided, make_test_dice
from ucb import main, trace, interact
from math import sqrt

GOAL_SCORE = 100  # The goal of Hog is to score 100 points.


def roll_dice(num_rolls, dice=six_sided):
    """Simulate rolling the DICE exactly NUM_ROLLS > 0 times. Return the sum of
    the outcomes unless any of the outcomes is 1. In that case, return 1.

    num_rolls:  The number of dice rolls that will be made.
    dice:       A function that simulates a single dice roll outcome.
    """
    # These assert statements ensure that num_rolls is a positive integer.
    assert type(num_rolls) == int, 'num_rolls must be an integer.'
    assert num_rolls > 0, 'Must roll at least once.'

    result, it = 0, 0
    hasOne = False
    while it < num_rolls:
        d = dice()
        if d == 1:
            hasOne = True
        result += d
        it += 1
    return 1 if hasOne else result


def oink_points(player_score, opponent_score):
    """Return the points scored by player due to Oink Points.

    player_score:   The total score of the current player.
    opponent_score: The total score of the other player.
    """
    oppLastDigt = opponent_score % 10
    oppSecondLastDigt = (opponent_score // 10) % 10
    oPoints = 2 * oppSecondLastDigt - oppLastDigt
    if oPoints <= 1:
        return 1
    else:
        return oPoints


def take_turn(num_rolls, player_score, opponent_score, dice=six_sided, goal=GOAL_SCORE):
    """Simulate a turn rolling NUM_ROLLS dice,
    which may be 0 in the case of a player using Oink Points.
    Return the points scored for the turn by the current player.

    num_rolls:       The number of dice rolls that will be made.
    player_score:    The total score of the current player.
    opponent_score:  The total score of the opponent.
    dice:            A function that simulates a single dice roll outcome.
    goal:            The goal score of the game.
    """
    # Leave these assert statements here; they help check for errors.
    assert type(num_rolls) == int, 'num_rolls must be an integer.'
    assert num_rolls >= 0, 'Cannot roll a negative number of dice in take_turn.'
    assert num_rolls <= 10, 'Cannot roll more than 10 dice.'
    assert max(player_score, opponent_score) < goal, 'The game should be over.'
    if num_rolls == 0:
        return oink_points(player_score, opponent_score)
    else:
        return roll_dice(num_rolls, dice)


def is_prime(n):
    if n == 2:
        return True
    elif n % 2 == 0:
        return False
    i = 3
    while i <= sqrt(n):
        if n % i == 0:
            return False
        i += 2
    return True


def pigs_on_prime(player_score, opponent_score):
    """Return the points scored by the current player due to Pigs on Prime.


    player_score:   The total score of the current player.
    opponent_score: The total score of the other player.
    """

    if is_prime(player_score):
        additional = 1
        while not is_prime(player_score + additional):
            additional += 1
        return additional
    else:
        return 0


def next_player(who):
    ...


def silence(score0, score1, leader=None):
    ...


def play(strategy0, strategy1, score0=0, score1=0, dice=six_sided,
         goal=GOAL_SCORE, say=silence):
    """Simulate a game and return the final scores of both players, with Player
    0's score first, and Player 1's score second.

    A strategy is a function that takes two total scores as arguments (the
    current player's score, and the opponent's score), and returns a number of
    dice that the current player will roll this turn.

    strategy0:  The strategy function for Player 0, who plays first.
    strategy1:  The strategy function for Player 1, who plays second.
    score0:     Starting score for Player 0
    score1:     Starting score for Player 1
    dice:       A function of zero arguments that simulates a dice roll.
    goal:       The game ends and someone wins when this score is reached.
    say:        The commentary function to call every turn.
    """
    who = 0  # Who is about to take a turn, 0 (first) or 1 (second)
    leader = None
    while score0 < goal and score1 < goal:
        if who == 0:
            turnScore = take_turn(strategy0(score0, score1),
                                  score0, score1, dice, goal)
            score0 += turnScore
            score0 += pigs_on_prime(score0, score1)
        else:
            turnScore = take_turn(strategy1(score1, score0),
                                  score1, score0, dice, goal)
            score1 += turnScore
            score1 += pigs_on_prime(score1, score0)
        who = next_player(who)
        leader, message = say(score0, score1, leader)
        if message != None and message != "":
            print(message)
    return score0, score1


def say_scores(score0, score1, player=None):
    ...


def announce_lead_changes(score0, score1, last_leader=None):
    """A commentary function that announces when the leader has changed.

    >>> leader, message = announce_lead_changes(5, 0)
    >>> print(message)
    Player 0 takes the lead by 5
    >>> leader, message = announce_lead_changes(5, 12, leader)
    >>> print(message)
    Player 1 takes the lead by 7
    >>> leader, message = announce_lead_changes(8, 12, leader)
    >>> print(leader, message)
    1 None
    >>> leader, message = announce_lead_changes(8, 13, leader)
    >>> leader, message = announce_lead_changes(15, 13, leader)
    >>> print(message)
    Player 0 takes the lead by 2
    """
    if score0 > score1:
        curtLeader = 0
    elif score1 > score0:
        curtLeader = 1
    else:
        curtLeader = None

    if curtLeader == last_leader:
        return curtLeader, print(end="")
    if curtLeader == None:
        return curtLeader, print(end="")
    if curtLeader != last_leader:
        return curtLeader, f'Player {curtLeader} takes the lead by {abs(score0-score1)}'


def both(f, g):
    ...


def always_roll(n):
    ...


def make_averaged(original_function, total_samples=1000):
    """Return a function that returns the average value of ORIGINAL_FUNCTION
    called TOTAL_SAMPLES times.

    To implement this function, you will have to use *args syntax, a new Python
    feature introduced in this project.  See the project description.

    >>> dice = make_test_dice(4, 2, 5, 1)
    >>> averaged_dice = make_averaged(roll_dice, 1000)
    >>> averaged_dice(1, dice)
    3.0
    """
    def avg(*args):
        it_avg, total_avg = 0, 0
        while it_avg < total_samples:
            it_avg += 1
            total_avg += original_function(*args)
        return total_avg / total_samples
    return avg


def max_scoring_num_rolls(dice=six_sided, total_samples=1000):
    """Return the number of dice (1 to 10) that gives the highest average turn score
    by calling roll_dice with the provided DICE a total of TOTAL_SAMPLES times.
    Assume that the dice always return positive outcomes.

    >>> dice = make_test_dice(1, 6)
    >>> max_scoring_num_rolls(dice)

    """
    i, max_roll_num, res = 1, 0, 1
    while i <= 10:
        roll_num = make_averaged(roll_dice, total_samples)
        max_i = roll_num(i, dice)
        if max_i > max_roll_num:
            max_roll_num = max_i
            res = i
        i += 1
    return res


def winner(strategy0, strategy1):
    ...


def average_win_rate(strategy, baseline=always_roll(6)):
    ...


def run_experiments():
    ...


def oink_points_strategy(score, opponent_score, threshold=8, num_rolls=6):
    """This strategy returns 0 dice if that gives at least THRESHOLD points, and
    returns NUM_ROLLS otherwise.
    """
    if oink_points(score, opponent_score) >= threshold:
        return 0
    else:
        return num_rolls


def pigs_on_prime_strategy(score, opponent_score, threshold=8, num_rolls=6):
    """This strategy returns 0 dice when this would result in Pigs on Prime taking
    effect. It also returns 0 dice if it gives at least THRESHOLD points.
    Otherwise, it returns NUM_ROLLS.
    """
    if oink_points(score, opponent_score) >= threshold or pigs_on_prime(score+oink_points(score, opponent_score), opponent_score) > 0:
        return 0
    elif pigs_on_prime(score+oink_points(score, opponent_score), opponent_score) == 0:
        return num_rolls
    else:
        return num_rolls


def final_strategy(score, opponent_score):
    return 6


@main
def run(*args):
    """Read in the command-line argument and calls corresponding functions."""
    import argparse
    parser = argparse.ArgumentParser(description="Play Hog")
    parser.add_argument('--run_experiments', '-r', action='store_true',
                        help='Runs strategy experiments')
    args = parser.parse_args()

    if args.run_experiments:
        run_experiments()
