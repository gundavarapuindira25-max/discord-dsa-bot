import discord
from discord.ext import commands, tasks
from datetime import datetime
import pytz
import os
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from dotenv import load_dotenv
from problems import PROBLEMS
from system_design_problems import SYSTEM_DESIGN_PROBLEMS
 
class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"ok")
    def log_message(self, format, *args):
        pass
 
def run_health_server():
    HTTPServer(("0.0.0.0", 8080), HealthHandler).serve_forever()
 
threading.Thread(target=run_health_server, daemon=True).start()
 
load_dotenv()
 
TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))
SD_CHANNEL_ID = int(os.getenv("SD_CHANNEL_ID", "0"))
TIMEZONE = os.getenv("TIMEZONE", "America/New_York")
 
MONDAY = 0
THURSDAY = 3
SUNDAY = 6
POST_HOUR = 9
POST_MINUTE = 0
SD_POST_HOUR = 10
 
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)
 
 
def get_current_week_index():
    start_date = datetime(2025, 7, 6) 
    now = datetime.now(pytz.timezone(TIMEZONE))
    delta = now - start_date.replace(tzinfo=pytz.timezone(TIMEZONE))
    week_num = max(0, delta.days // 7)
    return week_num % len(PROBLEMS)
 
 
def get_sd_week_index():
    start_date = datetime(2025, 7, 5) 
    now = datetime.now(pytz.timezone(TIMEZONE))
    delta = now - start_date.replace(tzinfo=pytz.timezone(TIMEZONE))
    week_num = max(0, delta.days // 14)
    return week_num % len(SYSTEM_DESIGN_PROBLEMS)
 
 
def build_easy_embed(problem_set):
    embed = discord.Embed(
        title=f"🟢  Week {problem_set['week']} — {problem_set['topic']}",
        description="Monday problem — start of the week. Easy warm-up.",
        color=0x1D9E75,
    )
    p = problem_set["easy"]
    embed.add_field(name="Problem", value=f"[{p['title']}]({p['url']})", inline=False)
    embed.add_field(name="Pattern", value=p["pattern"], inline=False)
    embed.add_field(
        name="How to participate",
        value="Drop your solution, pseudocode, or approach below.\nStuck after 30 min? Look it up — understanding a solution counts.",
        inline=False,
    )
    embed.set_footer(text="Thursday: medium problem drops. No pressure, just show up.")
    return embed
 
 
def build_medium_embed(problem_set):
    embed = discord.Embed(
        title=f"🟡  Week {problem_set['week']} — {problem_set['topic']}",
        description="Thursday problem — mid-week stretch.",
        color=0xBA7517,
    )
    p = problem_set["medium"]
    embed.add_field(name="Problem", value=f"[{p['title']}]({p['url']})", inline=False)
    embed.add_field(name="Pattern", value=p["pattern"], inline=False)
    embed.add_field(
        name="How to participate",
        value="Same rules — attempt first, then look it up if stuck.\nFriday: drop your wins in #wins (anything counts).",
        inline=False,
    )
    embed.set_footer(text="Next Monday: new topic, new easy problem.")
    return embed
 
 
def build_sd_embed(problem):
    embed = discord.Embed(
        title=f"🏗️  System Design — Week {problem['week']}",
        description=f"**{problem['title']}**  *(e.g. {problem['example']})*",
        color=0x534AB7,
    )
    embed.add_field(name="The prompt", value=problem["prompt"], inline=False)
    think = "\n".join(f"• {q}" for q in problem["think_about"])
    embed.add_field(name="Things to think about", value=think, inline=False)
    embed.add_field(name="Scale nudge", value=f"_{problem['scale_nudge']}_", inline=False)
    embed.add_field(
        name="How to participate",
        value=(
            "Drop your high-level design below — a few sentences is enough.\n"
            "No right answer. Think out loud and see how others approach it.\n"
            "Wednesday: react with ✅ if you had a go at it."
        ),
        inline=False,
    )
    embed.set_footer(text="Next system design drops in 2 weeks.")
    return embed
 
 
@tasks.loop(minutes=1)
async def check_schedule():
    tz = pytz.timezone(TIMEZONE)
    now = datetime.now(tz)
 
    if now.minute != POST_MINUTE:
        return
 
    # DSA — Monday easy
    if now.weekday() == MONDAY and now.hour == POST_HOUR:
        channel = bot.get_channel(CHANNEL_ID)
        if channel:
            problem_set = PROBLEMS[get_current_week_index()]
            await channel.send(embed=build_easy_embed(problem_set))
            print(f"[{now}] Posted Monday easy — Week {problem_set['week']}")
 
    # DSA — Thursday medium
    elif now.weekday() == THURSDAY and now.hour == POST_HOUR:
        channel = bot.get_channel(CHANNEL_ID)
        if channel:
            problem_set = PROBLEMS[get_current_week_index()]
            await channel.send(embed=build_medium_embed(problem_set))
            print(f"[{now}] Posted Thursday medium — Week {problem_set['week']}")
 
    # System design — bi-weekly Sunday
    if now.weekday() == SUNDAY and now.hour == SD_POST_HOUR and SD_CHANNEL_ID != 0:
        start_date = datetime(2025, 7, 6, tzinfo=tz)
        weeks_elapsed = (now - start_date).days // 7
        if weeks_elapsed % 2 == 0:
            channel = bot.get_channel(SD_CHANNEL_ID)
            if channel:
                problem = SYSTEM_DESIGN_PROBLEMS[get_sd_week_index()]
                await channel.send(embed=build_sd_embed(problem))
                print(f"[{now}] Posted system design — {problem['title']}")
 
 
@bot.event
async def on_ready():
    print(f"Bot online as {bot.user}")
    check_schedule.start()
 
 
@bot.command(name="testpost")
@commands.has_permissions(administrator=True)
async def test_post(ctx, day: str = "monday"):
    problem_set = PROBLEMS[get_current_week_index()]
    embed = build_easy_embed(problem_set) if day.lower() == "monday" else build_medium_embed(problem_set)
    await ctx.send(embed=embed)
    await ctx.message.delete()
 
 
@bot.command(name="testsd")
@commands.has_permissions(administrator=True)
async def test_sd(ctx):
    problem = SYSTEM_DESIGN_PROBLEMS[get_sd_week_index()]
    await ctx.send(embed=build_sd_embed(problem))
    await ctx.message.delete()
 
 
@bot.command(name="nextproblem")
@commands.has_permissions(administrator=True)
async def next_problem(ctx):
    idx = get_current_week_index()
    problem_set = PROBLEMS[idx]
    await ctx.send(f"Week index: {idx} | Week {problem_set['week']}: {problem_set['topic']}")
 
 
bot.run(TOKEN)