# Simple Macro Agent for Gold Trading 🏆

A minimalist macro analysis system that generates daily gold trading signals based on Fed policy and DXY correlation.

## 🎯 Core Philosophy

**Less is more.** This system uses only 4 data points and simple if/then logic to replicate a proven manual trading edge:
- Fed policy drives gold over weeks/months
- Strong dollar usually overrides other factors  
- Simple directional bias beats complex analysis

## 📊 Features

### Signal Generation
- **Daily Analysis**: Runs at 8 AM Sydney time (weekdays only)
- **Simple Logic**: Fed rate + DXY = Clear signal
- **Email Delivery**: Plain text signals to your inbox
- **AI Enhancement**: Claude AI provides reasoning and context

### Data Sources
- **FRED API**: Federal Funds Rate, 10Y Treasury, CPI
- **Yahoo Finance**: DXY (US Dollar Index)
- **Note**: Gold price data temporarily unavailable - awaiting more accurate API source

## 🚀 Quick Start

### 1. Installation
```bash
# Clone the repository
git clone [your-repo]
cd macro-analysis-agent

# Install dependencies
pip install -r requirements.txt

# Setup environment
cp .env.template .env
# Edit .env with your API keys
```

### 2. Configuration
Edit `.env` file with your credentials:
```bash
# API Keys
FRED_API_KEY=your_fred_api_key
ANTHROPIC_API_KEY=your_anthropic_api_key

# Email Settings
EMAIL_FROM=your.email@gmail.com
EMAIL_TO=recipient@gmail.com
EMAIL_PASSWORD=your_app_password
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
```

### 3. Test Run
```bash
# Test the system locally
python run_once.py
```

### 4. Deploy
The system runs automatically via GitHub Actions:
- **Schedule**: Weekdays at 11 PM UTC (8 AM Sydney)
- **Manual trigger**: Available via GitHub Actions UI
- **Setup**: Add all environment variables as GitHub Secrets

## 📧 Daily Email Format

```
DAILY GOLD MACRO ANALYSIS
Monday, November 04, 2025

SIGNAL: LONG
Confidence: High

MACRO ENVIRONMENT
• Fed Funds Rate: 4.75%
• Fed Bias: Dovish
• DXY Level: 102.5 (Neutral vs gold)
• 10Y Treasury: 4.2%
• Latest CPI: 2.8%

ANALYSIS
The Fed's dovish pivot at 4.75% creates a favorable environment 
for gold as real rates decline. The neutral DXY at 102.5 removes 
the dollar headwind that previously capped gold rallies. Key risk 
to monitor is unexpected economic data strength that could delay 
Fed easing.

---
Last updated: 2025-11-04 08:00:15

Note: Gold price data temporarily unavailable - awaiting more accurate API source.
```

## 📁 File Structure

```
macro-analysis-agent/
├── main.py                      # Main orchestrator
├── data_fetcher.py             # FRED & Yahoo data retrieval
├── signal_generator.py         # Fed + DXY logic
├── config.py                   # Configuration settings
├── production_runner.py        # GitHub Actions entry point
├── run_once.py                # Local testing script
├── data_snapshots/            # Daily data backups (auto-created)
├── .github/workflows/         # GitHub Actions automation
│   └── daily-analysis.yml
├── requirements.txt           # Python dependencies
├── .env                      # Your configuration (not in git)
└── .gitignore               # Git exclusions
```

## 📈 Signal Logic

### Fed Policy Assessment
- **Above 5%** → Hawkish (bearish gold bias)
- **3-5%** → Neutral (watch DXY)
- **Below 3%** → Dovish (bullish gold bias)

### DXY Confirmation
- **>105** → Strong dollar (bearish gold)
- **100-105** → Neutral
- **<100** → Weak dollar (bullish gold)

### Signal Matrix
| Fed Policy | DXY Weak | DXY Neutral | DXY Strong |
|------------|----------|-------------|------------|
| Dovish     | LONG ✅  | LONG ✅     | WAIT ⏸️    |
| Neutral    | LONG ✅  | WAIT ⏸️     | SHORT ❌   |
| Hawkish    | WAIT ⏸️  | SHORT ❌    | SHORT ❌   |

## 💵 Costs

- **FRED API**: Free (500 calls/day limit)
- **Yahoo Finance**: Free
- **Claude AI**: ~$10-15/month (1 call/day)
- **GitHub Actions**: Free (public repo)
- **Total**: Under $20/month

## 🔒 Security

- All sensitive data in `.env` file (not committed)
- GitHub Secrets for production environment
- API keys never logged or exposed
- Local data storage only

## 📝 Maintenance

### Daily Tasks
- Review email signals
- Check for any error notifications

### Weekly Tasks
- Review GitHub Actions logs
- Verify all emails delivered successfully

### Monthly Tasks
- Review signal accuracy
- Check API usage and costs
- Update fallback values in config.py if needed

## ⚠️ Important Notes

1. **Paper Trade First**: Test signals for 4-8 weeks before live trading
2. **Manual Override**: Always apply your own judgment to signals
3. **Data Quality**: System includes fallback values for API failures
4. **Weekdays Only**: Runs Monday-Friday, skips weekends
5. **Gold Price**: Temporarily unavailable until better API source found

## 🚨 Troubleshooting

### Email not arriving?
- Check spam folder
- Verify SMTP settings in `.env`
- For Gmail, use app-specific password
- Check GitHub Actions logs for errors

### Data fetch errors?
- Check FRED API key is valid
- Verify internet connectivity
- System uses fallback values automatically
- Check `macro_agent.log` for details

### GitHub Actions failing?
- Verify all secrets are set correctly
- Check workflow file syntax
- Review Actions logs in repository
- Ensure Python version matches (3.9+)

## 📊 Success Metrics

Target performance after 3 months:
- **Signal Frequency**: 3-5 trades/month
- **Signal Quality**: Clear directional bias
- **System Uptime**: >95%
- **Email Delivery**: 100%
- **Time Saved**: 30+ minutes/day vs manual analysis

## 🎯 Philosophy Reminder

> "The system replicates your existing manual trading edge with less daily time investment. If it doesn't improve upon your current approach within 8 weeks, abandon the project rather than adding complexity."

Keep it simple. Let it run. Trust the process.

## 🔧 Development

### Running Locally
```bash
# Single test run
python run_once.py

# Continuous scheduler (for testing)
python main.py
```

### Adding Features
When considering new features, ask:
1. Does it improve signal quality?
2. Does it reduce manual work?
3. Does it maintain simplicity?

If no to any of these, don't add it.

## 📖 Documentation

For detailed technical documentation including:
- Architecture diagrams
- Function specifications
- Data flow details
- Configuration options

See: `Macro_Agent_Documentation.docx`

---

For support, check the logs in `macro_agent.log` or run `python run_once.py` for testing.

**Remember**: Simple systems that execute consistently beat complex systems that don't.