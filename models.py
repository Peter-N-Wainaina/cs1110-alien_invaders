"""
Models module for Alien Invaders

This module contains the model classes for the Alien Invaders game. Anything
that you interact with on the screen is model: the ship, the laser bolts, and
the aliens.

Just because something is a model does not mean there has to be a special
class for it. Unless you need something special for your extra gameplay
features, Ship and Aliens could just be an instance of GImage that you move
across the screen. You only need a new class when you add extra features to
an object. So technically Bolt, which has a velocity, is really the only model
that needs to have its own class.

With that said, we have included the subclasses for Ship and Aliens. That is
because there are a lot of constants in consts.py for initializing the
objects, and you might want to add a custom initializer.  With that said,
feel free to keep the pass underneath the class definitions if you do not want
to do that.

You are free to add even more models to this module.  You may wish to do this
when you add new features to your game, such as power-ups.  If you are unsure
about whether to make a new class or not, please ask on Piazza.

Peter Ng'ang'a Wainaina pnw6
Iman Kiio iwk4
6th December 2021
"""
from consts import *
from game2d import *

# PRIMARY RULE: Models are not allowed to access anything in any module other
# than consts.py.  If you need extra information from Gameplay, then it should
# be a parameter in your method, and Wave should pass it as a argument when it
# calls the method.


class Ship(GSprite):
    """
    A class to represent the game ship.

    At the very least, you want a __init__ method to initialize the ships
    dimensions. These dimensions are all specified in consts.py.

    You should probably add a method for moving the ship.  While moving a
    ship just means changing the x attribute (which you can do directly),
    you want to prevent the player from moving the ship offscreen.  This
    is an ideal thing to do in a method.

    You also MIGHT want to add code to detect a collision with a bolt. We
    do not require this.  You could put this method in Wave if you wanted to.
    But the advantage of putting it here is that Ships and Aliens collide
    with different bolts.  Ships collide with Alien bolts, not Ship bolts.
    And Aliens collide with Ship bolts, not Alien bolts. An easy way to
    keep this straight is for this class to have its own collision method.

    However, there is no need for any more attributes other than those
    inherited by GImage. You would only add attributes if you needed them
    for extra gameplay features (like animation).
    """
    #  IF YOU ADD ATTRIBUTES, LIST THEM BELOW

    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)

    def setFrame(self,frame):
        """
        Sets the current frame of the GSprite to frame

        Parameter frame : The current frame of the ship in the GSprite
        Precondition: frame must be an int>=0
        """
        assert isinstance(frame, int) and frame>=0
        self.frame=frame

    def getFrame(self):
        """
        Returns the current frame of the ship in the GSprite
        """
        return self.frame

    def getCount(self):
        """
        Returns the number of images in the ship GSprite
        """
        return self.count

    # INITIALIZER TO CREATE A NEW SHIP
    def __init__(self,x_c=GAME_WIDTH/2,y_c=(SHIP_BOTTOM+(0.5*SHIP_HEIGHT))):
        """
        Initializes the ship

        Parameter x_c:The x-coordinate to center the  middle  of the ship image in the Game Window
        Precondition:x_c must be a number (int or float) and GAME_WIDTH>=x_c>=0

        Parameter y_c:The y-coordinate to center the  middle  of the ship image in the Game Window
        Precondition:y_c must be a number (int or float) and GAME_HEIGHT>=x_c>=0
        """
        #assert statements
        assert isinstance(x_c,float) or isinstance(x_c,int) and x_c>=0 and x_c<=GAME_WIDTH
        assert isinstance(y_c,float) or isinstance(y_c,int) and y_c>=0 and y_c<=GAME_HEIGHT

        super().__init__(width=SHIP_WIDTH,height=SHIP_HEIGHT,x=x_c,y=y_c,source=SHIP_IMAGE,format=(2,3))

    # METHODS TO MOVE THE SHIP AND CHECK FOR COLLISIONS
    def collides(self,bolt):
        """
        Returns True if an alien bolt collides with the ship

        This method returns False if bolt was not fired by an alien.

        Parameter bolt: The laser bolt to check
        Precondition: bolt is of class Bolt
        """
        #asserts
        assert isinstance(bolt,Bolt)

        bolt_edges=[(bolt.x-BOLT_WIDTH/2,bolt.y-BOLT_HEIGHT/2),(bolt.x+BOLT_WIDTH/2,bolt.y-BOLT_HEIGHT/2),(bolt.x-BOLT_WIDTH/2,bolt.y+BOLT_HEIGHT/2),(bolt.x+BOLT_WIDTH/2,bolt.y+BOLT_HEIGHT/2)]

        for edge in bolt_edges :
            collides=False
            if self.contains(edge) and not bolt.isPlayerBolt():
                collides=True
        return collides

    # COROUTINE METHOD TO ANIMATE THE SHIP
    # ADD MORE METHODS (PROPERLY SPECIFIED) AS NECESSARY


