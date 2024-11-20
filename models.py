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

Author: Eric Yang (ejy29), Natan Aklilu (nta6)
Date: December 9, 2021
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
    # Attribute _sprite: a GSprite object representing the ship
    # Invariant: _sprite is a GSprite object

    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)

    # INITIALIZER TO CREATE A NEW SHIP
    def __init__(self):
        """
        Creates the ship object according to variables in constants. Makes a
        GSprite object.
        """
        self._sprite = GSprite(bottom=SHIP_BOTTOM, x=GAME_WIDTH/2,
        width=SHIP_WIDTH, height=SHIP_HEIGHT, format = (2,4), source=SHIP_IMAGE,
        frame=0)

    # METHODS TO MOVE THE SHIP AND CHECK FOR COLLISIONS
    def move(self, posx):
        """
        Moves the ship to the x position given.

        Parameter posx: the future x position of the ship
        Precondition: posx is an integer
        """
        self._sprite.x = posx

    def collides(self, bolt):
        """
        Detects whether or not the ship GSPRITE object colldies with a bolt object.

        Parameter bolt: the bolt we are detecting collision with.
        Precondition: Bolt is a bolt object.
        """
        x = bolt.get_x()
        y = bolt.get_y()
        if bolt.get_friendly():
            return False
        else:
            if self._sprite.contains((x+BOLT_WIDTH/2,y+BOLT_HEIGHT/2)) or \
            self._sprite.contains((x+BOLT_WIDTH/2,y-BOLT_HEIGHT/2)) or \
            self._sprite.contains((x-BOLT_WIDTH/2,y+BOLT_HEIGHT/2)) or \
            self._sprite.contains((x-BOLT_WIDTH/2,y-BOLT_HEIGHT/2)):
                return True

    # COROUTINE METHOD TO ANIMATE THE SHIP
    def explode(self):
        """
        Advances and creates the explosition animation. Makes a coroutine,
        and use the coroutine to advance the frames of the Gsprite object
        every time it is called through yield. Once every frame has been displayed,
        the while loop is terminated.
        """
        exploding = True
        sum = 0
        while exploding:
            dt = (yield)
            sum += dt
            state = 7*(sum/DEATH_SPEED)
            state1 = int(round(state, 0))
            if state1 > 7:
                exploding = False
            else:
                self._sprite.frame = state1

    # ADD MORE METHODS (PROPERLY SPECIFIED) AS NECESSARY
    def draw(self, view):
        """
        Draws the ship on screen.

        Parameter view: view is the screen we are drawing the ship on.
        Precondition: View is a gameapp view object.
        """
        self._sprite.draw(view)


