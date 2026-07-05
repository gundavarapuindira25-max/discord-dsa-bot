import discord
from discord.ext import commands, tasks
from datetime import datetime, time
import pytz
import os
from dotenv import load_dotenv
from problems import PROBLEMS

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))
TIMEZONE = os.getenv("TIMEZONE", "America/New_York")

# Post at 9am on Monday (easy) and Thursday (medium)
MONDAY = 0
THURSDAY = 3
POST_HOUR = 9
POST_MINUTE = 0

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)


def get_current_week_index():
    """Returns which problem set to use based on weeks since a fixed start date."""
    start_date = datetime(2025, 1, 6)  # First Monday — update to your actual start date
    now = datetime.now(pytz.timezone(TIMEZONE))
    delta = now - start_date.replace(tzinfo=pytz.timezone(TIMEZONE))
    week_num = max(0, delta.days // 7)
    return week_num % len(PROBLEMS)


def build_easy_embed(problem_set):
    embed = discord.Embed(
        title=f"🟢  Week {problem_set['week']} — {problem_set['topic']}",
        description="Monday problem — start of the week. Easy warm-up.",
        color=0x1D9E75,  # teal
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
        color=0xBA7517,  # amber
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


@tasks.loop(minutes=1)
async def check_schedule():
    tz = pytz.timezone(TIMEZONE)
    now = datetime.now(tz)

    if now.minute != POST_MINUTE or now.hour != POST_HOUR:
        return

    is_monday = now.weekday() == MONDAY
    is_thursday = now.weekday() == THURSDAY

    if not (is_monday or is_thursday):
        return

    channel = bot.get_channel(CHANNEL_ID)
    if not channel:
        print(f"Channel {CHANNEL_ID} not found.")
        return

    problem_set = PROBLEMS[get_current_week_index()]

    if is_monday:
        embed = build_easy_embed(problem_set)
        await channel.send(embed=embed)
        print(f"[{now}] Posted Monday easy — Week {problem_set['week']}")

    elif is_thursday:
        embed = build_medium_embed(problem_set)
        await channel.send(embed=embed)
        print(f"[{now}] Posted Thursday medium — Week {problem_set['week']}")


@bot.event
async def on_ready():
    print(f"Bot online as {bot.user}")
    check_schedule.start()


# Manual test command — admin only
@bot.command(name="testpost")
@commands.has_permissions(administrator=True)
async def test_post(ctx, day: str = "monday"):
    problem_set = PROBLEMS[get_current_week_index()]
    if day.lower() == "monday":
        embed = build_easy_embed(problem_set)
    else:
        embed = build_medium_embed(problem_set)
    await ctx.send(embed=embed)
    await ctx.message.delete()


@bot.command(name="nextproblem")
@commands.has_permissions(administrator=True)
async def next_problem(ctx):
    idx = get_current_week_index()
    problem_set = PROBLEMS[idx]
    await ctx.send(
        f"Current week index: {idx} | Week {problem_set['week']}: {problem_set['topic']}"
    )


bot.run(TOKEN)


# ── System Design ──────────────────────────────────────────────────────────────
from system_design_problems import SYSTEM_DESIGN_PROBLEMS

SD_CHANNEL_ID = int(os.getenv("SD_CHANNEL_ID", "0"))
SD_DAY = 6  # Sunday
SD_POST_HOUR = 10


def get_sd_week_index():
    start_date = datetime(2025, 1, 5)  # First Sunday — update to match your start
    now = datetime.now(pytz.timezone(TIMEZONE))
    delta = now - start_date.replace(tzinfo=pytz.timezone(TIMEZONE))
    # Every 2 weeks
    week_num = max(0, delta.days // 14)
    return week_num % len(SYSTEM_DESIGN_PROBLEMS)


def build_sd_embed(problem):
    embed = discord.Embed(
        title=f"🏗️  System Design — Week {problem['week']}",
        description=f"**{problem['title']}**  *(e.g. {problem['example']})*",
        color=0x534AB7,  # purple
    )
    embed.add_field(name="The prompt", value=problem["prompt"], inline=False)
    think = "\n".join(f"• {q}" for q in problem["think_about"])
    embed.add_field(name="Things to think about", value=think, inline=False)
    embed.add_field(name="Scale nudge", value=f"_{problem['scale_nudge']}_", inline=False)
    embed.add_field(
        name="How to participate",
        value=(
            "Drop your high-level design below — a few sentences or a rough diagram description is enough.\n"
            "No right answer. The point is to think out loud and see how others approach it.\n"
            "Wednesday: react with ✅ if you had a go at it."
        ),
        inline=False,
    )
    embed.set_footer(text="Next system design drops in 2 weeks.")
    return embed


@check_schedule.before_loop
async def before_check():
    await bot.wait_until_ready()


# Patch check_schedule to also handle system design
original_check = check_schedule.coro


async def patched_check():
    await original_check()

    if SD_CHANNEL_ID == 0:
        return

    tz = pytz.timezone(TIMEZONE)
    now = datetime.now(tz)

    if now.minute != POST_MINUTE or now.hour != SD_POST_HOUR:
        return
    if now.weekday() != SD_DAY:
        return

    # Only post on even weeks (bi-weekly)
    start_date = datetime(2025, 1, 5, tzinfo=tz)
    weeks_elapsed = (now - start_date).days // 7
    if weeks_elapsed % 2 != 0:
        return

    channel = bot.get_channel(SD_CHANNEL_ID)
    if not channel:
        return

    problem = SYSTEM_DESIGN_PROBLEMS[get_sd_week_index()]
    embed = build_sd_embed(problem)
    await channel.send(embed=embed)
    print(f"[{now}] Posted system design — Week {problem['week']}: {problem['title']}")


check_schedule.coro = patched_check


@bot.command(name="testsd")
@commands.has_permissions(administrator=True)
async def test_sd(ctx):
    problem = SYSTEM_DESIGN_PROBLEMS[get_sd_week_index()]
    embed = build_sd_embed(problem)
    await ctx.send(embed=embed)
    await ctx.message.delete()
