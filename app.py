"""
Primary module for Alien Invaders

This module contains the main controller class for the Alien Invaders app.
There is no need for any additional classes in this module.  If you need
more classes, 99% of the time they belong in either the wave module or the
models module. If you are unsure about where a new class should go, post a
question on Piazza.

Peter Ng'ang'a Wainaina pnw6
Iman Kiio iwk4
6th December 2021
"""
from consts import *
from game2d import *
from wave import *


# PRIMARY RULE: Invaders can only access attributes in wave.py via getters/setters
# Invaders is NOT allowed to access anything in models.py

class Invaders(GameApp):
    """
    The primary controller class for the Alien Invaders application

    This class extends GameApp and implements the various methods necessary
    for processing the player inputs and starting/running a game.

        Method start begins the application.

        Method update either changes the state or updates the Play object

        Method draw displays the Play object and any other elements on screen

    Because of some of the weird ways that Kivy works, you SHOULD NOT create
    an initializer __init__ for this class.  Any initialization should be done
    in the start method instead.  This is only for this class.  All other
    classes behave normally.

    Most of the work handling the game is actually provided in the class Wave.
    Wave should be modeled after subcontrollers.py from lecture, and will
    have its own update and draw method.

    The primary purpose of this class is to manage the game state: which is
    when the game started, paused, completed, etc. It keeps track of that in
    an internal (hidden) attribute.

    For a complete description of how the states work, see the specification
    for the method update.

    Attribute view: the game view, used in drawing
    Invariant: view is an instance of GView (inherited from GameApp)

    Attribute input: user input, used to control the ship or resume the game
    Invariant: input is an instance of GInput (inherited from GameApp)
    """
    # HIDDEN ATTRIBUTES:
    # Attribute _state: the current state of the game represented as an int
    # Invariant: _state is one of STATE_INACTIVE, STATE_NEWWAVE, STATE_ACTIVE,
    # STATE_PAUSED, STATE_CONTINUE, STATE_COMPLETE, or STATE_NEWGAME
    #
    # Attribute _wave: the subcontroller for a single wave, managing aliens
    # Invariant: _wave is a Wave object, or None if there is no wave currently
    # active. It is only None if _state is STATE_INACTIVE.
    #
    # Attribute _text: the currently active message
    # Invariant: _text is a GLabel object, or None if there is no message to
    # display. It is only None if _state is STATE_ACTIVE.

    #
    # You may have new attributes if you wish (you might want an attribute to
    # store any score across multiple waves). But you must document them.

    # LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    #
    #Attribute _lives: Message displaying Player Lives
    #Invariant: _lives is a Glabel object only displayed during STATE_ACTIVE or None in all other states
    #
    #Attribute _score:Message displaying player score
    #Invariant :_score is a Glabel object displayed during STATE_ACTIVE or None in all other states
    #
    #Attribute _time:Total since  last update call in STATE_PAUSED
    #Invariant: _time is time in seconds

    # DO NOT MAKE A NEW INITIALIZER!

    # THREE MAIN GAMEAPP METHODS
    def start(self):
        """
        Initializes the application.

        This method is distinct from the built-in initializer __init__ (which
        you should not override or change). This method is called once the
        game is running. You should use it to initialize any game specific
        attributes.

        This method should make sure that all of the attributes satisfy the
        given invariants. When done, it sets the _state to STATE_INACTIVE and
        create a message (in attribute _text) saying that the user should press
        to play a game.
        """
        # IMPLEMENT ME
        self._state=STATE_INACTIVE
        self._text=None
        self._time=0
        self._wave=None
        self._score=None
        self._lives=None


    def update(self,dt):
        """
        Animates a single frame in the game.

        It is the method that does most of the work. It is NOT in charge of
        playing the game.  That is the purpose of the class Wave. The primary
        purpose of this game is to determine the current state, and -- if the
        game is active -- pass the input to the Wave object _wave to play the
        game.

        As part of the assignment, you are allowed to add your own states.
        However, at a minimum you must support the following states:
        STATE_INACTIVE, STATE_NEWWAVE, STATE_ACTIVE, STATE_PAUSED,
        STATE_CONTINUE, and STATE_COMPLETE.  Each one of these does its own
        thing and might even needs its own helper.  We describe these below.

        STATE_INACTIVE: This is the state when the application first opens.
        It is a paused state, waiting for the player to start the game.  It
        displays a simple message on the screen. The application remains in
        this state so long as the player never presses a key.  In addition,
        this is the state the application returns to when the game is over
        (all lives are lost or all aliens are dead).

        STATE_NEWWAVE: This is the state creates a new wave and shows it on
        the screen. The application switches to this state if the state was
        STATE_INACTIVE in the previous frame, and the player pressed a key.
        This state only lasts one animation frame before switching to
        STATE_ACTIVE.

        STATE_ACTIVE: This is a session of normal gameplay.  The player can
        move the ship and fire laser bolts.  All of this should be handled
        inside of class Wave (NOT in this class).  Hence the Wave class
        should have an update() method, just like the subcontroller example
        in lecture.

        STATE_PAUSED: Like STATE_INACTIVE, this is a paused state. However,
        the game is still visible on the screen.

        STATE_CONTINUE: This state restores the ship after it was destroyed.
        The application switches to this state if the state was STATE_PAUSED
        in the previous frame, and the player pressed a key. This state only
        lasts one animation frame before switching to STATE_ACTIVE.

        STATE_COMPLETE: The wave is over, and is either won or lost.

        You are allowed to add more states if you wish. Should you do so, you should
        describe them here.

        STATE_NEWGAME:The game is over, and new game is being started, state changes to STATE_INACTIVE, and starts all over again

        Parameter dt: The time in seconds since last update
        Precondition: dt is a number (int or float)
        """
        # IMPLEMENT ME
        #check if key was pressed and change state

        if self._state==STATE_INACTIVE:
            self._inactive()

        if self._state==STATE_NEWWAVE:
            self._new_wave()

        if self._state==STATE_ACTIVE:
            self._active(dt)

        if self._state==STATE_PAUSED:
            self._paused()

        if self._state==STATE_COMPLETE:
            self._complete()

        if self._state==STATE_NEWGAME:
            self._new_game(dt)


    def draw(self):
        """
        Draws the game objects to the view.

        Every single thing you want to draw in this game is a GObject.  To
        draw a GObject g, simply use the method g.draw(self.view).  It is
        that easy!

        Many of the GObjects (such as the ships, aliens, and bolts) are
        attributes in Wave. In order to draw them, you either need to add
        getters for these attributes or you need to add a draw method to
        class Wave.  We suggest the latter.  See the example subcontroller.py
        from class.
        """
        # IMPLEMENT ME
        if self._state==STATE_NEWWAVE or self._state==STATE_ACTIVE:
            self._wave.draw(self.view)
            self._lives.draw(self.view)
            self._score.draw(self.view)

        else:
            try:
                self._text.draw(self.view)
            except:
                pass

    # HELPER METHODS FOR THE STATES GO HERE
    def _inactive(self):
        """
        Helper method for STATE_INACTIVE

        Assigns the current text to _text, and changes state to STATE_NEWWAVE if specified key is pressed
        """
        self._text=GLabel(text="Press S to play",x=GAME_WIDTH/2,y=GAME_HEIGHT/2,font_name="Arcade.ttf",font_size=64)

        if  self.input.is_key_down('s'):
            self._state=STATE_NEWWAVE

    def _new_wave(self):
        """
        Helper method for STATE_NEWWAVE
        Creates a new wave object. Changes state to STATE_ACTIVE
        """
        self._wave=Wave()
        self._state=STATE_ACTIVE

    def _active(self,dt):
        """
        Helper method for STATE_ACTIVE
        Assigns appropriate texts to _lives and _score. Calls update method in _wave
        Changes state to STATE_COMPLETE if game over

        Parameter dt :The time in seconds since last update
        Precondition: dt is a number (int or float)
        """
        #assert preconditions
        assert isinstance(dt,float) or isinstance(dt,int)
        #assign _lives
        self._lives=GLabel(x=GAME_WIDTH-MESSAGE_WIDTH,y=GAME_HEIGHT-MESSAGE_HEIGHT,font_name="Arcade.ttf",font_size=40)
        #get current lives from _wave
        self._lives.text="Lives:"+" "+str(self._wave.getLives
        ())
        #assign _score
        self._score=GLabel(y=GAME_HEIGHT-MESSAGE_HEIGHT,x=MESSAGE_WIDTH,font_name="Arcade.ttf",font_size=40)
        #get current score from _wave
        self._score.text="Score:"+" "+str(self._wave.getScore())
        #call update method in _wave
        self._wave.update(self.input,dt)
        #if game is over, change state
        if  not self._wave.hasPlayerWon() is None:
            self._state=STATE_COMPLETE
        #if ship is blown up, change state as appropriate
        if self._wave.isShipDestroyed():
            if self._wave.isLifeLeft():
                self._state=STATE_PAUSED
            else:
                self._state=STATE_COMPLETE

    def _paused(self):
        """
        Helper method for STATE_PAUSED
        Changes state to state active as instructed by the user
        """
        #assign new text to _text
        self._text=GLabel(text="Press S to Continue",x=GAME_WIDTH/2,y=GAME_HEIGHT/2,font_name="Arcade.ttf",font_size=64)
        #change state if specified key is pressed
        if  self.input.is_key_down('s'):
            self._state=STATE_ACTIVE
            self._wave.createNewShip()
            self._wave.resetShipDestroyed()

    def _complete(self):
        """
        Helper Method for STATE_COMPLETE
        Changes state to STATE_NEWGAME  and displays messages as appropriate
        """
        if self._wave.hasPlayerWon()==True:
            self._text=GLabel(text="Congratulations",x=GAME_WIDTH/2,y=GAME_HEIGHT/2,font_name="Arcade.ttf",font_size=64)
        else:
            self._text=GLabel(text="Sorry.You Lose!!!",x=GAME_WIDTH/2,y=GAME_HEIGHT/2,font_name="Arcade.ttf",font_size=64)

        self._state=STATE_NEWGAME

    def _new_game(self,dt):
        """
        Helper for STATE_NEWGAME

        Parameter dt:Time in seconds since the last update
        Precondition:dt must be a number (int or float)
        """
        assert isinstance(dt,int) or isinstance(dt,float)
        self._time+=dt
        #change text about 2 seconds  after completion
        if abs(self._time-2)<0.1:
            self._text=GLabel(text="Initializing New Game",x=GAME_WIDTH/2,y=GAME_HEIGHT/2,font_name="Arcade.ttf",font_size=64)

        #start new game after approximately another two  seconds and reset _time
        if abs(self._time-4)<0.1:
            self._state=STATE_INACTIVE
            self._time=0
