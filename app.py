"""
Primary module for Alien Invaders

This module contains the main controller class for the Alien Invaders app.
There is no need for any additional classes in this module.  If you need
more classes, 99% of the time they belong in either the wave module or the
models module. If you are unsure about where a new class should go, post a
question on Piazza.

Author: Eric Yang (ejy29), Natan Aklilu (nta6)
Date: December 9, 2021
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
    # STATE_PAUSED, STATE_CONTINUE, or STATE_COMPLETE
    #
    # Attribute _wave: the subcontroller for a single wave, managing aliens
    # Invariant: _wave is a Wave object, or None if there is no wave currently
    # active. It is only None if _state is STATE_INACTIVE.
    #
    # Attribute _text: the currently active message
    # Invariant: _text is a GLabel object, or None if there is no message to
    # display. It is onl None if _state is STATE_ACTIVE.
    #
    # You may have new attributes if you wish (you might want an attribute to
    # store any score across multiple waves). But you must document them.
    # LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    #
    # Attribute _lastkeys: last keys pressed
    # Invariant: _lastkeys starts at 0
    #
    # Attribute _lives: keeps track of ship lives left
    # Invariant: _lives is an int >= 0 and <=3
    #
    # Attribute _textLives: text to display lives left
    # Invariant: _textLives is a GLabel
    #
    # Attribute _textSupport: text to encourage user to continue
    # Invariant: _textSupport is a GLabel
    #
    # Attribute _textAgain: text to prompt user to play again
    # Invariant: _textAgain is a GLabel
    #
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
        self._text = None
        self._wave = None
        self._state = STATE_INACTIVE
        self._lastkeys = 0
        self._text = GLabel(text="Press 'S' to Play", font_size = 60,
        font_name = "Arcade", x = GAME_WIDTH/2, y = GAME_HEIGHT/2)

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

        Parameter dt: The time in seconds since last update
        Precondition: dt is a number (int or float)
        """
        if self._state == STATE_INACTIVE:
            self.state_inactive()
        if self._state == STATE_NEWWAVE:
            self.state_new_wave()
        if self._state == STATE_ACTIVE:
            self.state_active(dt)
        if self._state == STATE_PAUSED:
            self.state_paused(dt)
        if self._state == STATE_CONTINUE:
            self.state_continue()
        if self._state == STATE_COMPLETE:
            self.state_complete()
            self.state_inactive()

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
        if self._text != None:
            self._text.draw(self.view)
        if self._state == STATE_ACTIVE:
            self._wave.draw(self.view)
            self._textLives.draw(self.view)
        if self._state == STATE_COMPLETE:
            self._textAgain.draw(self.view)
            self._textSupport.draw(self.view)

    # HELPER METHODS FOR THE STATES GO HERE
    def state_inactive(self):
        """
        Ran by update if the state is inactive. checks if the key 's' is pressed.
        if it is pressed, starts up the game by removing text and setting the _state
        to STATE NEWWAVE. Ran before the game starts.
        """
        if self.keys_pressed():
            if self.input.is_key_down('s'):
                self._state = STATE_NEWWAVE
                self._text = None
                self._textLives = GLabel(text = "Lives: 3", font_size = 30,
                font_name = "Arcade", x = GAME_WIDTH*9/10,
                y = GAME_HEIGHT*9/10)

    def state_new_wave(self):
        """
        Ran by update if the state is NEW_WAVE. Creates a wave object, and sets the
        state to STATE_ACTIVE. Only ran once when the game starts up.
        """
        self._wave = Wave()
        self._state = STATE_ACTIVE

    def state_active(self, dt):
        """
        Ran by update if the state is STATE_ACTIVE. exectues the update method within
        _wave every time unless a win or lose state is reached, in which case
        the game is either paused or complete depending on lives and
        get_game_state. Ran constantly while the game is active.
        """
        self._wave.update(self.input, dt)
        if self._wave.get_game_state() =='lose':
            if self._wave.getLives() > 0:
                self._state = STATE_PAUSED
            else:
                self._state=STATE_COMPLETE
        elif self._wave.get_game_state() == 'win':
            self._state=STATE_COMPLETE

    def state_paused(self, dt):
        """
        Ran by the update if the state is STATE_PAUSED. gives players the prompt
        to press 's', and detects if s is pressed in which case the game is
        started again by setting the state to STATE_CONTINUE. Occurs after the
        player dies and has lives.
        """
        self._text = GLabel(text = "Press 'S' to Continue", font_size = 60,
        font_name = "Arcade", x = GAME_WIDTH/2, y = GAME_HEIGHT/2)
        self._wave.update(self.input, dt)
        if self.keys_pressed():
            if self.input.is_key_down('s'):
                self._state = STATE_CONTINUE

    def state_continue(self):
        """
        Ran by the update if the state is STATE_CONTINUE. Creates a new ship,
        set the game state, and sets the state to STATE_ACTIVE.
        Only ran once after each time the game exits
        STATE_PAUSED.
        """
        self._wave.create_ship()
        self._state = STATE_ACTIVE
        self._wave.set_game_state('play')
        self._text = None
        self._textLives.text = 'Lives: ' + str(self._wave.getLives())

    def state_complete(self):
        """
        Ran by the update if the state is STATE_COMPLETE. determines if the
        game was either won or lost, then displays the appropriate screen. Ran
        continously only after a victory or defeat.
        """
        if self._wave.get_game_state() == 'win':
            self._text = GLabel(text = "Congratulations, YOU WIN!",
            font_size = 60, font_name = "Arcade", x = GAME_WIDTH/2,
            y = GAME_HEIGHT/8*5)
            self._textSupport = GLabel(text = 'You did it! One more?',
            font_size = 50, font_name = "Arcade", x = GAME_WIDTH/2,
            top = self._text.bottom-GAME_HEIGHT/10)
            self._textAgain = GLabel(text = 'Press "S" to Play Again',
            font_size = 40, font_name = "Arcade", x = GAME_WIDTH/2,
            top = self._textSupport.bottom-GAME_HEIGHT/10)

        else:
            self._text = GLabel(text = "Game Over :(",
            font_size = 60, font_name = "Arcade", x = GAME_WIDTH/2,
            y = GAME_HEIGHT/8*5)
            self._textSupport = GLabel(text = 'Come on, you can do this!',
            font_size = 50, font_name = "Arcade", x = GAME_WIDTH/2,
            top = self._text.bottom-GAME_HEIGHT/10)
            self._textAgain = GLabel(text = 'Press "S" to Play Again',
            font_size = 40, font_name = "Arcade", x = GAME_WIDTH/2,
            top = self._textSupport.bottom-GAME_HEIGHT/10)



    def keys_pressed(self):
        """
        Detects if a key is pressed. Only returns true for a single frame after
        the key is pressed to prevent input spam from holding down a key. Referenced
        several times by other helped functions when detecting if the player wants
        to continue or start the game.
        """
        keys_pressed = self.input.key_count
        change = keys_pressed and self.lastkeys == 0
        self.lastkeys = keys_pressed
        if change:
            return True
