#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2
import bleach


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    DB = psycopg2.connect("dbname=tournament")
    c = DB.cursor()
    c.execute("delete from matches")
    DB.commit()
    DB.close()

    """Remove all the match records from the database."""


def deletePlayers():
    """Remove all the player records from the database."""
    DB = psycopg2.connect("dbname=tournament")
    c = DB.cursor()
    c.execute("delete from players")
    DB.commit()
    DB.close()

def countPlayers():
    """Returns the number of players currently registered."""
    DB = psycopg2.connect("dbname=tournament")
    c = DB.cursor()
    c.execute("select count(*) from players")
    num = c.fetchall()
    DB.commit()
    DB.close()
    return num[0][0]


def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    cleanname = bleach.clean(name)
    DB = psycopg2.connect("dbname=tournament")
    c = DB.cursor()
    c.execute("insert into players (name) values(%s)",(cleanname,))
    DB.commit()
    DB.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    DB = psycopg2.connect("dbname=tournament")
    c = DB.cursor()
    c.execute("select * from standings")
    standings = c.fetchall() 
    DB.commit()
    DB.close()
    return standings


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    cleanwinner = bleach.clean(winner)
    cleanloser = bleach.clean(loser)
    DB = psycopg2.connect("dbname=tournament")
    c = DB.cursor()
    c.execute("insert into matches (winid, loseid) values(%s, %s)",(cleanwinner, cleanloser, ))
    DB.commit()
    DB.close()
 
 
def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    DB = psycopg2.connect("dbname=tournament")
    c = DB.cursor()
    c.execute("select standingsodd.id, standingsodd.name, standingseven.id, standingseven.name from standingseven join standingsodd on (standingsodd.row + 1) = standingseven.row;")
    pairings = c.fetchall() 
    DB.commit()
    DB.close()
    return pairings




