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

Author: Eric Yang (ejy29), Natan Aklilu (nta6)
Date: December 9, 2021
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

    All of the attributes of this class ar to be hidden. You may find that
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
    # Attribute _shipx: the x position of the ship.
    # Invariant: _shipx is an int >=0 and < GAME_WIDTH
    #
    # Attribute _polarity: The direction the ships are moving in
    # Invariant: _polarity is an integer either -1 or 1
    #
    # Attribute _alien_steps: The steps the aliens have taken
    # Invariant: _alien_steps is an integer>-1
    #
    # Attribute _ship_alive: keeps track of whether ship is not dead
    # Invariant: _ship_alive is either True or False
    #
    # Attribute _death_anim: coroutine for performing the explosion animation
    # Invariant: _death_anim is a generator-based coroutine (or None)
    #
    # Attribute _state: keeps track of game state
    # Invariant: _state is a string of either 'play', 'lose', or 'win'
    #
    # You may change any attribute above, as long as you update the invariant
    # You may also add any new attributes as long as you document them.
    # LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY

    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def get_game_state(self):
        """
        Returns: self._state
        """
        return self._state

    def set_game_state(self, x):
        """
        Sets self._state to x

        Parameter: x describes the game state
        Preconditions: self._state is a str 'play', 'lose', or 'win'
        """
        self._state = x

    def getLives(self):
        """
        Returns: self._lives
        """
        return self._lives

    def setShipAlive(self):
        """
        Sets the variable self._ship_alive to True
        """
        self._ship_alive = True

    # INITIALIZER (standard form) TO CREATE SHIP AND ALIENS
    def __init__(self):
        """
        Intilizes the application. Creates the aliens, ships, defense line, and
        sets all the invariants properly. Called only once to start up the game
        """
        self.create_aliens()
        self.create_ship()
        self.create_dline()
        self._time=0
        self._polarity=1
        self._bolts=[]
        self._alien_steps=0
        self._ship_alive=True
        self._death_anim=None
        self._state='play'
        self._lives = SHIP_LIVES

    def create_aliens(self):
        """
        Creates the aliens according to the variables in consts. Fills the list
        self._aliens with alien objects. Only ran once,
        and called by __init__.
        """
        self._aliens = []
        current_x = 0
        current_y = 0
        for y in range(1, ALIEN_ROWS+1):
            self._aliens.append([])
            if y%6==1 or y%6==0:
                source = ALIEN_IMAGES[0]
            elif y%6==2 or y%6==3:
                source = ALIEN_IMAGES[1]
            elif y%6==4 or y%6==5:
                source = ALIEN_IMAGES[2]
            current_y = ALIEN_CEILING+(y-1)*(ALIEN_V_SEP+ALIEN_HEIGHT)
            for x in range(ALIENS_IN_ROW):
                current_x = ALIEN_H_SEP+x*(ALIEN_H_SEP+ALIEN_WIDTH)
                self._aliens[y-1].append(Alien(current_x, GAME_HEIGHT-current_y,
                source))

    def create_ship(self):
        """
        Creates the ship according to the variables in consts by assinging
        self._ship to a ship object. called by __init__ and called every time
        the player continues.
        """
        self._shipx = GAME_WIDTH/2
        self._ship = Ship()

    def create_dline(self):
        """
        Creates the defense line by drawing one on screen. called once by init.
        """
        self._dline=GPath(points = [0, DEFENSE_LINE, GAME_WIDTH, DEFENSE_LINE],
        linewidth = 1, linecolor = 'black')

    # UPDATE METHOD TO MOVE THE SHIP, ALIENS, AND LASER BOLTS
    def update(self, input, dt):
        """
        Updates the game objects every time it is called, including aliens,
        ship, bolts. Handles all aspects of the game using mostly helper methods.

        Parameter input: an input object that allows us to detect keystrokes
        Precondition: input is a GameAPP input object

        Parameter dt: the time passed since the last time update was called
        Precondition: dt a float such that dt>=0.
        """
        self._time += dt
        self.defense_line_death()
        self.ship_actions(dt, input)
        self.alien_death(dt)
        if self._ship_alive==True:
            self.alien_shoot()
        self.clear_lasers()
        self.game_collision()

    def defense_line_death(self):
        """
        Causes the game to be lost when an alien crosses the defense line. Finds
        the lowest alien, then determines if the alien is lower than the defense
        line. Ends the game if this is the case by setting the ship to dead. Ran
        every time update is called.
        """
        lowest=GAME_HEIGHT
        for x in self._aliens:
            for y in x:
                if y == None or y.get_alien_alive() == False:
                    pass
                elif y.get_y() < lowest:
                    lowest = y.get_y()
        if lowest-ALIEN_HEIGHT/2 <= DEFENSE_LINE:
            self._lives=0
            self.ship_death()

    def ship_actions(self, dt, input):
        """
        Updates ship attributes ship alive status. Either does nothing if ship
        is None, takes in input to move and fire ship, or triggers death
        animation.

        Parameter input: an input object that allows us to detect keystrokes
        Precondition: input is a GameAPP input object

        Parameter dt: the time passed since the last time update was called
        Precondition: dt a float such that dt>=0.
        """
        if self._ship == None:
            pass
        elif self._ship_alive:
            self.ship_input(input)
        elif self._death_anim == None:
            self._death_anim = self._ship.explode()
            next(self._death_anim)
        else:
            try:
                self._death_anim.send(dt)
            except:
                self.ship_death()

    def ship_input(self, input):
        """
        Moves ship based on user input.

        Parameter input: an input object that allows us to detect keystrokes
        Precondition: input is a GameAPP input object
        """
        if input.is_key_down('right'):
            if ((self._shipx+5) > (0+SHIP_WIDTH/2) and
            (self._shipx+5) < (800-SHIP_WIDTH/2)):
                self._shipx += 5
        if input.is_key_down('left'):
            if ((self._shipx-5) > (0+SHIP_WIDTH/2) and
            (self._shipx-5) < (800-SHIP_WIDTH/2)):
                self._shipx -= 5
        if input.is_key_down('spacebar'):
            fire = True
            for laser in self._bolts:
                if laser.get_friendly() == True:
                    fire = False
            if fire == True:
                self._bolts.append(Bolt(BOLT_SPEED, self._shipx,
                SHIP_BOTTOM+SHIP_HEIGHT, True))

    def ship_death(self):
        """
        Called when the ship finishes its death animation. Removes a life,
        sets the game to loss, and deletes the ship object along with cleaning
        up the self._bolts folder. Called by update.
        """
        self._death_anim = None
        self._ship = None
        self._lives += -1
        self._state = 'lose'
        self._ship_alive = True
        for x in self._bolts:
            self._bolts.remove(x)

    def alien_death(self, dt):
        """
        Method that checks all aliens and triggers alien explosion animation for
        each alien that is dead and is not None

        Parameter dt: the time passed since the last time update was called
        Precondition: dt a float such that dt>=0.
        """
        xpos = -1
        for x in self._aliens:
            xpos += 1
            ypos = -1
            for y in x:
                ypos += 1
                if y != None and y.get_alien_alive() == False:
                    self.alien_death_anim(y, dt, xpos, ypos)

    def alien_shoot(self):
        """
        controls the alien shooting. Find a random column of aliens, picks the
        lowest alien in that column, and creates a bolt object at that alien
        firing downwards. Ran every time update is called.
        """
        try:
            if self._time >= ALIEN_SPEED:
                self.alien_move()
                self._alien_steps += 1
                if self._alien_steps == BOLT_RATE:
                    self._alien_steps = 0
                    column_list = []
                    for x in self._aliens:
                        for y in x:
                            if y==None or y.get_alien_alive() == False:
                                pass
                            elif y.get_x() not in column_list:
                                column_list.append(y.get_x())
                    firing = random.randint(0, len(column_list)-1)
                    lowest = GAME_HEIGHT
                    for x in self._aliens:
                        for y in x:
                            if y == None or y.get_alien_alive() == False:
                                pass
                            elif (y.get_y() < lowest and
                            y.get_x() == column_list[firing]):
                                lowest = y.get_y()
                    self._bolts.append(Bolt(-BOLT_SPEED, column_list[firing],
                    lowest, False))
        except:
            pass

    def alien_move(self):
        """
        Moves the aliens. Checks if the aliens can move left/right depending on
        self._polarity and if the alien is alive.
        If there is space, move them. If not, change the polairty
        and move the aliens downwards. Called every update.
        """
        rightmost =- 1
        leftmost = GAME_WIDTH
        down = False
        for x in self._aliens:
            for y in x:
                if y == None:
                    pass
                elif y.get_x() > rightmost:
                    rightmost = y.get_x()
        for x in self._aliens:
            for y in x:
                if y == None:
                    pass
                elif y.get_x() < leftmost:
                    leftmost = y.get_x()
        self.move_options(rightmost, leftmost, down)

    def move_options(self, rightmost, leftmost, down):
        """
        Moves aliens using given values to check whether aliens are moving into
        the wall on either side. If it is the wall, function moves down then
        reverses direction.

        Parameter: rightmost is the x position of the alien furthest right
        Precondition: rightmost is an int >= 0 and <= GAME_WIDTH

        Parameter: leftmost is the x position of the alien furthest left
        Precondition: leftmost is an int >= 0 and <= GAME_WIDTH

        Paramater: down keeps track of whether aliens move down against wall
        Precondition: down is either True or False
        """
        if rightmost == -1:
            self._state='win'
        elif ((rightmost+ALIEN_H_WALK*self._polarity)>
        (GAME_WIDTH-(ALIEN_H_SEP+ALIEN_WIDTH/2)) or
        (leftmost+ALIEN_H_WALK*self._polarity)<
        (ALIEN_H_SEP+ALIEN_WIDTH/2)):
            self._polarity = self._polarity*-1
            down=True
        for x in self._aliens:
            for y in x:
                if y == None:
                    pass
                elif y.get_alien_alive() == True:
                    self._time = 0
                    if down == False:
                        y.move(ALIEN_H_WALK*self._polarity)
                    else:
                        y.move(0, -ALIEN_V_WALK)
                    if y.get_frame() == 0:
                        y.set_frame(1)
                    elif y.get_frame() == 1:
                        y.set_frame(0)

    def alien_death_anim(self, y, dt, xpos, ypos):
        """
        Called every time an alien is detected to be dead. Changes the alien
        sprite to the death animation state using set_death_anim, then
        advances it continually using get_death_anim.send(dt) until the animation
        is done, at which this function deletes the aline. Called by update.

        Parameter y: an object in the _alien list
        Precondition: y is an alien object or is None

        Parameter dt: the time that has passed since the last time update was called
        Precondition: dt a float such that dt>=0.

        Parameter xpos: the x position of the alien object in 2d list _alien
        Precondition: xpos is an integer such that xpos>=0

        Parameter ypos: the y position of the alien object in the 2d list _alien
        Precondition: ypos is an integer such that ypos>=0
        """
        if y == None:
            pass
        elif y.get_death_anim() == None:
            y.set_death_anim(y.explode())
            next(y.get_death_anim())
        else:
            try:
                y.get_death_anim().send(dt)
            except:
                y.set_death_anim(None)
                self._aliens[xpos][ypos]=None

    def clear_lasers(self):
        """
        Method that removes any lasers that are off screen
        """
        for laser in self._bolts:
            laser.move()
            if laser.off_screen()==True:
                self._bolts.remove(laser)

    # DRAW METHOD TO DRAW THE SHIP, ALIENS, DEFENSIVE LINE AND BOLTS
    def draw(self, view):
        """
        Draws the game objects into view. Called by app directly.

        Parameter view: the viewscreen to be drawn on
        Precondition: view is a gameapp object view.
        """
        for x in range(len(self._aliens)):
            for y in self._aliens[x]:
                if y == None:
                    pass
                else:
                    y.draw(view)
        self._ship.move(self._shipx)
        self._ship.draw(view)
        self._dline.draw(view)
        for laser in self._bolts:
            laser.draw(view)

    # HELPER METHODS FOR COLLISION DETECTION
    def game_collision(self):
        """
        Handles all game collisions between bolts and aliens, along with bolts
        and the ship. Kills the aliens and the ship by calling setters or setting
        the ship to death directly. Called by update.
        """
        if self._ship == None:
            pass
        else:
            for x in self._bolts:
                if self._ship_alive:
                    if self._ship.collides(x):
                        self._bolts.remove(x)
                        self._ship_alive=False
        for x in self._bolts:
            for y  in self._aliens:
                for z in y:
                    if z == None:
                        pass
                    elif z.collides(x) and z.get_alien_alive()==True:
                        try:
                            self._bolts.remove(x)
                        except:
                            pass
                        z.set_alien_alive(False)