class Alien(GSprite):
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
    #Attribute _sprite: the gsprite object representing the alien
    #Invariant: _sprite is a gsprite object.
    #
    # Attribute _alien_alive: keeps track of whether the alien is alive or dead
    # Invariant: _alien_alive is either True or False
    #
    # Attribute _death_anim: coroutine for performing the explosion animation
    # Invariant: _death_anim is a generator-based coroutine (or None)

    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def get_sprite(self):
        """
        Returns the alien sprite object
        """
        return self._sprite

    def get_x(self):
        """
        Returns the x position of the alien, an integer
        """
        return self._sprite.x

    def get_y(self):
        """
        Returns the y position of the alien, an integer
        """
        return self._sprite.y

    def get_frame(self):
        """
        Returns the current frame of the alien, an integer
        """
        return self._sprite.frame

    def set_frame(self, x):
        """
        Sets the frame of the alien to x

        Parameter: x is the desired frame
        Precondition: x is an int >=0  and <=7
        """
        self._sprite.frame = x

    def set_alien_alive(self, x):
        """
        Sets alien alive status to True or False

        Parameter: x is desired alive state
        Precondition: x is either True or False
        """
        self._alien_alive = x

    def get_alien_alive(self):
        """
        Returns alien alive status, either True or False
        """
        return self._alien_alive

    def set_death_anim(self, x):
        """
        Sets alien death animation to desired value

        Paramter: x is a coroutine for performing the alien explosion animation
        Precondition: x is a generator-based coroutine (or None)
        """
        self._death_anim = x

    def get_death_anim(self):
        """
        Returns alien death animation state, which is either True or False.
        """
        return self._death_anim

    # INITIALIZER TO CREATE AN ALIEN
    def __init__(self, x, y, image):
        """
        Intializes an alien object. creates an gsprite at the proper coordinates
        with the corect image.

        Parameter x: x is the x coordinate of the alien
        Preconditions: x is an integer such that x<=800 and x>=0

        Parameter: y is the y coordinate of the alien
        Precondition: y is an integer such that x<=800 and x>=0

        Parameter: image is str describing the file name of the image to be used.
        Precondition: image is either a str 'alien-strip1.png','alien-strip2.png'
        or 'alien-strip3.png'
        """
        self._sprite = GSprite(top=y, left=x, width=ALIEN_WIDTH,
        height=ALIEN_HEIGHT, format = (4,2), source=image, frame = 0)
        self._alien_alive = True
        self._death_anim = None

    # METHOD TO CHECK FOR COLLISION (IF DESIRED)
    def collides(self, bolt):
        """
        Checks if the alien object and bolt object occupy the same space. Returns
        True if this is the case.

        Paramter bolt: Bolt is the bolt that is checked if it collides with this
        alien object.
        Precondition: bolt is a bolt object
        """
        x=bolt.get_x()
        y=bolt.get_y()
        if not bolt.get_friendly():
            return False
        else:
            if self._sprite.contains((x+BOLT_WIDTH/2,y+BOLT_HEIGHT/2)) or \
            self._sprite.contains((x+BOLT_WIDTH/2,y-BOLT_HEIGHT/2)) or \
            self._sprite.contains((x-BOLT_WIDTH/2,y+BOLT_HEIGHT/2)) or \
            self._sprite.contains((x-BOLT_WIDTH/2,y-BOLT_HEIGHT/2)):
                return True

    # ADD MORE METHODS (PROPERLY SPECIFIED) AS NECESSARY
    def draw(self, view):
        """
        Draws the alien on screen.

        Parameter view: View is the screen we are drawing on
        Precondition: view is a gameapp object view.
        """
        self._sprite.draw(view)

    def move(self, dx=0, dy=0):
        """
        Moves the alien by dx and dy.

        Parameter dx: dx is the amount we are moving the alien along x axis
        Precondition: dx is an integer

        Parameter dy: dy is the amount we are moving the alien along the y axis
        Precondition: dy is an integer
        """
        self._sprite.x+=dx
        self._sprite.y+=dy

    def explode(self):
        """
        Handles the explosion animation. Starts up a coroutine once called, and
        advances the coroutine with yield. the animation advances by a set amount
        depending on the dt given by yield. Once the animation has gone through
        every frame, the alien stops exploding and ends the animation.
        """
        exploding=True
        sum = 0
        while exploding:
            dt=(yield)
            sum += dt
            state=6*(sum/DEATH_SPEED)
            state1=int(round(state, 0))
            if state1>6:
                exploding=False
            else:
                self._sprite.frame=state1


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

    # Attribute _laser: the laser bolt shot from the ship
    # Invariant: _laser is a GRectangle object

    # Attribute _friendly: determines whether it hurts the ship or alien
    # Invarinat: is a boolean
    # LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY


    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def get_friendly(self):
        """
        Returns if the bolt is fired by the player or not. A boolean.
        """
        return self._friendly

    def get_x(self):
        """
        Returns the laser rectangle object x position.
        """
        return self._laser.x

    def get_y(self):
        """
        Returns the y position of the rectangle object
        """
        return self._laser.y

    # INITIALIZER TO SET THE VELOCITY
    def __init__(self, vel, xval, yval, friendly):
        """
        Intializes the laser bolt by creating a GRectangle object, and setting a
        velocity to it along with alignment.

        Parameter vel: the velocity of the bolt in pixels per frame
        Precondition: vel is an integer.

        Parameter xval: the x position of the bolt
        Precondition: x is a integer

        Parameter yval: the y position of the bolt.
        Precondition: y is an integer.

        Parameter friendly: whether a bolt is fired by the player or aliens.
        True if fired by players, false if aliens.
        Precondition: friendly is a boolean
        """
        self._velocity = vel
        self._laser = GRectangle(x = xval, y = yval, width = BOLT_WIDTH,
        height = BOLT_HEIGHT, fillcolor = 'red', linecolor = 'black')
        self._friendly=friendly

    # ADD MORE METHODS (PROPERLY SPECIFIED) AS NECESSARY
    def move(self):
        """
        Move the _laser object according to the preset velocity.
        """
        self._laser.y+=self._velocity

    def off_screen(self):
        """
        Detects if the bolt is offscreen. Returns true if it is offscreen, false
        otherwise.
        """
        if self._laser.y>800+BOLT_HEIGHT or self._laser.y<0-BOLT_HEIGHT:
            return True
        else:
            return False

    def draw(self, view):
        """
        Draws the bolt _laser object.
        """
        self._laser.draw(view)
# IF YOU NEED ADDITIONAL MODEL CLASSES, THEY GO HERE
