# Finalized AI Gold Macro Intelligence System Requirements

## Core Philosophy
**Comprehensive macro-driven gold intelligence system focused on Fed policy, dollar strength, and inflation analysis. Delivers deep fundamental analysis with historical pattern recognition through AI-powered insights.**

---

## 1. Data Sources (All Free/Low-Cost)

### Primary Data Feeds
- **FRED API**: All economic data, Fed policy, yields, employment
- **Yahoo Finance**: DXY, treasury yields, VIX, equity indices (for macro context, no gold prices)
- **CFTC COT Reports**: Weekly positioning data (Fridays ~3:30 PM EST)
- **Fed Communications**: Manual scraping of Fed speeches/statements from Fed.gov
- **NewsAPI.org**: Daily news summary for fundamental analysis

### Economic Calendar
- **Source**: FRED release schedule (build internally from FRED API)
- **Focus**: Major releases only (CPI, NFP, PCE, FOMC, Fed speeches)
- **No third-party calendar APIs needed**

### News Intelligence System
- **Source**: NewsAPI.org (previously used, familiar integration)
- **Frequency**: Daily summary of previous day's key events
- **AI Analysis**: Anthropic processes news for gold market implications
- **Focus**: Fundamental drivers (Fed policy, economic data, central bank actions)
- **Not included**: Real-time breaking news alerts

