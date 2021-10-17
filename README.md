
# Table of Contents

1.  [What is this?](#org4bfc5bc)
2.  [Next Steps](#org04242bc)
        1.  [Add round to dealer object](#org8342041)



<a id="org4bfc5bc"></a>

# What is this?

This is an attempt at building a poker simulator (five-card stud) in
Python.  It began as an attempt to get better at Python, but ended
up as an attempt to become better at software engineering.

The code is pretty rigourously unit-tested, but has no documentation
(in contrast to other work, which has docs but is not well unit-tested). 

I've ended up learning a bunch of stuff about Python, managing
complexity and TDD (along with property based testing and linting). 

This is a side-project, so by definition is not done.

That being said, I'm reasonably close to being able to run a betting
round between n players and one dealer. 

One day, if I have time <sup><a id="fnr.1" class="footref" href="#fn.1">1</a></sup>, I hope to get this working with my
objected-oriented design, and expose a Gym API so that I could try
RL alogorithms on it. That would be cool, and if it ever happens, I
promise to update this README within six months of the date of that happening! 


<a id="org04242bc"></a>

# Next Steps


<a id="org8342041"></a>

### DONE Add round to dealer object

1.  DONE small blind

2.  DONE large blind

3.  DONE deal cards to players

    1.  DONE Wrap up all of these functions into a start round one, which returns players with Hands

4.  DONE send players state so they can decide action

    -   have player decide on action based on state
    -   internal state (cards held)
    -   external state (position, pot value, actions of other players)

5.  DONE Fix hand API

    -   have a hand class
    -   also have a bunch of functions that act on hand objects
    -   should join them together in holy matrimony/encapsulation
    
    1.  TODO deal\_cards apparently isn't used anywhere, delete

6.  Player Updates

    1.  Change player function names to calculate\_bet, call etc
    
    2.  DONE Make use of state object to decide action

7.  Dealer Updates

    1.  DONE Add dealer get action function
    
    2.  Add dealer logic for round structure
    
    3.  DONE Add dealing of cards to start\_round

8.  Deck Object

    1.  Move discard pile to deck object
    
    2.  Move replenish\_cards and update\_cards to dealer object

9.  Round Structure

    1.  bet/call/fold in order
    
        -   Almost done, just need to handle the case where all but one player folds
    
    2.  discard cards
    
    3.  get new cards
    
    4.  bet/call/fold in order
    
    5.  finish round
    
        -   award pot
        -   reset deck and cards
        -   log player/dealer state

10. Card API

    1.  TODO change equality function to make 10H and 10S equal
    
        -   Use this to simplify logic in hand scoring etc
        -   note that gt method and eq method are very different (gt only uses
            rank)

11. Hand API

    1.  DONE Fix Set[Card] issue
    
        -   I only added this to make hypothesis work, but it's ugly and stupid
        -   Fix the hypothesis test so that the type can be List[Card]
        -   move logic in <span class="underline"><span class="underline">init</span></span> to separate function (validate\_hand)
        
        1.  TODO Fix hand equality
        
            -   If same cards are in different order, will return False incorrectly
            -   in general, it's impossible for two hands to be equal as it requires
                the exact same cards
            -   This is clearly impossible
        
        2.  TODO make sure that <span class="underline"><span class="underline">iter</span></span> and <span class="underline"><span class="underline">next</span></span> actually work (they look kinda weird)


# Footnotes

<sup><a id="fn.1" href="#fnr.1">1</a></sup> i recently had a child, it's unlikely that I'll have this time
