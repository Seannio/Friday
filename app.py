###### FRIDAY V5 ###### 
# A stupid, stupid bot that does a bunch of stupid things.
# The documentation is BAD. 
# This bot is STUPID and built on the corpses of four other bots! Yay! 

import discord
import random
import markovify
import csv
import wikipedia
import wikipediaapi
import COVID19Py
import json


###### VARIABLES ###### 
TOKEN = 'NzAyOTM2ODM3NjUxNjkzNjAw.XqHS-A.KTlLykkBj8E5qDx__Xrv2hqcneg'
client = discord.Client()

wiki_wiki = wikipediaapi.Wikipedia('en')

covid19 = COVID19Py.COVID19(data_source="jhu")
buglist = []

###### FILE MANIPULATION ###### 
with open("Quotes.txt") as f:  
    text = f.read()
    model = markovify.Text(text)

def randQuote():
    lines = open('Quotes.txt').read().splitlines()
    myline = random.choice(lines)
    return myline

def randAth():
    with open("Authors.csv") as a:  
        reader = csv.reader(a)
        ans = str(random.choice(list(reader)))
        return ans.replace('\'', '').replace('[', '').replace(']', '').replace('"', '')

def randInsult() :
    with open("insults.csv") as b:  
        reader = csv.reader(b)
        ans1 = str(random.choice(list(reader)))
        return ans1.replace('[', '').replace(']', '').replace('\'', '')

###### WIKIPEDIA SKIMMER ###### 
def bugprint(categorymembers, level=0, max_level=1):
    for c in categorymembers.values():
        #print("%s: %s (ns: %d)" % ("*" * (level + 1), c.title, c.ns))
        if not ("Category:" or "List" or "Hadronyche macquariensis" or "Spider Bite" or "(disambiguation)") in c.title:
            buglist.append(c.title)
        if c.ns == wikipediaapi.Namespace.CATEGORY and level < max_level:
                bugprint(c.categorymembers, level=level +1, max_level=max_level)

###### BOT SETUP ###### 
@client.event
async def on_ready():
    # BUGBOT Setup 
    # Cosmopolitan_spiders
    cat1 = wiki_wiki.page("Category:Venomous_spiders")
    bugprint(cat1.categorymembers)

    cat2 = wiki_wiki.page("Category:Butterflies_of_Jamaica")
    bugprint(cat2.categorymembers)

    cat3 = wiki_wiki.page("Category:Insect_common_names")
    bugprint(cat3.categorymembers)
    
    #print(buglist)
    print(f'{client.user.name} has connected to Discord!')
    await client.change_presence(status=discord.Status.online, activity = discord.Activity(name='with bugs!', type=discord.ActivityType.streaming))


