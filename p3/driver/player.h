#ifndef __PLAYER_H_
#define __PLAYER_H_

#include "hand.h"


class Player {
    // A virtual base class, providing the player interface
protected:
    Team team; // The team of each member, either SOS Brigade or Stardust Crusaders
    int ID; // The ID of each member.
    string name; // The full name of each member.

public:
    virtual int bet(unsigned int bankroll,
        unsigned int minimum) = 0;
    // REQUIRES: bankroll >= minimum
    // EFFECTS: returns the player's bet, between minimum and bankroll 
    // inclusive

    virtual bool draw(Card dealer,             // Dealer's "up card"
        const Hand& player) = 0; // Player's current hand
    // EFFECTS: returns true if the player wishes to be dealt another
    // card, false otherwise.

    virtual void expose(Card c) = 0;
    // EFFECTS: allows the player to "see" the newly-exposed card.
    // For example, each card that is dealt "face up" is exposed, i.e. expose().
    // Likewise, if the dealer must show his "hole card", it is also exposed, i.e.
    // expose().  Note: not all cards dealt are exposed, i.e. expose()---if the
    // player goes over 21 or is dealt a natural 21, the dealer need
    // not expose his hole card.

    virtual void shuffled() = 0;
    // EFFECTS: tells the player that the deck has been re-shuffled.

    virtual string getName();
    // EFFECTS: get the name of the player.

    virtual int getID();
    // EFFECTS: get the ID of the player.

    virtual Team getTeam();
    // EFFECTS: get the team of the player.

    virtual void setPlayer(Team tm, int id);
    // EFFECTS: set a member's name, ID and team
    // MODIFIES: name, ID, team

    virtual ~Player() { }
    // Note: this is here only to suppress a compiler warning.
    //       Destructors are not needed for this project.
};

extern Player* get_Player(string& dealerSide, string& playerType, int& ID);
    // EFFECTS: get a pointer to a player.
    // "dealerSide" describes whether the dealer is from 
    // SOS Brigade or Stardust Crusade. 
    // This depends on the last program argument: [sos|sc]. 
    // sc means the dealer team is Stardust Crusaders, 
    // sos means the dealer team is SOS Brigade.
    // "playerType" describes whether Koizumi Itzuki and 
    // Mohammed Avdol are simple player or count player. 
    // This depends on the penultimate program argument: [simple|counting]. 
    // If this argument is "simple", then Itzuki and Avdol are simple players. 
    // If this argument is "counting", then Itzuki and Avdol are countingplayers. 
    // "ID" is the player's ID.

#endif /* __PLAYER_H__ */
