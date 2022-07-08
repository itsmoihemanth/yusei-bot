import os
import discord
import uuid
import asyncio
from discord.commands import Option
from discord.ext import commands , pages

from helpers import checks, manager

# Here we name the cog and create a new class for the cog.
class Template(commands.Cog, name="template-slash"):
    def __init__(self, bot):
        self.bot = bot

    survey = SlashCommandGroup("survey", "Survey commands")

    @quotes.command(
        name="add",
        description="Add new quotes"
        )
    @checks.not_blacklisted()
    async def survey_view(self, interaction: discord.ApplicationContext,
                        candidate: Option(discord.Member, "Take the survey",default="")) -> None:
        """
        This command displays the survey files.
        :param interaction: The application command interaction.
        :param candidate: The user whose file we want to see.
        """

        check2=0
        dm = await bot.fetch_user(candidate)
        user = str(dm).split('#', 1)[0]
    
        await ctx.reply(f"Check your dm's {candidate.mention} to fill the survey")
        def checking(msg):
            return (str(msg.author.id)) == candidate and isinstance(msg.channel,discord.DMChannel)
        
        while check2==0:
            check3=0
            survey_author = ""
        
            if ctx.author.id in [440433975396401152]:
                try:
                    await dm.send("Whose survey do you want to take - skittles/yams/trix ?")
                    author = await bot.wait_for("message", check=checking, timeout=120)
                    survey_author = str(author.content)
                
                except asyncio.TimeoutError:
                    await dm.send("Sorry," + candidate.mention + " you didn't reply in time! \n---------------------------------------------------")

            
            if survey_author or ctx.author.id in ["skittles","Skittles","SKITTLES",697933501617406012] :
                file = "skittles survey"
                survey_df = ath.convert_to_dataframe(
                ath.airtable_download(file))  ## Read excel file
              
                check = survey_df[survey_df["Candidate ID"].str.contains(str(dm))]  ## Check if quote already exists

                if not check.empty:
                    await dm.send(user+" you have already filled the Skittles Survey, What are you trying to do?")
                else: 
                    await dm.send("**__The Skittles Survey for "+candidate.mention+"__**")

                    question = await dm.send("Do u like fruit roll ups?")
                    try:
                        Q1 = await bot.wait_for("message", check=checking, timeout=120)
                        await question.edit("Do u like sports or anime?")

                    
                        Q2 = await bot.wait_for("message", check=checking, timeout=120)
                        await question.edit(
                            "Are you ||gay||?(you don't gotta answer if it makes you uncomfortable)"
                        )

                       
                        Q3 = await bot.wait_for("message", check=checking, timeout=120)
                        await question.edit(
                            "When u think of the name riley, whats the first last name that comes to mind?"
                        )

                       
                        Q4 = await bot.wait_for("message", check=checking, timeout=120)
                        await question.edit(
                            "Thank you for completing the skittles Survey your in the files <:fr_love:892759550476845066>"
                        )
                        Id = uuid.uuid4().hex[:5]

                        ath.airtable_upload(
                            file, {
                                "Id": Id,
                                "Candidate ID": candidate,
                                "Candidate Name": str(dm),
                                "Q1": Q1.content,
                                "Q2": Q2.content,
                                "Q3": Q3.content,
                                "Q4": Q4.content
                            })

                        response = "**->Do u like fruit roll ups?**\n" + Q1.content + "\n\n**->Do u like sports or anime?**\n" + Q2.content + "\n\n**->Are you ||gay||?(you don't gotta answer if it makes you uncomfortable)**\n" + Q3.content + "\n\n**->When u think of the name riley, whats the first last name that comes to mind?\n**" + Q4.content
                        make_embed = discord.Embed(title="__The Skittles Survey "+user+" file__",
                                                   description=response,
                                                   color=0xe0a8cf)
                        await ctx.send(embed=make_embed)

                        
                    except asyncio.TimeoutError:
                        await dm.send("Sorry," + candidate.mention +
                                       " you didn't reply in time! \n---------------------------------------------------")

            elif survey_author or ctx.author.id in ["yams","Yams","YAMS",547643632912433182]:
                file = "yams survey"
                survey_df = ath.convert_to_dataframe(
                    ath.airtable_download(file))  ## Read excel file
                candidate = str(candidate)
                candidate = candidate.lstrip("<@!")
                candidate = candidate.rstrip(">")
            
                check = survey_df[survey_df["Candidate ID"].str.contains(str(dm))] 

                if not check.empty:
                    await dm.send(user+" you have already filled the Yams exit Survey, What are you trying to do?")
                
                else:
                    await dm.send("**__The Yams exit Survey for"+candidate.mention+"__**")

                    await dm.send("Have you watched and/or read citrus?")
                    try:
                        Q1 = await bot.wait_for("message", check=checking, timeout=120)
                        await dm.send("What is your favorite food?")

                        Q2 = await bot.wait_for("message", check=checking, timeout=120)
                        await dm.send(
                            "Thank you for completing the Yams exit Survey your in the files <:fr_love:892759550476845066>"
                        )
                        Id = uuid.uuid4().hex[:5]

                        ath.airtable_upload(
                            file, {
                                "Id": Id,
                                "Candidate ID": candidate,
                                "Candidate Name": str(dm),
                                "Q1": Q1.content,
                                "Q2": Q2.content
                            })

                        response = "**->Have you watched and/or read citrus?**\n" + Q1.content + "\n\n**->What is your favorite food?**\n" + Q2.content
                        make_embed = discord.Embed(title="__The Yams Exit Survey "+user+" file__",
                                                   description=response,
                                                   color=0xe0a8cf)
                        await ctx.send(embed=make_embed)

                    except asyncio.TimeoutError:
                        await dm.send("Sorry," + mention +
                                       " you didn't reply in time! \n---------------------------------------------------")
                                   
            elif survey_author or ctx.author.id in ["trix","Trix","TRIX","trixie","Trixie","TRIXIE",905323842858270751]:
                file = "trixie survey"
                survey_df = ath.convert_to_dataframe(
                    ath.airtable_download(file))  ## Read excel file
                candidate = str(candidate)
                candidate = candidate.lstrip("<@!")
                candidate = candidate.rstrip(">")
            
                check = survey_df[survey_df["Candidate ID"].str.contains(str(dm))] 

                if not check.empty:
                    await dm.send(user+" you have already filled the Trixie Survey, What are you trying to do?")
                
                else:
                    await dm.send("**__The Trixie Survey for "+mention+"__**")

                    await dm.send("What’s your Zodiac sign?")
                    try:
                        Q1 = await bot.wait_for("message", check=checking, timeout=120)
                        await dm.send("How tall are you?")

                        Q2 = await bot.wait_for("message", check=checking, timeout=120)
                        await dm.send("Do you have an accent and if so where from?")

                        Q3 = await bot.wait_for("message", check=checking, timeout=120)
                        await dm.send(
                            "Thank you for completing the Trixie Survey your in the files <:fr_love:892759550476845066>"
                        )
                        Id = uuid.uuid4().hex[:5]

                        ath.airtable_upload(
                            file, {
                                "Id": Id,
                                "Candidate ID": candidate,
                                "Candidate Name": str(dm),
                                "Q1": Q1.content,
                                "Q2": Q2.content,
                                "Q3": Q3.content
                            })

                        response = "**->What’s your Zodiac sign?**\n" + Q1.content + "\n\n**->How tall are you?**\n" + Q2.content + "\n\n**->Do you have an accent and if so where from?**\n" + Q3.content
                        make_embed = discord.Embed(title="__The Trixie Survey "+user+"__",
                                                   description=response,
                                                   color=0xe0a8cf)
                        await ctx.send(embed=make_embed)

                    except asyncio.TimeoutError:
                        await dm.send("Sorry," + mention +
                                       "> you didn't reply in time! \n---------------------------------------------------")
                                   
            else:
                await dm.send(f"{survey_author.content} doesn't have a survey")
            
            check2=1
            if ctx.author.id not in [697933501617406012,547643632912433182,938667389367775273]:  
              while check3==0:
                    try:
                        await dm.send( f"Do you want to take another survey?")
                        reply = await bot.wait_for("message", check=checking, timeout=60)
                    
                        if reply.content in ["Yes","YES","yes","hell ya","sure"]:
                            check2=0
                            check3=1
                        elif reply.content in ["No","NO","no","nah","NAH"]:
                            check2=1
                            check3=1
                        else:
                            check3=0
                            await dm.send("I dont know what that means, only a yes or no please")
                  
                    except asyncio.TimeoutError:
                            check3=0
                            await dm.send("I'll take your silence as a no")

def setup(bot):
    bot.add_cog(Template(bot))