class Alien(GImage):
    """
    A class to represent a single alien.

    At the very least, you want a __init__ method to initialize the alien
    dimensions. These dimensions are all specified in consts.py.

    You also MIGHT want to add code to detect a collision with a bolt. We
    do not require this.  You could put this method in Wave if you wanted to.
    But the advantage of putting it here is that Ships and Aliens collide
    with different bolts.  Ships collide with Alien bolts, not Ship bolts.
    And Aliens collide with Ship bolts, not Alien bolts. An easy way to
    keep this straight is for this class to have its own collision method.

    However, there is no need for any more attributes other than those
    inherited by GImage. You would only add attributes if you needed them
    for extra gameplay features (like giving each alien a score value).
    """
    #  IF YOU ADD ATTRIBUTES, LIST THEM BELOW
    #_alien: an alien image
    #invariant: _alien should be an instance of GImage

    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)

    # INITIALIZER TO CREATE AN ALIEN
    def __init__(self,x_c,y_c,s):
        """
        Initializes alien dimensions and position


        Parameter x_c:The x-coordinate to center the  middle  of the alien image in the Game Window
        Precondition:x_c must be a number (int or float) and GAME_WIDTH>=x_c>=0

        Parameter y_c:The y-coordinate to center the  middle  of the bolt image in the Game Window
        Precondition:y_c must be a number (int or float) and GAME_HEIGHT>=x_c>=0

        parameter:s,the index of the image in ALIEN_IMAGES
        precondition:must be an int, must be a valid index of the tuple ALIEN_IMAGES
        """
        assert isinstance(s,int) and s<len(ALIEN_IMAGES) and s>=-len(ALIEN_IMAGES)
        assert isinstance(x_c,float) or isinstance(x_c,int) and x_c>=0 and x_c<=GAME_WIDTH
        assert isinstance(y_c,float) or isinstance(y_c,int) and y_c>=0 and y_c<=GAME_HEIGHT

        super().__init__(width=ALIEN_WIDTH,height=ALIEN_HEIGHT,x=x_c,y=y_c,source=ALIEN_IMAGES[s])
        #self._alien=GImage(x=x_c,y=y_c,source=ALIEN_IMAGES[s])


    # METHOD TO CHECK FOR COLLISION (IF DESIRED)
    def collides(self,bolt):
        """
        Returns True if the player bolt collides with this alien

        This method returns False if bolt was not fired by the player.

        Parameter bolt: The laser bolt to check
        Precondition: bolt is of class Bolt
        """
        #asserts
        assert isinstance(bolt,Bolt)

        bolt_edges=[(bolt.x-BOLT_WIDTH/2,bolt.y-BOLT_HEIGHT/2),(bolt.x+BOLT_WIDTH/2,bolt.y-BOLT_HEIGHT/2),(bolt.x-BOLT_WIDTH/2,bolt.y+BOLT_HEIGHT/2),(bolt.x+BOLT_WIDTH/2,bolt.y+BOLT_HEIGHT/2)]

        collide=False
        for edge in bolt_edges:
            if self.contains(edge) and bolt.isPlayerBolt():
                collide=True
        return collide

    # ADD MORE METHODS (PROPERLY SPECIFIED) AS NECESSARY


class Bolt(GRectangle):
    """
    A class representing a laser bolt.

    Laser bolts are often just thin, white rectangles. The size of the bolt
    is determined by constants in consts.py. We MUST subclass GRectangle,
    because we need to add an extra (hidden) attribute for the velocity of
    the bolt.

    The class Wave will need to look at these attributes, so you will need
    getters for them.  However, it is possible to write this assignment with
    no setters for the velocities.  That is because the velocity is fixed and
    cannot change once the bolt is fired.

    In addition to the getters, you need to write the __init__ method to set
    the starting velocity. This __init__ method will need to call the __init__
    from GRectangle as a  helper.

    You also MIGHT want to create a method to move the bolt.  You move the
    bolt by adding the velocity to the y-position.  However, the getter
    allows Wave to do this on its own, so this method is not required.
    """
    # INSTANCE ATTRIBUTES:
    # Attribute _velocity: the velocity in y direction
    # Invariant: _velocity is an int or float

    # LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY


    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def getVelocity(self):
        """
        Returns the current velocity of the bolt
        """
        return self._velocity

    def isPlayerBolt(self):
        """
        Return True if bolt velocity >0 False otherwise
        """
        return self._velocity>0


    # INITIALIZER TO SET THE VELOCITY
    def __init__(self,x_c,y_c,v):
        """
        Initializes a new Bolt

        Parameter x_c:The x-coordinate to center the  middle  of the bolt image in the Game Window
        Precondition:x_c must be a number (int or float) and GAME_WIDTH>=x_c>=0

        Parameter y_c:The y-coordinate to center the  middle  of the bolt image in the Game Window
        Precondition:y_c must be a number (int or float) and GAME_HEIGHT>=x_c>=0

        Parameter:v The velocity of the bolt
        Precondition: v is an number(int or float)

        """
        #asserts
        assert isinstance(x_c,float) or isinstance(x_c,int) and x_c>=0 and x_c<=GAME_WIDTH
        assert isinstance(y_c,float) or isinstance(y_c,int) and y_c>=0 and y_c<=GAME_HEIGHT
        assert isinstance(v,int) or isinstance(v,float)

        if v>0:
            color="cyan"
        else:
            color="red"
        super().__init__(x=x_c,y=y_c,width=BOLT_WIDTH,height=BOLT_HEIGHT,fillcolor=color,linewidth=1)
        self._velocity=v


    # ADD MORE METHODS (PROPERLY SPECIFIED) AS NECESSARY


# IF YOU NEED ADDITIONAL MODEL CLASSES, THEY GO HERE
