import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import praw
from datetime import datetime
import random

bot = commands.Bot(".", intents=discord.Intents.all())
guildid = 1232010287633272903

flairwhitelist = ["Cat Picture", "Cat Picture - OC", "Adoption"]
filetypes = ["jpeg", "jpg", "webp", "png", "gif"]
load_dotenv()


reddit = praw.Reddit(client_id=os.getenv("CLIENTID"), client_secret=os.getenv("CLIENTSECRET"), user_agent="Discord Cat Bot Made by JugieNoob: github.com/JugieNoob/Discord-Cat-Bot", check_for_async=False)

def fetchCat():
    
    embed = discord.Embed(color=discord.Color.random())
    embed.set_footer(text="r/cats", icon_url=bot.user.avatar)
    
    submissions = []
    
    for submission in reddit.subreddit("Cats").hot(limit=100):
        if not submission.stickied and submission.link_flair_text in flairwhitelist and not submission.is_video:
            submissions.append(submission)
        pass
        
    image = ""

    post = random.randint(0, len(submissions) - 1)
    if "gallery" in submissions[post].url:
        gallery = reddit.submission(url = submissions[post].url).media_metadata
        for image_item in gallery.values():
            image =image_item["s"]["u"]
            break
            #largest_image = image_item['s']
           #image_url = largest_image['u']
    else:
        for file in filetypes:
            if file in submissions[post].url:
                image = submissions[post].url

        
    try:
        embed.title = submissions[post].title
    except():
        print("Title is too long! Attempting to shorten title...")
        embed.title = f"{submissions[post].title[0:200]}..."
    embed.url = f"https://www.reddit.com/r/cats/comments/{submissions[post]}"
    embed.description = f"u/{str(submissions[post].author)}"
    embed.set_image(url=image)
    embed.timestamp = datetime.fromtimestamp(submissions[post].created)
    return embed
        
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    
    
@bot.command(name="cat") #, guild=discord.Object(id=guildid)
async def self(ctx):

    catembed = fetchCat()    
    await ctx.send(embed=catembed)
    
   
    
# Start the bot.
bot.run(os.getenv("TOKEN"))
