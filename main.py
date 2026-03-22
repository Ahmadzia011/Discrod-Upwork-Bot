import discord
import os
from dotenv import load_dotenv
import json
import asyncio, inspect
import time
from datetime import datetime
from visitorJobSearch import get_jobs
from jobDetails import jobDetails
import sqlite3


job_count = 0

#Loading environment variables
load_dotenv()
bot_token = os.getenv('BOT_TOKEN')


#Database Initialization
conn = sqlite3.connect('jobs.db', timeout=20, check_same_thread=False)
cursor = conn.cursor()


#Creating a table in database if doesn't exist already
cursor.execute('''
    CREATE TABLE IF NOT EXISTS jobs (
        id VARCHAR PRIMARY KEY NOT NULL,
        job_url TEXT NOT NULL,
        job_title TEXT,
        job_desc TEXT,
        channel_id BIGINT,
        first_seen TIMESTAMP NOT NULL
        )
        ''')
conn.commit() # Commit changes to database


#Loading config.json file
with open('config.json', 'r') as json_file:
    channels = json.load(json_file)
    channels_data = channels['listed_channels']
    
    
#Conecting python with discord
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
client = discord.Client(intents=intents)
  

message_content = ''

# holds periodic background tasks keyed by channel id so we can cancel/restart
periodic_tasks = {}

#This function is the brain of main.
async def process_search(message):
    
    global cursor, conn
    
    #If the message is sent by bot then the function would not run to avoid infinite loop.
    if message.author.bot:
        return

    #Run only if user(bot) is mentioned in message. 
    if client.user.mentioned_in(message):
        
        # Ensures that only channel specific jobs should be returned.                         
        if message.channel.id == channels_data[2]['id']: #only in general channel any kind of job should be returned.
            message_content = message.content.split(" ", maxsplit=1)[1]

            
        elif message.channel.id == channels_data[0]['id']:
            if 'python' in message.content.lower():
                print('found python')
                message_content = message.content.split(" ", maxsplit=1)[1]
            else:
                print('Python word not found try again with better search')
                await message.channel.send('This is python channel, search for python jobs only')
                return

        elif message.channel.id == channels_data[1]['id']:
            # use the same pattern for the scraping channel
            if 'scraping' in message.content.lower():
                message_content = message.content.split(" ", maxsplit=1)[1]
            else:
                print('Scraping word not found try again with better search')
                await message.channel.send('This is Scraping channel, search for scraping jobs only')
                return

        #This part fetches specific job details.
        print('2 going to get jobs')
        get_values = await asyncio.to_thread(get_jobs, message_content)

        for job in get_values:
            get_job_details = await asyncio.to_thread(jobDetails, job['cipherID'])
            if not get_job_details:
                print(f"Skipping {job['cipherID']} - no details available")
                continue

            id = get_job_details.get('id')
            url = get_job_details.get('job_url')
            title = get_job_details.get('title')
            desc = get_job_details.get('full_description', '')[:200]
            channel_id = message.channel.id

            cursor.execute("SELECT id FROM jobs WHERE id = ?", [job['cipherID']])
            id_found = cursor.fetchone()
            cursor.execute("SELECT job_title FROM jobs WHERE job_title = ?", [job['title']])
            title_found = cursor.fetchone()
            cursor.execute("SELECT job_desc FROM jobs WHERE job_desc = ?", [desc])
            desc_found = cursor.fetchone()

            #If job is already present in db
            if id_found or (title_found and desc_found):
                print(f"Skipping {title} - already in database.")
                continue
            

            print(f"Processing new job: {job['cipherID']}")
            
            #Stores job data in db
            cursor.execute("""
                INSERT INTO jobs (id, job_url, job_title, job_desc, channel_id, first_seen) 
                VALUES (?, ?, ?, ?, ?, ?)
                """, (id, url, title, desc, channel_id, datetime.now()))


            embed = discord.Embed(title=job['title'],
            description=job['description'][:250], color=0x00ff00)
            embed.add_field(name="Budget", value=job['budget'], inline=True)
            embed.add_field(name="Time Posted", value=job['time'], inline=True)
            embed.add_field(name="Level", value=job['level'], inline=True)
            
            
            if 'python' in message_content:
                target_channel = client.get_channel(channels_data[0]['id'])
                await target_channel.send(embed=embed)

            elif 'scraping' in message_content:
                target_channel = client.get_channel(channels_data[1]['id'])
                await target_channel.send(embed=embed)
            
            else:
                # Extract search keyword from message content
                search_keyword = message_content.split('', maxsplit=1)[1].lower()
                channel_name = f"{search_keyword}-jobs"

                # Check if channel already exists
                existing_channel = discord.utils.get(message.guild.channels, name=channel_name)

                if existing_channel:
                    target_channel = existing_channel
                else:
                    # Create new channel if it doesn't exist
                    target_channel = await message.guild.create_text_channel(channel_name)

                await target_channel.send(embed=embed)
                
                
            await message.channel.send(embed=embed)


            thread = await message.channel.create_thread(
                name=f"Job: {job['title'][:95]}",
                auto_archive_duration=60
                )

            job_url = get_job_details.get('job_url', 'https://www.upwork.com')
            full_desc = get_job_details.get('full_description', 'No description available.')
            client_spent = get_job_details.get('client_total_spent', 0)
            client_jobs = get_job_details.get('client_jobs_posted', 0)
            location = get_job_details.get('client_location', 'Unknown')
            member_since = get_job_details.get('client_member_since', 'N/A')
            duration = get_job_details.get('project_duration', 'Not specified')
            experience = get_job_details.get('experience_level', 'Not specified')
            job_type = get_job_details.get('job_type', 'Not specified')


            formatted_message = f"""
                    **🚀 NEW JOB POSTING**
                    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
                    🔗 **[Apply on Upwork]({job_url})**

                    **Full Job Description**:
                    {full_desc}


                    **💼 CLIENT DETAILS**
                    💰 **Total Spent:** ${client_spent}
                    📊 **Jobs Posted:** {client_jobs}
                    📍 **Location:** {location}
                    🗓️ **Member Since:** {member_since}

                    **📝 JOB DETAILS**
                    ⏳ **Duration:** {duration}
                    🎓 **Experience:** {experience}
                    🛠️ **Job Type:** {job_type}

                    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
                """

            if len(formatted_message) > 2000:
                formatted_message = formatted_message[:1800] + "To view full job details. Click on the above link."
            await thread.send(inspect.cleandoc(formatted_message))

        conn.commit()


#This function ensures that the jobs should be rechecked after an interval.
async def periodic_search(message, interval):
    while True:
        await asyncio.sleep(interval)
        try:
            await process_search(message)
        except Exception as exc:
            print(f"Error in periodic search for channel {message.channel.id}: {exc}")



#Function that runs when on_message event is triggered.
@client.event
async def on_message(message):
    
    # immediate run
    await process_search(message)

    # schedule periodic updates (cancel old task if exists)
    chan_id = message.channel.id

    #this check would ensure that only one search is running at a time in a channel.
    if chan_id in periodic_tasks:
        periodic_tasks[chan_id].cancel()
        
    #this is the line that allows different channels to be live at the same time
    periodic_tasks[chan_id] = asyncio.create_task(periodic_search(message, 120))

client.run(bot_token)
