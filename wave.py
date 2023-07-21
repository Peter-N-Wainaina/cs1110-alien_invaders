"""
Subcontroller module for Alien Invaders

This module contains the subcontroller to manage a single level or wave in
the Alien Invaders game.  Instances of Wave represent a single wave. Whenever
you move to a new level, you are expected to make a new instance of the class.

The subcontroller Wave manages the ship, the aliens and any laser bolts on
screen. These are model objects.  Their classes are defined in models.py.

Most of your work on this assignment will be in either this module or
models.py. Whether a helper method belongs in this module or models.py is
often a complicated issue.  If you do not know, ask on Piazza and we will
answer.

Peter Ng'ang'a Wainaina pnw6
Iman Kiio iwk4
6th December 2021
"""
from game2d import *
from consts import *
from models import *
import random

# PRIMARY RULE: Wave can only access attributes in models.py via getters/setters
# Wave is NOT allowed to access anything in app.py (Subcontrollers are not
# permitted to access anything in their parent. To see why, take CS 3152)


class Wave(object):
    """
    This class controls a single level or wave of Alien Invaders.

    This subcontroller has a reference to the ship, aliens, and any laser bolts
    on screen. It animates the laser bolts, removing any aliens as necessary.
    It also marches the aliens back and forth across the screen until they are
    all destroyed or they reach the defense line (at which point the player
    loses). When the wave is complete, you  should create a NEW instance of
    Wave (in Invaders) if you want to make a new wave of aliens.

    If you want to pause the game, tell this controller to draw, but do not
    update.  See subcontrollers.py from Lecture 24 for an example.  This
    class will be similar to than one in how it interacts with the main class
    Invaders.

    All of the attributes of this class are to be hidden. You may find that
    you want to access an attribute in class Invaders. It is okay if you do,
    but you MAY NOT ACCESS THE ATTRIBUTES DIRECTLY. You must use a getter
    and/or setter for any attribute that you need to access in Invaders.
    Only add the getters and setters that you need for Invaders. You can keep
    everything else hidden.

    """
    # HIDDEN ATTRIBUTES:
    # Attribute _ship: the player ship to control
    # Invariant: _ship is a Ship object or None
    #
    # Attribute _aliens: the 2d list of aliens in the wave
    # Invariant: _aliens is a rectangular 2d list containing Alien objects or None
    #
    # Attribute _bolts: the laser bolts currently on screen
    # Invariant: _bolts is a list of Bolt objects, possibly empty
    #
    # Attribute _dline: the defensive line being protected
    # Invariant : _dline is a GPath object
    #
    # Attribute _lives: the number of lives left
    # Invariant: _lives is an int >= 0
    #
    # Attribute _time: the amount of time since the last Alien "step"
    # Invariant: _time is a float >= 0s
    #
    # You may change any attribute above, as long as you update the invariant
    # You may also add any new attributes as long as you document them.
    # LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY

    #Attribute _movement: horizontal alien motion
    #Invariant: _movement is a string, either "right" or "left"
    #
    #Attribute _fireRate: number of steps to take before next alien bolt
    #Invariant :_fireRate is an int in  1..BOLT_RATE
    #
    #Attribute _alienSteps : number of steps by aliens since last bolt was fired
    #Invariant :_alienSteps is an int greater >=0
    #
    # Attribute _animator: A coroutine for performing an animation
    # Invariant: _animator is a generator-based coroutine (or None)
    #
    #Attribute _shipDestroyed: whether existing ship is destroyed
    #Invariant: _shipDestroyed is a boolean
    #
    #Attribute _playerWon: whether the player has won
    #Invariant: _playerWon is either a boolean indicating endgame or None as game progresses
    #
    #Attribute _playerScore: current player score
    #Invariant :_playerScore is and int>=0

    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def isShipDestroyed(self):
        """
        Returns True if the ship is destroyed, False otherwise
        """
        return self._shipDestroyed

    def resetShipDestroyed(self):
        """
        Sets _shipDestroyed to False
        """
        self._shipDestroyed=False

    def isLifeLeft(self):
        """
        Returns  True is _lives is greater than 0 False otherwise
        """
        return self._lives>0

    def getLives(self):
        """
        Returns the number of player lives left
        """
        return self._lives

    def createNewShip(self):
        """
        Creates a new Ship object at the original position
        """
        self._ship=Ship()

    def hasPlayerWon(self):
        """
        Return True if player has won, False if player has lost, or None if game is not over yet
        """
        return self._playerWon

    def getScore(self):
        """
        Return the current player Score
        """
        return (self._playerScore*10)

    # INITIALIZER (standard form) TO CREATE SHIP AND ALIENS
    #helper for drawing aliens

    def __init__(self):
        """
        Initializes a new Wave object
        """
        self._aliens=self.create_aliens()
        self._ship=Ship()
        self._dline=GPath(linewidth=2,points=[0,DEFENSE_LINE,800,DEFENSE_LINE],linecolor="black")
        #no animation, hence time zero
        self._time=0
        #aliens start at right edge hence moving right
        self._movement="right"
        #at start, no bolts
        self._bolts=[]
        # at the start, randomize firing chance
        self._fireRate=random.randint(1,BOLT_RATE)
        #no steps so far
        self._alienSteps=0
        #animator isn't running
        self._animator=None
        #ship not destroyed yet
        self._shipDestroyed=False
        #lives full at the start
        self._lives=SHIP_LIVES
        #player hasn't won yet
        self._playerWon=None
        #no score yet
        self._playerScore=0

    # UPDATE METHOD TO MOVE THE SHIP, ALIENS, AND LASER BOLTS
    def update(self,input,dt):
        """
        Animates a single frame in the wave

        Parameter input: The input from the User
        Precondition: input must be an instance of GInput

        Parameter dt: The time in seconds since last update
        Precondition: dt is a number (int or float)
        """
        assert isinstance(input,GInput)
        assert isinstance(dt,int) or isinstance(dt,float)

        if not self._animator is None:
            try:
                self._animator.send(dt)
            except StopIteration:
                self._shipDestroyed=True
                self._animator=None
                self._ship=None
                self._bolts.clear()
        else:
            #move ship
            if not self._ship is None:
                self._move_ship(input)
                self._fire(input)
        #move aliens and maybe fire
        if self._aliens_exist():
            self._move_aliens(dt)
        #move bolts
        self._move_bolt()
        #check for colision
        self._collides()
        #check game ending
        self._checkEnd()

    # DRAW METHOD TO DRAW THE SHIP, ALIENS, DEFENSIVE LINE AND BOLTS
    def draw(self,view):
        """
        Draws the game objects to the view

        Parameter view: The view on which to draw the game objects
        Precondition: view must be an instance of GView
        """
        assert isinstance(view,GView)
        #draw ship
        if not self._ship is None:
            self._ship.draw(view)
        #draw defensive line
        self._dline.draw(view)
        #draw aliens
        for row in range (len(self._aliens)):
            for alien in self._aliens[row]:
                if not alien is None:
                    alien.draw(view)
        #draw bolts
        for bolt in self._bolts:
            bolt.draw(view)

    # HELPER METHODS FOR COLLISION DETECTION
    #helper for drawing aliens
    def create_aliens(self):
        """
        Returns a 2-D list of Alien Objects
        Helper function to initialize _aliens
        """
        #accumulator for all aliens
        aliens=[]
        y=GAME_HEIGHT-ALIEN_CEILING
        for row in range (ALIEN_ROWS):
            #find image to use based on row
            if row%2==0:
                image=((row+1)//2)%len(ALIEN_IMAGES)
            else:
                image=((row)//2)%len(ALIEN_IMAGES)
            #accumulator for aliens on one column
            alien_columns=[]
            #position of first Alien
            x=ALIEN_H_SEP+(ALIEN_WIDTH/2)

            for column in range(ALIENS_IN_ROW):
                alien_columns.append(Alien(x,y,image))
                #calculate x position of next Alien
                x+=(ALIEN_H_SEP+ALIEN_WIDTH)
            #calculate y coordinate of next row
            y-=(ALIEN_HEIGHT+ALIEN_V_SEP)
            aliens.append(alien_columns)

        return aliens

    def _move_ship(self,input):
        """
        Moves the ship left or right as specified by player via input

        Parameter input:User Input
        Precondition: input must be an instance of GInput
        """
        #asserts
        assert isinstance(input,GInput)
        #ship wraps around screen
        if self._ship.x>(GAME_WIDTH-(0.5*SHIP_WIDTH)):
            self._ship.x=0.5*SHIP_WIDTH
        elif self._ship.x<0.5*SHIP_WIDTH:
            self._ship.x=GAME_WIDTH-(0.5*SHIP_WIDTH)
        else:
            if input.is_key_down("right"):
                self._ship.x+=SHIP_MOVEMENT
            if input.is_key_down("left"):
                self._ship.x-=SHIP_MOVEMENT

    def _move_aliens(self,dt):
        """
        Moves the aliens

        Parameter dt: Time since the last update
        Precondition:dt must be a number(int or float)
        """
        assert isinstance(dt,int) or isinstance(dt,float)

        if self._alienSteps==self._fireRate:
            #reset steps
            self._alienSteps=0
            #randomize and reset fire rate
            self._fireRate=random.randint(1,BOLT_RATE)
            #get x and y co-coordinate
            bolt_pos=self._alien_to_fire()
            self._bolts.append(Bolt(bolt_pos[0],(bolt_pos[1]-(ALIEN_HEIGHT/2+BOLT_HEIGHT/2)),-BOLT_SPEED))
        #move  bolt
        if self._movement=="right":
            self._aliens_forward(dt)
        if self._movement=="left":
            self._aliens_back(dt)

    def _aliens_forward(self,dt):
        """
        Moves the existing aliens forward, i.e to the right

        Parameter dt: Time since the last update
        Precondition:dt must be a number(int or float)
        """
        assert isinstance(dt,int) or isinstance(dt,float)

        self._time+=dt
        if self._time>ALIEN_SPEED:
            #increase alien steps and reset time
            self._alienSteps+=1
            self._time=0
            #move all aliens
            for row in self._aliens:
                for alien in row:
                    if not alien is None:
                        alien.x+=ALIEN_H_WALK
        #determine whether to move down
        right_alien=self._right_most_alien()
        if (GAME_WIDTH-(right_alien.x+ALIEN_WIDTH/2))<ALIEN_H_SEP:
            self._movement="left"
            self._move_down()

    def _aliens_back(self,dt):
        """
        Moves the existing  aliens back i.e (to the left)

        Parameter dt: Time since the last update
        Precondition:dt must be a number(int or float)
        """
        assert isinstance(dt,int) or isinstance(dt,float)

        self._time+=dt

        if self._time>ALIEN_SPEED:
            #add alien steps and reset time
            self._alienSteps+=1
            self._time=0
            #move all aliens
            for row in self._aliens:
                for alien in row:
                    if not alien is None:
                        alien.x-=ALIEN_H_WALK
        #determine whether to move down
        left_alien=self._left_most_alien()
        if  ALIEN_H_SEP>(left_alien.x-ALIEN_WIDTH/2):
            self._movement="right"
            self._move_down()

    def _right_most_alien(self):
        """
        Returns any one existing alien in the right most column
        """
        for row in reversed(self._reverse_aliens()):
            for alien in row:
                if not alien is None:
                    return alien

    def _left_most_alien(self):
        """
        Returns any one existing alien in the left most column
        """
        for row in self._reverse_aliens():
            for alien in row:
                if not alien is None:
                    return alien

    def _reverse_aliens(self):
        """
        Returns a 2-D list of _aliens with the rows and columns swapped
        """
        reverse=[]
        for column in range(ALIENS_IN_ROW):
            columns=[]
            for row in self._aliens:
                columns.append(row[column])
            reverse.append(columns)
        return reverse


    def _move_down(self):
        """
        Moves all existing aliens down by the specified amount, i.e ALIEN_V_WALK
        """
        for row in self._aliens:
            for alien in row:
                if not alien is None:
                    alien.y-=ALIEN_V_WALK

    def _fire(self,input):
        """
        Fires a bolt from the player

        Parameter input: The input from the User
        Precondition: input is an instance of GInput
        """
        assert isinstance(input,GInput)
        if input.is_key_down("up"):
            fire=True
            for bolt in self._bolts:
                if bolt.isPlayerBolt():
                    fire =False
            if fire:
                self._bolts.append(Bolt(self._ship.x,(self._ship.y+SHIP_HEIGHT/2+BOLT_HEIGHT/2),BOLT_SPEED))

    def _move_bolt(self):
        """
        Moves all existing bolts in _bolts
        """
        for bolt in self._bolts:
            if bolt.isPlayerBolt():
                bolt.y+=(bolt.getVelocity()+bolt.height/2)
                if (bolt.y-BOLT_HEIGHT/2)>GAME_HEIGHT:
                    self._bolts.remove(bolt)
            else:
                bolt.y+=(bolt.getVelocity()-bolt.height/2)
                if (bolt.y+BOLT_HEIGHT/2)<0:
                    self._bolts.remove(bolt)

    def _alien_to_fire(self):
        """
        Returns a 1-D list of the current  x and y positions of a random alien in the bottom most row
        """
        alien=None
        while alien is None:
            column=random.randint(0,ALIENS_IN_ROW)
            for row in reversed(self._aliens):
                    try:
                        if not row[column] is None:
                            alien=row[column]
                            return [alien.x,alien.y]
                    except IndexError:
                        alien=None

    def _collides(self):
        """
        Checks if there is an alien bolt , or a player bolt and calls appropriate helpers to check for collision.
        """
        player_bolt=None
        #to check for even one alien bolt
        alien_bolt=None
        for bolt in self._bolts:
            if bolt.isPlayerBolt():
                player_bolt=bolt
            else:
                alien_bolt=bolt

        #check that there is at least one alien
        if not player_bolt is None and self._aliens_exist():
            self._alien_collides(player_bolt)

        if not alien_bolt is None and not self._ship is None:
            self._ship_collides()

    def _aliens_exist(self):
        """
        Returns True if there is at least one Alien in _aliens, False otherwise
        """
        aliens_exist=False
        for row in self._aliens:
            for alien in row:
                if not alien is None:
                    aliens_exist=True
        return aliens_exist

    def _alien_collides(self,player_bolt):
        """
        Checks if any Alien has collided with a player bolt. Removes the bolt if collision occurs. Updates _playerScore

        Parameter player_bolt: Player bolt to check for collision with
        Precondition: player_bolt is an instance of Bolt, and must be a player_bolt
        """
        assert isinstance(player_bolt,Bolt)
        assert player_bolt.isPlayerBolt()

        for row in self._aliens:
            for alien  in range(len(row)):
                if not row[alien] is None and row[alien].collides(player_bolt):
                    row[alien]=None
                    self._bolts.remove(player_bolt)
                    self._playerScore+=1

    def _ship_collides(self):
        """
        Checks if the ship collides with any Alien bolt.Removes the bolt if collision occurs. Updates _lives.
        """
        for bolt in self._bolts:
            if not bolt.isPlayerBolt() and self._ship.collides(bolt):
                self._animator=self._animate_death()
                next(self._animator)
                self._bolts.remove(bolt)
                self._lives-=1

    def _animate_death(self):
        """
        Coroutine for animating the ship explosion
        """
        #time spent animating so far
        time_passed=0
        #error for frame selection
        err=0.1
        animating=True

        while animating:
            dt=(yield)
            time_passed+=dt
            value=(time_passed/DEATH_SPEED)*self._ship.getCount()
            for frame in range(1,self._ship.getCount()):
                if (abs(value-frame))<=err:
                    self._ship.setFrame(frame)
                    if self._ship.getFrame()==self._ship.getCount()-1:
                        animating=False

    def _checkEnd(self):
        """
        Check if the game is over. Updates _playerWon as appropriate
        """
        #check player win
        win=True
        for row in self._aliens:
            for alien in row:
                if not alien is None:
                    win=False
        if win:
            self._playerWon=win
        #loss
        #check defense line breach
        breach=False
        for row in self._aliens:
            for alien in row:
                if not alien is None and (alien.y-ALIEN_HEIGHT/2)<=DEFENSE_LINE:
                    breach=True
        if breach:
            self._playerWon= not breach
        #check zero lives
        if self._lives==0:
            self._playerWon=False