###### TEXT RETURNS ###### 
@client.event
async def on_message(message):
    if message.author == client.user:
        return

    
    ###### MARKOV CALLS ######  
    if message.content == '$kama':
        response = model.make_short_sentence(400)
        await message.channel.send(response + " \n-" + randAth())

    if message.content == '$quote':
        await message.channel.send(randQuote() + " \n-" + randAth())
        

    ###### WIKIPEDIA CALL ######  
    if message.content == '$bug':
        bug = wikipedia.page(random.choice(buglist))
        e = discord.Embed(title="On today's menu: " + bug.title, description=bug.summary)
        e.set_image(url=bug.images[0])
        await message.channel.send(embed=e)

    if message.content == '$wiki':
        randomPage = wikipedia.random(1)
        weird = wikipedia.page(randomPage)
        e = discord.Embed(title=weird.title, description=weird.summary)
        e.set_footer(text=weird.url)
        e.set_image(url=weird.images[0])
        await message.channel.send(embed=e)

    ###### COVID CALLS ###### 
    
    if '$covid' in message.content:
        countryCode = message.content.split()[1]
        if countryCode == "UK" or countryCode == "GB":
            output = (f'```England sucks.```')
            await message.channel.send(output)
        elif countryCode == "CA":
                NSp = covid19.getLocationById(3)
                MBp = covid19.getLocationById(38)
                
                latestNS = NSp['latest']
                confirmedNS = latestNS['confirmed']
                deathsNS = latestNS['deaths']

                latestMB = MBp['latest']
                confirmedMB = latestMB['confirmed']
                deathsMB = latestMB['deaths']

                output = (f'```Nova Scotia\n------------\nConfirmed: {confirmedNS}\nDeaths: {deathsNS}\n\nManitoba\n------------\nConfirmed: {confirmedMB}\nDeaths: {deathsMB}```')
                await message.channel.send(output)
        elif countryCode == "NK":
            output = (f'```There are no cases of COVID-19 in the glorious Democratic People\'s Republic of Korea.```')
            await message.channel.send(output)

        else: 
            try:
                location = covid19.getLocationByCountryCode(countryCode)
                convertedList = location[0]
                print(convertedList)
                country = convertedList['country']
                time = convertedList['last_updated']

                dateTimeList = time.split('T')
                outdate, outtime = dateTimeList[0], dateTimeList[1]
                timeout = f'{outdate} at {outtime[0:5]}'

                latest = convertedList['latest']
                confirmed = latest['confirmed']
                recovered = latest['recovered']
                deaths = latest ['deaths']
                print(latest)
            
                output = (f'```Country: {country} \nConfirmed: {confirmed}\nDeaths: {deaths}\nUpdated: {timeout}```')
                await message.channel.send(output)

            except:
                output = ('```Invalid countrycode, dumbass.```')
                await message.channel.send(output)


    if message.content == '$apocalypse':
        latest = covid19.getLatest()
        print(latest)
        confirmed = latest['confirmed']
        deaths = latest['deaths']

        if message.author.id == 194250346883842048:
                output = (f':skull: RIP :skull:```\n{deaths} HAVE MET THEIR DEMISE!```')
                await message.channel.send(output)
        elif message.author.id == 209120745610149890:
                output = (f':corn: RIP :corn:```\n{deaths} HAVE MET THEIR DEMISE!```')
                await message.channel.send(output)
        else: 
            output = (f':fire: WORLDWIDE TOTAL :fire:```\nConfirmed: {confirmed} \nDeaths   :  {deaths}```')
            await message.channel.send(output)
    

    # Content checks for dumb stuff. 
    if message.content == '$nick':
        await message.channel.send("<@175732928586842113>" +  ' is a ' + randInsult())

    if message.content == '$bed':
        e = discord.Embed(title="HEY NICK!")
        e.set_image(url="https://i.imgur.com/fhIUOu1.png")
        await message.channel.send(embed=e)

    if '$add' in message.content:
        openquotes = open('Quotes.txt', "a")
        newquote = message.content.replace('$add ', '')
        openquotes.write(newquote + "\n")
        await message.channel.send("Quote added.")

    if "wut" in message.content.lower(): 
        e = discord.Embed(color=1146986, title="wut", description="wut")
        e.set_image(url="https://i.imgur.com/DIE6mze.png")
        e.set_footer(text="wut")
        await message.channel.send(embed=e)

    if "pot" in message.content.lower(): 
        e = discord.Embed(color=1146986, title="I PLAY POT OF GREED...", description="WHICH ALLOWS ME TO DRAW THREE ADDITIONAL CARDS.")
        e.set_image(url="https://i.imgur.com/h1hTDCz.png")
        e.set_footer(text="THEN I PLAY POT OF GREED \nWHICH ALLOWS ME TO DRAW TWO ADDITIONAL CARDS")
        await message.channel.send(embed=e)

    if "uhh" in message.content.lower(): 
        e = discord.Embed(title="lookat this doofus")
        e.set_image(url="https://imgur.com/2X7rrtX.png")
        e.set_footer(text="sayin uhhhh and shittttt")
        await message.channel.send(embed=e)

    if "fool" in message.content.lower(): 
        e = discord.Embed(color=15844367, title="YOU FOOL!")
        e.set_image(url="https://i.imgur.com/Oa3FZYy.gif")
        await message.channel.send(embed=e)
    
    if "snurg" in message.content.lower():
        response = "<:snurg:696892670726897735> <:snurg:696892670726897735> <:snurg:696892670726897735> <:snurg:696892670726897735> <:snurg:696892670726897735> <:snurg:696892670726897735> <:snurg:696892670726897735> <:snurg:696892670726897735> <:snurg:696892670726897735> <:snurg:696892670726897735> <:snurg:696892670726897735> <:snurg:696892670726897735> <:snurg:696892670726897735> <:snurg:696892670726897735> <:snurg:696892670726897735> <:snurg:696892670726897735> <:snurg:696892670726897735> <:snurg:696892670726897735> <:snurg:696892670726897735> UH <:snurg:696892670726897735> OH :lobster: IT'S REAL <:snurg:696892670726897735>  SNURGPOSTING <:snurg:696892670726897735>  HOURS <:snurg:696892670726897735> <:snurg:696892670726897735> <:snurg:696892670726897735> <:snurg:696892670726897735> <:snurg:696892670726897735> <:snurg:696892670726897735> <:snurg:696892670726897735> <:snurg:696892670726897735> <:snurg:696892670726897735>"
        await message.channel.send(response)

    if "aaaaa" in message.content.lower(): # Idea: The more 'aaaas' in the message, the more deepfried it gets.
        e = discord.Embed(color=15158332, title="AAAAAAAAAAAAAA! >:(")
        e.set_image(url="https://i.imgur.com/KgA6SaP.gif")
        await message.channel.send(embed=e)
    
    if "gunwolf" in message.content.lower():
        e = discord.Embed(color=3447003, title="hey GUN WOLF STOP PLEASE DANCING AND SHOOT THE GUY!")
        e.set_image(url="https://i.imgur.com/ZC2vRNI.gif") 
        await message.channel.send(embed=e)

    if "dog" in message.content.lower():
        e = discord.Embed(color=10181046, title="Yo did someone say it's DOGTIME?!?!")
        e.set_image(url="https://i.imgur.com/ql4K7wW.png")
        await message.channel.send(embed=e) 

    if "delete" in message.content.lower():
        e = discord.Embed(color=15158332, title="PLS DELETE")
        e.set_image(url="https://i.imgur.com/CVwd1nF.gif") 
        await message.channel.send(embed=e) 

    if "wife" in message.content.lower():
        response = "<@209120745610149890>" + ' - Did someone say Fuck my Wife?'
        await message.channel.send(response)

    #<:emoji_name:emoji_id 696892670726897735> 
    if message.content == "$help":
        response = """```md
# FRIDAY HELP!
# Use '$' for commands! 
< kama  > | Generates a shitty markov chain off of saved quotes
< add   > | Use add (text) to add (text) to the quotes file
< quote > | Pulls a quote from the quotes file
< bed   > | Tells nick to GODABED. 
< nick  > | Insults nick.
< bug   > | Decides on a bug to eat.
< covid > | Use with a country code (US) to see covids.
< wiki  > | Random wikipedia article
There are also SECRET commands!```"""
        await message.channel.send(response)

client.run(TOKEN)
