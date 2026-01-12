# Daily Tasks

Automated daily tasks powered by GitHub Actions:

- **MiYouShe Sign-in** - Game check-in for Honkai: Star Rail, Genshin Impact, etc.
- **Weather Report** - Daily weather forecast for Singapore
- **Anime Updates** - Daily anime broadcast notifications
- **Conference Deadlines** - Security & Cryptography conference deadline reminders

All results are pushed to WeChat via **PushPlus**.

## Features

### 1. MiYouShe Sign-in
- Supports: Honkai: Star Rail (enabled), Genshin Impact, Honkai Impact 3, Zenless Zone Zero
- Automatically detects bound game characters
- Enable/disable games: edit `GAMES` config in `tasks/miyoushe.py`

### 2. Weather Report
- Uses Singapore Government free API (data.gov.sg)
- Pushes daily temperature, humidity, and forecast
- Customizable area (default: Queenstown / NUS area)

### 3. Anime Updates
- Uses Bangumi API to get daily broadcast schedule
- Configurable watchlist to filter notifications
- Shows all updates if watchlist is empty

### 4. Conference Deadlines
- Tracks Security & Cryptography conference deadlines
- Data source: [sec-deadlines.github.io](https://sec-deadlines.github.io/)
- Configurable tags filter (SEC, CRYPTO, PRIV, etc.)
- Shows deadlines within configurable days ahead (default: 30 days)
- Urgency indicators: 🔴 TODAY, 🟠 ≤3 days, 🟡 ≤7 days, 🟢 >7 days

## Setup

### 1. Fork this repository

### 2. Configure Secrets

Go to `Settings` → `Secrets and variables` → `Actions`:

| Secret | Required | Description |
|--------|----------|-------------|
| `MIYOUSHE_COOKIE` | Yes | MiYouShe Cookie |
| `WECOM_WEBHOOK` | No* | WeCom Bot Webhook URL |
| `PUSHPLUS_TOKEN` | No* | PushPlus Token (fallback) |

*At least one push method required. WeCom is recommended for instant notifications.

### 3. Configure Variables (Optional)

In `Settings` → `Secrets and variables` → `Actions` → `Variables`:

| Variable | Default | Description |
|----------|---------|-------------|
| `WEATHER_AREA` | `Queenstown` | Singapore weather area |
| `BANGUMI_WATCHLIST` | empty | Anime watchlist, comma-separated |
| `CONF_DAYS_AHEAD` | `30` | Show deadlines within N days |
| `CONF_FILTER_TAGS` | `SEC,CRYPTO` | Filter by conference tags |

**Singapore Area Examples**:
- `Queenstown` - NUS Main Campus
- `Bukit Timah` - NUS Law School
- `Orchard` - Orchard Road
- `Jurong East` / `Jurong West`
- `Tampines` / `Bedok` / `Pasir Ris`

**Watchlist Example**:
```
Frieren,Jujutsu Kaisen,Attack on Titan
```

**Conference Tags Example**:
```
SEC,CRYPTO,PRIV
```
Available tags: `SEC` (Security), `CRYPTO` (Cryptography), `PRIV` (Privacy), `CONF` (Conference), `TOP4` (Top 4 venues)

### 4. Enable Actions

Go to `Actions` tab and enable the workflow.

### 5. Test

Click `Run workflow` to manually trigger a test run.

## Schedule

Runs daily at **8:00 AM SGT** (UTC 0:00).

To change: edit cron expression in `.github/workflows/sign.yml`.

## Project Structure

```
├── main.py                 # Entry point
├── tasks/
│   ├── miyoushe.py         # MiYouShe sign-in
│   ├── weather.py          # Weather report
│   ├── bangumi.py          # Anime updates
│   └── conference.py       # Conference deadlines
├── utils/
│   └── push.py             # Push notifications
├── .github/workflows/
│   └── sign.yml            # GitHub Actions config
└── README.md
```

## Adding New Tasks

1. Create a new module in `tasks/`
2. Implement `run()` function returning a message string or list
3. Import and call it in `main.py`

## Disclaimer

For personal use and learning purposes only.
