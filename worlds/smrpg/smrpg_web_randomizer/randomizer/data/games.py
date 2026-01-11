# Data module for minigame data.

from ...randomizer.logic import utils
from ...randomizer.logic.patch import Patch


# ******** Ball Solitaire

class BallSolitaireGame:
    """Class for ball solitaire minigame."""

    class BallSpot:
        """Class for individual ball spot in the game."""

        def __init__(self, has_ball=False):
            self.has_ball = has_ball
            self.up = None
            self.down = None
            self.left = None
            self.right = None

        def can_kick(self, direction, reverse=False):
            """Check if we can kick the ball in this spot in the given direction.

            Args:
                direction (str): Direction to kick.
                reverse (bool): True if we're doing a reverse kick for populating the game backwards.

            Returns:
                bool: True if we can kick in this direction, False otherwise.

            """
            if direction not in ('up', 'down', 'left', 'right'):
                raise ValueError("Bad direction: {!r}".format(direction))

            if not self.has_ball:
                return False

            step1 = getattr(self, direction)
            if not step1:
                return False

            step2 = getattr(step1, direction)
            if not step2:
                return False

            # Step 2 must be clear no matter what.
            if step2.has_ball:
                return False

            # For reverse kick, we're generating a ball in the middle spot.
            if reverse:
                return not step1.has_ball
            else:
                return step1.has_ball

        def kick(self, direction):
            """Kick a ball in given direction for puzzle solving.  Kicks the ball from this spot two spots in the given
            direction, and removes the ball in the middle spot along the way.

            Args:
                direction (str): Direction to kick.

            """
            if not self.can_kick(direction):
                raise ValueError("Cannot kick {}".format(direction))

            step1 = getattr(self, direction)
            step2 = getattr(step1, direction)

            # Kick ball from here, removing the middle spot, to the empty one.
            self.has_ball = False
            step1.has_ball = False
            step2.has_ball = True

        def reverse_kick(self, direction):
            """Kick a ball in reverse for puzzle generation.  Kicks the ball from this spot two spots in the given
            direction, but places a ball in an empty spot along the way instead of removing it.

            Args:
                direction (str): Direction to kick.

            """
            if not self.can_kick(direction, reverse=True):
                raise ValueError("Cannot kick {}".format(direction))

            step1 = getattr(self, direction)
            step2 = getattr(step1, direction)

            # We have two empty spots, okay.
            self.has_ball = False
            step1.has_ball = True
            step2.has_ball = True

    BASE_ADDRESS = 0x20c0e5

    def __init__(self, world):
        """

        Args:
            world (randomizer.logic.main.GameWorld):

        """
        self.world = world

        # Vanilla ball layout for bits:
        # 13 14 15 16
        # 9  10 11 12
        # 5  6  7  8
        # 1  2  3  4
        ball1 = self.BallSpot(True)
        ball2 = self.BallSpot(True)
        ball3 = self.BallSpot(True)
        ball4 = self.BallSpot(True)
        ball5 = self.BallSpot(True)
        ball6 = self.BallSpot(True)
        ball7 = self.BallSpot(True)
        ball8 = self.BallSpot(True)
        ball9 = self.BallSpot(True)
        ball10 = self.BallSpot(True)
        ball11 = self.BallSpot(True)
        ball12 = self.BallSpot(True)
        ball13 = self.BallSpot(True)
        ball14 = self.BallSpot(True)
        ball15 = self.BallSpot(False)
        ball16 = self.BallSpot(True)

        # Add connections between spots...there's a lot of them...
        ball1.right = ball2
        ball1.up = ball5

        ball2.left = ball1
        ball2.right = ball3
        ball2.up = ball6

        ball3.left = ball2
        ball3.right = ball4
        ball3.up = ball7

        ball4.left = ball3
        ball4.up = ball8

        ball5.right = ball6
        ball5.up = ball9
        ball5.down = ball1

        ball6.right = ball7
        ball6.left = ball5
        ball6.up = ball10
        ball6.down = ball2

        ball7.right = ball8
        ball7.left = ball6
        ball7.up = ball11
        ball7.down = ball3

        ball8.left = ball7
        ball8.up = ball12
        ball8.down = ball4

        ball9.right = ball10
        ball9.up = ball13
        ball9.down = ball5

        ball10.right = ball11
        ball10.left = ball9
        ball10.up = ball14
        ball10.down = ball6

        ball11.right = ball12
        ball11.left = ball10
        ball11.up = ball15
        ball11.down = ball7

        ball12.left = ball11
        ball12.up = ball16
        ball12.down = ball8

        ball13.right = ball14
        ball13.down = ball9

        ball14.right = ball15
        ball14.left = ball13
        ball14.down = ball10

        ball15.right = ball16
        ball15.left = ball14
        ball15.down = ball11

        ball16.left = ball15
        ball16.down = ball12

        # List of spots in bit order.
        self.spots = [
            ball1,
            ball2,
            ball3,
            ball4,
            ball5,
            ball6,
            ball7,
            ball8,
            ball9,
            ball10,
            ball11,
            ball12,
            ball13,
            ball14,
            ball15,
            ball16,
        ]

    def __str__(self):
        ball_str = ''
        for spot in self.spots:
            ball_str += 'O' if spot.has_ball else 'X'
        return '<{}: {} balls {}>'.format(self.__class__.__name__, self.num_balls, ball_str)

    def __repr__(self):
        return str(self)

    @property
    def num_balls(self):
        return len([s for s in self.spots if s.has_ball])

    def get_patch(self):
        """

        Returns:
            randomizer.logic.patch.Patch: Patch data

        """
        patch = Patch()

        # Balls should be in 0-indexed bit order already.
        result = 0
        for i, spot in enumerate(self.spots):
            if spot.has_ball:
                result |= (1 << i)
        patch.add_data(self.BASE_ADDRESS, utils.ByteField(result, num_bytes=2).as_bytes())

        return patch


