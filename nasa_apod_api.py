import os
import discord_functions as df


if __name__ == '__main__':
    df.bot.run(os.getenv('TOKEN'))