### Excluded (Cost/Noise Reduction)
- ❌ Real-time price feeds (using TradingView for live data)
- ❌ Gold price tickers (Yahoo Finance doesn't have right contracts)
- ❌ Live breaking news alerts  
- ❌ High-frequency options flow data
- ❌ Paid economic calendar services

---

## 2. AI Integration Strategy

### Daily AI Usage (5-8 calls/day)
- **Morning Brief**: 2-3 calls (macro regime analysis, event scenarios)
- **News Analysis**: 2-3 calls (previous day's news impact assessment)
- **Deep Analysis**: 1-2 calls (historical pattern recognition, correlation analysis)
- **COT Analysis**: 1 call (weekly, when released)
- **Fed Communication**: 1-2 calls (as speeches occur)

### Caching Strategy
- **No caching initially** - Real-time data processing
- **Future consideration**: Add caching if API costs become significant

---

## 3. Delivery System

### Email Infrastructure
- **Provider**: Gmail SMTP
- **Format**: Plain text (no HTML/mobile optimization)
- **Delivery Times**: 8:00 AM Sydney (5:00 PM EST previous day)
- **Style**: Short, concise, numbers/prices/movements prioritized

### Email Types
1. **Daily Macro Brief** (Mon-Fri, 8 AM Sydney) - Comprehensive 4-section analysis
2. **Weekly Deep Dive** (Sunday, 8 AM Sydney) - Strategic macro outlook  
3. **COT Analysis Alert** (Friday evenings, when CFTC releases data)
4. **Fed Speech Analysis** (Within 1 hour of major Fed communications)

---

## 4. Comprehensive Daily Email Structure (Single Email with 4 Sections)

### Section 1: Executive Summary (30-second read)
```
GOLD MACRO INTELLIGENCE - Tuesday, Jan 16, 2025

EXECUTIVE SUMMARY:
Fed Bias: DOVISH SHIFT | Macro Confidence: 75%
DXY: 104.15 (-0.1% yesterday) | 10Y: 4.48% (+2bp) | VIX: 18.2
Key Catalyst: Core CPI 8:30 AM EST - Critical for Fed policy direction

GOLD FUNDAMENTAL OUTLOOK: BULLISH
Confidence: 75% | Risk Level: Moderate (CPI event week)
Key Drivers: Fed dovish shift + DXY weakness + falling real yields
```

### Section 2: News Analysis (Previous Day's Events)
```
YESTERDAY'S NEWS ANALYSIS:

🏛️ Fed's Waller Speech: "Data supports slower pace of hikes"
Market Reaction: DXY -0.3%, 10Y yields -4bp
Gold Implication: BULLISH - Dovish Fed pivot narrative strengthening
AI Assessment: 70% probability Fed pauses at next meeting

📊 Retail Sales Miss: -0.2% vs +0.1% expected  
Market Reaction: Growth concerns, recession probability increased
Gold Implication: BULLISH - Safe haven demand + easier Fed policy
Historical Context: Retail sales misses during Fed hiking cycles average +$18 gold move

🌍 ECB Officials: "Inflation target within reach"
Market Reaction: EUR weakness vs USD
Gold Implication: NEUTRAL - Supports global easing theme but no direct USD impact

AI NEWS SYNTHESIS:
"Combined dovish Fed signals + growth concerns create bullish macro environment for gold. 
Historical precedent: Similar news combinations led to gold outperformance 68% of time."
```

### Section 3: Deep Fundamental Analysis (Numbers + Historical Patterns)
```
DEEP MACRO ANALYSIS:

🏛️ FED POLICY DEEP DIVE:
Current Fed Funds Rate: 5.25%
Neutral Rate Estimate: 2.75% (Fed's own projection)
Policy Restrictiveness: +2.5% above neutral (highly restrictive)
Real Interest Rate: 5.25% - 3.1% CPI = 2.15% (well above historical 0-1%)

6-Month Rate Trend: +0.75% (likely at cycle peak)
Fed Communication Shift: 65% more dovish language vs 3 months ago (AI analysis)

AI HISTORICAL PATTERN ANALYSIS:
"Current setup mirrors December 2018 Fed pause conditions:
- Real rates: 2.15% now vs 2.3% then
- Policy restrictiveness: Similar +2.5% above neutral
- Economic data: Growth slowing, inflation declining
- Gold performance after similar setups: +8.2% over 3 months (avg of 5 instances)
- Pattern confidence: 78% based on macro similarity"

Gold Impact Assessment: STRONGLY BULLISH (-0.7 score)
Reasoning: Real rates at restrictive extremes typically mark gold lows

💵 DXY FUNDAMENTAL ANALYSIS:
Current Level: 104.15
6-Month Range: 100.2 - 106.8 (currently in upper third)
Fed vs Other Central Banks: US 5.25%, ECB 4.5%, BOJ 0.1% (advantage narrowing)
Economic Divergence Score: -0.3 (US growth advantage fading)

Technical Pattern: Potential double top formation at 105-106
Volume Analysis: Declining volume on recent highs (bearish divergence)
RSI Divergence: Negative vs price action (momentum weakening)

AI HISTORICAL PATTERN ANALYSIS:
"DXY double tops above 105 level (occurred 6 times since 2000):
- Reversal success rate: 73% (4 of 6 times led to significant decline)
- Average decline: -4.8% over 3 months
- Gold correlation during DXY reversals: +0.82 (very strong)
- Avg gold gain during DXY reversals: +$87 over 3 months"

Gold Impact Assessment: BULLISH (-0.4 score)
Reasoning: DXY momentum waning, technical reversal pattern forming

📈 INFLATION & REAL YIELDS ANALYSIS:
Current CPI YoY: 3.1% | Core CPI: 3.8% | Fed Target: 2.0%
Inflation Trend: Decelerating (peak 9.1% June 2022 → 3.1% current)
Real 10Y Yield: 4.48% - 3.1% = 1.38%
Historical Real Yield Range: 0.5% - 1.0% (current level elevated)

Breakeven Inflation (5Y): 2.4% (near Fed target, stable expectations)
Fed's Preferred PCE: 2.9% (closer to target than CPI)

AI HISTORICAL CORRELATION ANALYSIS:
"Real yields vs Gold correlation: -0.89 (very strong inverse relationship)
Real yield inflection points (historical analysis):
- When real yields >1.5%: Gold typically underperforms
- When real yields fall below 1.0%: Gold averages +$150-250 gains
- Current real yield 1.38% = critical transition zone
- Fed policy pivots historically cause 50-100bp real yield decline"

Gold Impact Assessment: TRANSITIONING BULLISH (+0.2 score, improving)
Reasoning: Real yields approaching inflection point, Fed pivot = catalyst

🔗 CROSS-ASSET CORRELATION MATRIX:
Gold vs DXY: -0.83 (strong negative, normal)
Gold vs Real Yields: -0.89 (very strong negative, elevated)
Gold vs VIX: +0.34 (weak positive, below normal +0.60)
Gold vs 10Y Yields: -0.72 (strong negative, normal)

Correlation Breakdown Alert: Gold-VIX correlation weakened
AI Analysis: "Suggests gold demand driven by currency debasement rather than fear.
Similar breakdown in 2020 preceded major gold rally as inflation hedging dominated."
```

### Section 4: Signal Status & Risk Assessment
```
MACRO SIGNAL STATUS:

OVERALL ASSESSMENT:
Macro Score: +0.47 (Moderately Bullish for Gold)
Component Breakdown:
• Fed Policy: +0.7 (Strong dovish shift developing)  
• DXY Fundamentals: +0.4 (Technical and fundamental weakness)
• Real Yields: +0.2 (Approaching bullish inflection point)
• Risk Sentiment: +0.1 (Neutral, no major fear or complacency)

CONFIDENCE ANALYSIS:
Overall Confidence: 75%
• Data Quality: HIGH (Fresh Fed communications, clear economic trends)
• Component Agreement: STRONG (All major factors aligned bullish)
• Historical Pattern Match: GOOD (78% correlation with similar periods)
• Event Risk: MODERATE (CPI release could cause temporary volatility)

RISK LEVEL ASSESSMENT:
Current Environment: MODERATE RISK
Risk Factors:
• CPI release within 24 hours (binary outcome potential)
• Fed speakers could contradict dovish narrative
• Technical levels (DXY 104, 10Y yield 4.5%) at key decision points

Risk Mitigation:
• Wait for CPI confirmation before major positioning
• Monitor Fed speaker consistency with dovish pivot theme
• Watch for technical level breaks to confirm fundamental analysis

POSITION SIZING GUIDANCE:
Base Risk Framework: 2% of account capital
Current Adjustments:
• High Confidence Bonus: +15% (strong fundamental alignment)
• Event Risk Penalty: -25% (CPI binary risk)
• Net Recommended Risk: 1.7% of capital

Sizing Strategy:
• Pre-CPI: Reduced size or wait for confirmation
• Post-CPI (if supportive): Normal to slightly elevated sizing
• Stop Loss Guidance: Use technical levels, not fundamental changes

UPCOMING CATALYSTS:
Today: Core CPI 8:30 AM EST (High Impact)
Tomorrow: Fed's Williams speech (Medium Impact) 
This Week: Retail Sales, FOMC Minutes (Medium Impact)

Strategic Positioning:
"Macro fundamentals strongly support gold, but tactical patience 
recommended until CPI confirms Fed pivot narrative."
```

---

## 5. Macro Fundamental Analysis Framework

### Fed Policy Assessment (-1 to +1 Gold Impact Score)
```
Components:
- Current rate vs neutral (2.5-3.0%)
- Rate trend (6-month change)
- Real interest rates (fed rate - inflation)
- Policy stance language analysis

Weighting: 50% of overall macro assessment
Gold Impact: 
- Score < -0.5 = Bullish (dovish policy)
- Score > 0.5 = Bearish (hawkish policy)
```

### DXY Fundamental Analysis (-1 to +1)  
```
Components:
- Technical momentum and trend
- Fed policy vs other central banks
- Cross-currency strength signals
- Economic data divergence

Weighting: 30% of overall assessment
Gold Impact: Inverse correlation
- Strong DXY fundamentals = Bearish Gold
- Weak DXY fundamentals = Bullish Gold
```

### Inflation Environment (0 to +1)
```
Components:
- CPI YoY vs Fed target (2%)
- Trend acceleration/deceleration
- Breakeven inflation expectations
- Real yield implications

Weighting: 20% of overall assessment
Gold Impact: Higher inflation typically bullish
```

---

## 6. Weekly Deep Dive Structure

### Previous Week Analysis
- **High-impact events and macro responses**
- **AI pattern recognition vs historical norms**
- **Positioning changes and market structure shifts**
- **What worked/didn't work in analysis**

### Coming Week Intelligence
- **Critical events with AI scenario analysis**
- **Probability-weighted outcomes**
- **Key levels and macro setups**
- **Risk management adjustments needed**

---

## 7. COT Analysis System

### Trigger: CFTC Release (Fridays ~3:30 PM EST)
```
📊 COT POSITIONING ALERT - Gold Futures

Large Speculators:
• Net Long: 185K contracts (+12K vs last week)
• Positioning: 68% long (ELEVATED - contrarian bearish)

Commercial Hedgers:
• Net Short: -201K contracts (-8K vs last week)  
• Positioning: 82% short (EXTREME - historically significant)

AI HISTORICAL ANALYSIS:
"Similar commercial short extremes occurred in:
- Oct 2022: Gold bottomed 2 weeks later, +$180 rally
- Mar 2021: Gold consolidated 1 month, then +$120 move
- Average subsequent move: +$95 over 6 weeks"

Trading Implication:
Contrarian bullish setup developing. Wait for technical 
confirmation before positioning for medium-term upside.
```

---

## 8. Risk Management Integration (Macro Risk Assessment)

### Macro Risk Assessment Framework
```python
class MacroRiskAssessment:
    def __init__(self):
        self.base_risk_percent = 0.02   # Always 2% base risk
        
    def assess_macro_risk_level(self, macro_data, upcoming_events, market_conditions):
        """
        Macro Risk Level Assessment:
        
        LOW RISK:
        - Clear macro signals (Fed/DXY/inflation aligned)
        - No major events for 48 hours
        - VIX < 20, stable market conditions
        - Recommendation: Normal 2% risk acceptable
        
        MODERATE RISK:
        - Mixed macro signals OR major event within 24 hours OR VIX 20-30
        - Some uncertainty in Fed policy direction
        - DXY at key technical levels
        - Recommendation: Reduce to 1.5% risk
        
        HIGH RISK:
        - Conflicting macro signals AND major event <12 hours AND VIX >30
        - Fed policy uncertainty + economic data surprises
        - Multiple central bank events same week
        - Recommendation: Reduce to 1% risk or avoid trades
        """
        
    def provide_sizing_guidance(self, macro_assessment, risk_level, confidence):
        """
        Position Sizing Guidance (recommendations only):
        
        Base Risk: Always 2% of current account balance
        
        Confidence Adjustments:
        - High confidence (>80%): Can consider normal to slightly larger size
        - Normal confidence (65-80%): Standard sizing appropriate
        - Lower confidence (<65%): Consider reduced sizing or wait
        
        Event Risk Adjustments:
        - Major events (CPI/Fed): Reduce by 25%
        - High volatility (VIX >30): Reduce by 50%
        - Multiple events same week: Reduce by 35%
        """
```

---

## 9. Fed Communication Analysis

### Automated Fed Speech Monitoring
```python
class FedSpeechAnalyzer:
    def monitor_fed_communications(self):
        # Scrape Fed.gov for new speeches/statements
        # Track major Fed officials: Powell, Williams, Bostic, etc.
        # Trigger AI analysis within 1 hour of publication
        
    def analyze_fed_speech(self, speech_text, speaker):
        """
        AI Natural Language Processing:
        
        1. Hawkish/Dovish Sentiment Scoring
        2. Policy Signal Strength Assessment  
        3. Historical Context Comparison
        4. Gold Market Implications
        5. Confidence Level in Analysis
        
        Output: Professional email analysis within 1 hour
        """
```

---

## 10. Technical Implementation Architecture

### Core Data Pipeline
```python
class MacroIntelligenceOrchestrator:
    def __init__(self):
        # Data Connectors (no gold price data)
        self.fred_connector = FREDConnector(api_key)
        self.yahoo_connector = YahooConnector()  # DXY, yields, VIX only
        self.news_connector = NewsAPIConnector(api_key)
        self.economic_calendar = EconomicCalendarAPI()
        self.cot_data = COTDataConnector()
        
        # AI Analysis Engines
        self.fed_analyzer = FedCommunicationAI(anthropic_key)
        self.news_analyzer = NewsImpactAI(anthropic_key)
        self.dxy_analyzer = DXYFundamentalAI(anthropic_key)
        self.macro_regime_analyzer = MacroRegimeAI(anthropic_key)
        self.historical_pattern_analyzer = HistoricalPatternAI(anthropic_key)
        
        # Risk Assessment System
        self.risk_assessor = MacroRiskAssessment()
        
        # Communication System
        self.email_system = ProfessionalEmailSystem()
        
    async def generate_daily_macro_brief(self):
        """Main orchestration - generates complete 4-section email"""
        # 1. Gather macro data (FRED, DXY, yields, VIX)
        # 2. Analyze previous day's news for gold impact
        # 3. Run deep fundamental analysis with historical patterns
        # 4. Generate comprehensive 4-section email
        # 5. Send at 8 AM Sydney
```

### Main System Components
```python
class GoldMacroIntelligenceSystem:
    def __init__(self):
        # Data Connectors (no gold prices)
        self.fred = FREDConnector(api_key)
        self.yahoo = YahooConnector()  # DXY, yields, VIX only
        self.news = NewsAPIConnector(api_key)
        self.cot = COTDataConnector()
        
        # AI Analysis Engine
        self.anthropic = anthropic.Client(api_key)
        
        # Risk Assessment (no position tracking)
        self.risk_assessor = MacroRiskAssessment()
        
        # Communication System
        self.email = GmailSMTP(credentials)
        
        # Database & Storage  
        self.db = SQLiteDatabase()
        
        # Schedulers
        self.daily_scheduler = APScheduler()
        self.event_monitor = AsyncMonitor()
    
    async def run_daily_macro_brief(self):
        """Executes at 8 AM Sydney daily - generates complete 4-section analysis"""
        
    async def run_weekly_analysis(self):
        """Executes Sunday 8 AM Sydney - strategic macro outlook"""
        
    async def monitor_cot_releases(self):
        """Continuous monitoring for CFTC releases"""
        
    async def monitor_fed_communications(self):
        """Continuous monitoring for Fed speeches"""
```

---

## 11. Success Metrics & Validation

### Phase 1 Technical Milestones (Month 1-2)
- [ ] Daily 4-section brief delivers consistently at 8 AM Sydney
- [ ] AI historical pattern analysis provides valuable insights
- [ ] News analysis adds meaningful context to fundamental outlook
- [ ] Deep fundamental analysis includes quantitative depth
- [ ] Email formatting renders properly as plain text
- [ ] COT analysis triggers automatically on CFTC releases
- [ ] Fed communication analysis works effectively

### Phase 2 Performance Validation (Month 3-4)
- [ ] Historical pattern recognition proves accurate >70% of time
- [ ] Macro risk assessment provides useful guidance
- [ ] AI insights add value vs simple fundamental analysis
- [ ] System reliability >95% uptime
- [ ] Analysis depth satisfies professional research standards

### Phase 3 Business Integration (Month 4-6)
- [ ] Intelligence quality supports trading decisions
- [ ] Foundation ready for integration with trade tracking
- [ ] Documented edge in gold macro analysis
- [ ] Cost-effective operation under $70/month

---

## 12. Cost Structure

### Fixed Costs
- **FRED API**: Free (500 calls/day limit)
- **Yahoo Finance**: Free (DXY, yields, VIX data only)
- **NewsAPI.org**: Free tier (1000 requests/month) or $449/month premium
- **CFTC COT Data**: Free
- **Claude AI**: ~$30-50/month (estimated 250-400 calls/month)
- **Gmail SMTP**: Free
- **VPS Hosting**: ~$10-20/month

### Total Monthly Operating Cost: ~$40-70 (or ~$500 with premium NewsAPI)

This approach delivers comprehensive fundamental analysis with deep historical insights and AI-powered pattern recognition, focusing purely on macro intelligence without trade execution.