# DSA Study Group Bot

Posts one Easy problem every Monday and one Medium every Thursday at 9am automatically.

---

## Step 1 — Create the bot on Discord

1. Go to https://discord.com/developers/applications
2. Click **New Application** → name it (e.g. "DSA Bot")
3. Go to **Bot** tab → click **Add Bot**
4. Under **Token** → click **Reset Token** → copy it (you need this)
5. Scroll down → enable **Message Content Intent**
6. Go to **OAuth2 → URL Generator**
   - Scopes: check `bot`
   - Bot Permissions: check `Send Messages`, `Embed Links`, `Read Message History`
7. Copy the generated URL → open in browser → add to your server

---

## Step 2 — Get your channel ID

1. In Discord: Settings → Advanced → enable **Developer Mode**
2. Right-click your `#dsa-weekly` channel → **Copy ID**

---

## Step 3 — Configure the bot

```bash
cp .env.example .env
```

Edit `.env`:
```
DISCORD_TOKEN=paste_your_token_here
CHANNEL_ID=paste_your_channel_id_here
TIMEZONE=America/New_York   # or America/Chicago, America/Los_Angeles, Europe/London etc.
```

Update `bot.py` line 21 — set your actual start date (first Monday your group starts):
```python
start_date = datetime(2025, 1, 6)  # change this
```

---

## Step 4 — Run locally (test)

```bash
pip install -r requirements.txt
python bot.py
```

In Discord, run `!testpost monday` or `!testpost thursday` to see a preview post.
Run `!nextproblem` to check which week index the bot thinks it is.

---

## Step 5 — Deploy free on Railway

1. Go to https://railway.app → sign up with GitHub
2. New Project → Deploy from GitHub repo (push this folder to a repo first)
3. Add environment variables (same as your .env) in Railway dashboard
4. Deploy — bot stays online 24/7 for free

Alternative: **Render.com** (also free) — create a Background Worker, same env vars.

---

## Customizing problems

Edit `problems.py` to add, remove, or change problems. Each entry follows this format:

```python
{
    "week": 1,
    "topic": "Arrays & Hashing",
    "easy": {
        "title": "Contains Duplicate",
        "url": "https://leetcode.com/problems/contains-duplicate/",
        "pattern": "HashSet — check if element already seen",
    },
    "medium": {
        "title": "Group Anagrams",
        "url": "https://leetcode.com/problems/group-anagrams/",
        "pattern": "HashMap — sort each word as key",
    },
},
```

The bot cycles through problems in order, looping back after the last week.

---

## Admin commands (only server admins can use these)

| Command | What it does |
|---|---|
| `!testpost monday` | Posts the current week's easy problem now |
| `!testpost thursday` | Posts the current week's medium problem now |
| `!nextproblem` | Shows current week index |