# ******** Magic Buttons

class MagicButtonsGame:
    """Class for magic buttons minigame."""

    class ButtonSpot:
        """Class for individual button spot in the game."""

        def __init__(self, pressed=False):
            self.pressed = pressed
            self.up = None
            self.down = None
            self.left = None
            self.right = None

        def press(self):
            if self.pressed:
                raise ValueError("Already pressed")

            self.pressed = True
            for spot in (self.up, self.down, self.left, self.right):
                if spot is not None:
                    spot.pressed = not spot.pressed

        def unpress(self):
            if not self.pressed:
                raise ValueError("Not pressed")

            self.pressed = False
            for spot in (self.up, self.down, self.left, self.right):
                if spot is not None:
                    spot.pressed = not spot.pressed

    BASE_ADDRESS = 0x205137

    def __init__(self, world):
        """

        Args:
            world (randomizer.logic.main.GameWorld):

        """
        self.world = world

        # Vanilla button layout for bits:
        # 13 14 15 16
        # 9  10 11 12
        # 5  6  7  8
        # 1  2  3  4
        button1 = self.ButtonSpot()
        button2 = self.ButtonSpot()
        button3 = self.ButtonSpot()
        button4 = self.ButtonSpot()
        button5 = self.ButtonSpot()
        button6 = self.ButtonSpot()
        button7 = self.ButtonSpot()
        button8 = self.ButtonSpot()
        button9 = self.ButtonSpot()
        button10 = self.ButtonSpot()
        button11 = self.ButtonSpot()
        button12 = self.ButtonSpot()
        button13 = self.ButtonSpot()
        button14 = self.ButtonSpot()
        button15 = self.ButtonSpot()
        button16 = self.ButtonSpot()

        # Add connections between spots.
        button1.right = button2
        button1.up = button5

        button2.left = button1
        button2.right = button3
        button2.up = button6

        button3.left = button2
        button3.right = button4
        button3.up = button7

        button4.left = button3
        button4.up = button8

        button5.right = button6
        button5.up = button9
        button5.down = button1

        button6.right = button7
        button6.left = button5
        button6.up = button10
        button6.down = button2

        button7.right = button8
        button7.left = button6
        button7.up = button11
        button7.down = button3

        button8.left = button7
        button8.up = button12
        button8.down = button4

        button9.right = button10
        button9.up = button13
        button9.down = button5

        button10.right = button11
        button10.left = button9
        button10.up = button14
        button10.down = button6

        button11.right = button12
        button11.left = button10
        button11.up = button15
        button11.down = button7

        button12.left = button11
        button12.up = button16
        button12.down = button8

        button13.right = button14
        button13.down = button9

        button14.right = button15
        button14.left = button13
        button14.down = button10

        button15.right = button16
        button15.left = button14
        button15.down = button11

        button16.left = button15
        button16.down = button12

        # List of spots in bit order.
        self.spots = [
            button1,
            button2,
            button3,
            button4,
            button5,
            button6,
            button7,
            button8,
            button9,
            button10,
            button11,
            button12,
            button13,
            button14,
            button15,
            button16,
        ]

    def __str__(self):
        button_str = ''
        for spot in self.spots:
            button_str += 'X' if spot.pressed else 'O'
        return '<{}: {}>'.format(self.__class__.__name__, button_str)

    def __repr__(self):
        return str(self)

    def get_patch(self):
        """

        Returns:
            randomizer.logic.patch.Patch: Patch data

        """
        patch = Patch()

        # Spots should be in 0-indexed bit order already.
        result = 0
        for i, spot in enumerate(self.spots):
            if spot.pressed:
                result |= (1 << i)
        patch.add_data(self.BASE_ADDRESS, utils.ByteField(result, num_bytes=2).as_bytes())

        return patch
