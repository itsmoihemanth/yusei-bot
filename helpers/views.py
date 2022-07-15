import discord

class Confirm_View(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None

    @discord.ui.button(label="Confirm", style=discord.ButtonStyle.green)
    async def confirm_callback(self, button: discord.ui.Button, interaction: discord.Interaction):
        await interaction.response.send_message("Confirming", ephemeral=True)
        self.value = True
        self.stop()

    @discord.ui.button(label="Cancel", style=discord.ButtonStyle.red)
    async def cancel_callback(self, button: discord.ui.Button, interaction: discord.Interaction):
        await interaction.response.send_message("Cancelling", ephemeral=True)
        self.value = False
        self.stop()

class Modules_View(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None

    @discord.ui.button(label="Birthday", style=discord.ButtonStyle.blurple)
    async def birthday_callback(self, button: discord.ui.Button, interaction: discord.Interaction):
        view = Channels_View()
        await interaction.response.send_message("Would you like to create a new channel or select an existing channel", view=view)
        await view.wait()
        if view.value == True:
            print("done")
        self.stop()

    @discord.ui.button(label="Quotes", style=discord.ButtonStyle.blurple)
    async def quotes_callback(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.stop()

class Channels_View(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None

    @discord.ui.button(emoji=discord.PartialEmoji(name="🔨"), style=discord.ButtonStyle.blurple) 
    async def new_callback(self, button: discord.ui.Button, interaction: discord.Interaction):
        await interaction.response.send_message("New Channel created",view=Confirm_View())
        self.stop()

    @discord.ui.button(emoji=discord.PartialEmoji(name="🖱"), style=discord.ButtonStyle.blurple)
    async def existing_callback(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.stop()

    @discord.ui.button(emoji=discord.PartialEmoji(name="❌"), style=discord.ButtonStyle.blurple)
    async def cancel_callback(self, button: discord.ui.Button, interaction: discord.Interaction):
        view=Confirm_View()
        await interaction.response.send_message("",view=view)

        await view.wait()
        if view.value == False:
            print("Continue")

        self.value = True
        self.stop()


class PersistentView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(
        label="Wave To Say Hi!!",
        custom_id="persistent_view:greet",
    )
    async def greet(self, button: discord.ui.Button, interaction: discord.Interaction):
        await interaction.response.send_message(random.choice(["https://c.tenor.com/-Kgr-uW4GA8AAAAi/hello.gif","https://c.tenor.com/qLMpwF42khIAAAAi/hi-brown.gif","https://c.tenor.com/y1enbfpHMTEAAAAi/hi-cute.gif","https://c.tenor.com/ftqs42Yna-oAAAAi/mochi-mochi-hello-white-mochi-mochi.gif"]))


#Tic Tac Toe Views Start

from typing import List

import discord
from discord.ext import commands


# Defines a custom button that contains the logic of the game.
# The ['TicTacToe'] bit is for type hinting purposes to tell your IDE or linter
# what the type of `self.view` is. It is not required.
class TicTacToeButton(discord.ui.Button["TicTacToe"]):
    def __init__(self, x: int, y: int):
        # A label is required, but we don't need one so a zero-width space is used.
        # The row parameter tells the View which row to place the button under.
        # A View can only contain up to 5 rows -- each row can only have 5 buttons.
        # Since a Tic Tac Toe grid is 3x3 that means we have 3 rows and 3 columns.
        super().__init__(style=discord.ButtonStyle.secondary, label="\u200b", row=y)
        self.x = x
        self.y = y

    # This function is called whenever this particular button is pressed.
    # This is part of the "meat" of the game logic.
    async def callback(self, interaction: discord.Interaction):
        assert self.view is not None
        view: TicTacToe = self.view
        state = view.board[self.y][self.x]
        if state in (view.X, view.O):
            return

        if view.current_player == view.X:
            self.style = discord.ButtonStyle.danger
            self.label = "X"
            view.board[self.y][self.x] = view.X
            view.current_player = view.O
            content = "It is now O's turn"
        else:
            self.style = discord.ButtonStyle.success
            self.label = "O"
            view.board[self.y][self.x] = view.O
            view.current_player = view.X
            content = "It is now X's turn"

        self.disabled = True
        winner = view.check_board_winner()
        if winner is not None:
            if winner == view.X:
                content = "X won!"
            elif winner == view.O:
                content = "O won!"
            else:
                content = "It's a tie!"

            for child in view.children:
                child.disabled = True

            view.stop()

        await interaction.response.edit_message(content=content, view=view)


# This is our actual board View.
class TicTacToe(discord.ui.View):
    # This tells the IDE or linter that all our children will be TicTacToeButtons.
    # This is not required.
    children: List[TicTacToeButton]
    X = -1
    O = 1
    Tie = 2

    def __init__(self):
        super().__init__()
        self.current_player = self.X
        self.board = [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
        ]

        # Our board is made up of 3 by 3 TicTacToeButtons.
        # The TicTacToeButton maintains the callbacks and helps steer
        # the actual game.
        for x in range(3):
            for y in range(3):
                self.add_item(TicTacToeButton(x, y))

    # This method checks for the board winner and is used by the TicTacToeButton.
    def check_board_winner(self):
        # Check horizontal
        for across in self.board:
            value = sum(across)
            if value == 3:
                return self.O
            elif value == -3:
                return self.X

        # Check vertical
        for line in range(3):
            value = self.board[0][line] + self.board[1][line] + self.board[2][line]
            if value == 3:
                return self.O
            elif value == -3:
                return self.X

        # Check diagonals
        diag = self.board[0][2] + self.board[1][1] + self.board[2][0]
        if diag == 3:
            return self.O
        elif diag == -3:
            return self.X

        diag = self.board[0][0] + self.board[1][1] + self.board[2][2]
        if diag == -3:
            return self.X
        elif diag == 3:
            return self.O

        # If we're here, we need to check if a tie has been reached.
        if all(i != 0 for row in self.board for i in row):
            return self.Tie

        return None

#Tic Tac Toe Views End 