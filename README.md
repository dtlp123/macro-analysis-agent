# Simple Macro Agent for Gold Trading 🏆

A minimalist macro analysis system that generates daily gold trading signals based on Fed policy and DXY correlation.

## 🎯 Core Philosophy

**Less is more.** This system uses only 5 data points and simple if/then logic to replicate a proven manual trading edge:
- Fed policy drives gold over weeks/months
- Strong dollar usually overrides other factors  
- Simple directional bias beats complex analysis

## 📊 Features

### Dynamic Capital Management ✨ NEW!
- **Automatic Balance Tracking**: Position sizes adjust as your account grows/shrinks
- **Trade Recording**: Log wins/losses to update balance automatically
- **Performance Statistics**: Track win rate, drawdown, and returns
- **Manual Adjustments**: Add deposits, withdrawals, or corrections anytime

### Signal Generation
- **Daily Analysis**: Runs at 8 AM Sydney time
- **Simple Logic**: Fed rate + DXY = Clear signal
- **Risk Management**: 2% risk per trade (configurable)
- **Email Delivery**: Plain text signals to your inbox

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

### 2. Initial Setup
```bash
# Test the system
python run_once.py

# Set your starting capital (interactive)
python trade_manager.py
# Select option 2 → Set new balance → Enter your amount
```

### 3. Daily Operation
```bash
# Run the agent (will execute daily at 8 AM)
python simple_macro_agent.py
```

## 💰 Capital Management

### Recording Trades
After each trade closes, update your balance:

```bash
python trade_manager.py
```

Select option 1 (Record Trade) and enter:
- Signal taken (LONG/SHORT)
- Entry and exit prices
- Position size
- The system calculates P&L automatically

### Viewing Performance
```bash
python trade_manager.py
```
- Option 3: View statistics (win rate, drawdown, returns)
- Option 4: View recent trades
- Option 5: Export full performance report

### Adding/Withdrawing Funds
```bash
python trade_manager.py
```
- Option 2: Update balance
- Choose deposit, withdrawal, or set new balance

## 📧 Daily Email Format

```
ACCOUNT STATUS
Current Balance: $10,500.00 (+5.0% return)
Win Rate: 60.0% (3W/2L)

MACRO ENVIRONMENT
Fed Environment: 5.25% - Hawkish assessment
DXY Status: 106.5 - Strong vs gold

Signal: SHORT
Reasoning: Fed remains hawkish at 5.25% with DXY strength at 106.5 
confirming dollar dominance. This combination typically pressures gold lower.

TRADE PARAMETERS
Entry: $1,950.00
Stop: $1,969.50
Target: $1,911.00
Position Size: 10.8 units ($21,060 value)
Risk: 2% account ($210 on $10,500 account)

RECENT PERFORMANCE
Last 5 trades: W W L W L
Max Drawdown: 4.2%
```

## 📁 File Structure

```
macro-analysis-agent/
├── simple_macro_agent.py    # Main controller
├── data_fetcher.py          # FRED & Yahoo data
├── signal_generator.py      # Fed + DXY logic
├── capital_manager.py       # Balance & trade tracking
├── trade_manager.py         # CLI for recording trades
├── run_once.py             # Test script
├── capital_data.json       # Your balance & history (auto-created)
├── data_snapshots/         # Daily data backups
└── .env                    # Your configuration
```

## 🔧 Configuration

Edit `.env` file:
```bash
# Starting balance (can change anytime)
INITIAL_CAPITAL=25000

# Risk per trade (% of current balance)
RISK_PERCENTAGE=1.5

# Email settings
EMAIL_TO=your.email@gmail.com
```

## 📈 Signal Logic

### Fed Policy Assessment
- **Above 5%** → Bearish gold bias
- **3-5%** → Neutral, watch DXY
- **Below 3%** → Bullish gold bias

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

- **FRED API**: Free
- **Yahoo Finance**: Free
- **Claude AI**: ~$10-15/month (1 call/day)
- **Total**: Under $20/month

## 🔒 Data Security

- Capital data stored locally in `capital_data.json`
- Automatic backups before any reset
- No external database required
- All data under your control

## 📝 Maintenance

### Weekly Tasks
- Record closed trades via `trade_manager.py`
- Review performance statistics
- Verify email delivery

### Monthly Tasks
- Export performance report
- Review signal accuracy vs manual decisions
- Adjust risk percentage if needed

## ⚠️ Important Notes

1. **Paper Trade First**: Test for 4-8 weeks before live trading
2. **Record All Trades**: Keep the system updated for accurate position sizing
3. **Manual Override**: You can always skip signals you don't agree with
4. **Backup Data**: The `capital_data.json` file contains your history - back it up!

## 🚨 Troubleshooting

### Email not arriving?
- Check spam folder
- Verify SMTP settings in `.env`
- For Gmail, use app-specific password

### Wrong balance showing?
- Run `python trade_manager.py`
- Option 2 → Set new balance

### Need to start over?
- Run `python trade_manager.py`
- Option 6 → Reset account (creates backup first)

## 📊 Success Metrics

Target performance after 3 months:
- **Signal Frequency**: 3-5 trades/month
- **Win Rate**: >50%
- **Risk-Reward**: 1:2 minimum
- **Max Drawdown**: <10%
- **Time Saved**: 30+ minutes/day

## 🎯 Philosophy Reminder

> "The system replicates your existing manual trading edge with less daily time investment. If it doesn't improve upon your current approach within 8 weeks, abandon the project rather than adding complexity."

Keep it simple. Let it run. Record your trades. Trust the process.

---

For support, check the logs in `macro_agent.log` or run `python run_once.py` for testing.
