"""
Capital Manager Module
Tracks account balance and trade history
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Optional
import logging

logger = logging.getLogger(__name__)


class CapitalManager:
    """
    Manages trading capital and tracks performance.
    Stores data in JSON for simplicity (no database needed).
    """
    
    def __init__(self, initial_capital: float = 10000.0):
        """
        Initialize capital manager with starting balance.
        
        Args:
            initial_capital: Starting account balance (default $10,000)
        """
        self.data_file = "capital_data.json"
        self.initial_capital = initial_capital
        self.data = self._load_data()
        
        logger.info(f"CapitalManager initialized. Current balance: ${self.get_current_balance():,.2f}")
    
    def _load_data(self) -> Dict:
        """Load capital data from JSON file or create new"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    data = json.load(f)
                    logger.info(f"Loaded existing capital data from {self.data_file}")
                    return data
            except Exception as e:
                logger.error(f"Error loading capital data: {e}")
        
        # Create new data structure
        data = {
            'initial_capital': self.initial_capital,
            'current_balance': self.initial_capital,
            'trades': [],
            'balance_history': [
                {
                    'date': datetime.now().isoformat(),
                    'balance': self.initial_capital,
                    'event': 'Account initialized'
                }
            ],
            'statistics': {
                'total_trades': 0,
                'winning_trades': 0,
                'losing_trades': 0,
                'total_pnl': 0.0,
                'win_rate': 0.0,
                'largest_win': 0.0,
                'largest_loss': 0.0,
                'peak_balance': self.initial_capital,
                'drawdown': 0.0
            }
        }
        
        self._save_data(data)
        logger.info(f"Created new capital data file with initial balance: ${self.initial_capital:,.2f}")
        return data
    
    def _save_data(self, data: Dict = None):
        """Save capital data to JSON file"""
        if data is None:
            data = self.data
        
        try:
            with open(self.data_file, 'w') as f:
                json.dump(data, f, indent=2)
            logger.debug(f"Capital data saved to {self.data_file}")
        except Exception as e:
            logger.error(f"Error saving capital data: {e}")
    
    def get_current_balance(self) -> float:
        """Get current account balance"""
        return self.data['current_balance']
    
    def update_balance(self, new_balance: float, reason: str = "Manual update"):
        """
        Manually update account balance.
        
        Args:
            new_balance: New balance amount
            reason: Reason for update (deposit, withdrawal, correction, etc.)
        """
        old_balance = self.data['current_balance']
        self.data['current_balance'] = new_balance
        
        # Add to history
        self.data['balance_history'].append({
            'date': datetime.now().isoformat(),
            'balance': new_balance,
            'change': new_balance - old_balance,
            'event': reason
        })
        
        # Update peak balance
        if new_balance > self.data['statistics']['peak_balance']:
            self.data['statistics']['peak_balance'] = new_balance
        
        # Calculate drawdown
        drawdown = (self.data['statistics']['peak_balance'] - new_balance) / self.data['statistics']['peak_balance'] * 100
        self.data['statistics']['drawdown'] = max(0, drawdown)
        
        self._save_data()
        logger.info(f"Balance updated: ${old_balance:,.2f} → ${new_balance:,.2f} ({reason})")
    
    def record_trade(self, trade: Dict):
        """
        Record a completed trade and update balance.
        
        Args:
            trade: Dict containing trade details
                - signal: LONG/SHORT
                - entry: Entry price
                - exit: Exit price
                - position_size: Position size
                - pnl: Profit/loss in dollars
                - date_opened: When trade was opened
                - date_closed: When trade was closed
                - reason: Why trade was closed (target, stop, manual)
        """
        # Add trade to history
        trade['id'] = len(self.data['trades']) + 1
        trade['date_recorded'] = datetime.now().isoformat()
        self.data['trades'].append(trade)
        
        # Update balance
        pnl = trade.get('pnl', 0)
        new_balance = self.data['current_balance'] + pnl
        self.data['current_balance'] = new_balance
        
        # Update statistics
        stats = self.data['statistics']
        stats['total_trades'] += 1
        stats['total_pnl'] += pnl
        
        if pnl > 0:
            stats['winning_trades'] += 1
            stats['largest_win'] = max(stats['largest_win'], pnl)
        else:
            stats['losing_trades'] += 1
            stats['largest_loss'] = min(stats['largest_loss'], pnl)
        
        # Calculate win rate
        if stats['total_trades'] > 0:
            stats['win_rate'] = stats['winning_trades'] / stats['total_trades'] * 100
        
        # Update peak and drawdown
        if new_balance > stats['peak_balance']:
            stats['peak_balance'] = new_balance
        
        drawdown = (stats['peak_balance'] - new_balance) / stats['peak_balance'] * 100
        stats['drawdown'] = max(0, drawdown)
        
        # Add to balance history
        self.data['balance_history'].append({
            'date': datetime.now().isoformat(),
            'balance': new_balance,
            'change': pnl,
            'event': f"Trade #{trade['id']} closed: {'Win' if pnl > 0 else 'Loss'} ${abs(pnl):.2f}"
        })
        
        self._save_data()
        
        result = "WIN" if pnl > 0 else "LOSS"
        logger.info(f"Trade recorded: {result} ${abs(pnl):.2f} | New balance: ${new_balance:,.2f}")
    
    def get_statistics(self) -> Dict:
        """Get current trading statistics"""
        stats = self.data['statistics'].copy()
        stats['current_balance'] = self.data['current_balance']
        stats['total_return_pct'] = ((self.data['current_balance'] - self.data['initial_capital']) 
                                     / self.data['initial_capital'] * 100)
        return stats
    
    def get_recent_trades(self, count: int = 10) -> List[Dict]:
        """Get recent trades"""
        return self.data['trades'][-count:] if self.data['trades'] else []
    
    def get_balance_history(self, days: int = 30) -> List[Dict]:
        """Get balance history for specified days"""
        if not self.data['balance_history']:
            return []
        
        cutoff_date = datetime.now().timestamp() - (days * 24 * 60 * 60)
        history = []
        
        for entry in self.data['balance_history']:
            entry_date = datetime.fromisoformat(entry['date']).timestamp()
            if entry_date >= cutoff_date:
                history.append(entry)
        
        return history
    
    def calculate_position_size(self, stop_distance: float, risk_percentage: float = 2.0) -> float:
        """
        Calculate position size based on current balance and risk.
        
        Args:
            stop_distance: Dollar distance to stop loss
            risk_percentage: Percentage of account to risk (default 2%)
        
        Returns:
            Position size in units
        """
        current_balance = self.get_current_balance()
        risk_amount = current_balance * (risk_percentage / 100)
        position_size = risk_amount / stop_distance
        
        logger.debug(f"Position size calculated: {position_size:.2f} units "
                    f"(Balance: ${current_balance:.2f}, Risk: ${risk_amount:.2f})")
        
        return position_size
    
    def reset_account(self, new_balance: Optional[float] = None):
        """
        Reset account to initial state or new balance.
        WARNING: This will delete all trade history!
        
        Args:
            new_balance: New starting balance (uses initial_capital if None)
        """
        if new_balance is None:
            new_balance = self.initial_capital
        
        # Backup current data before reset
        backup_file = f"capital_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(backup_file, 'w') as f:
            json.dump(self.data, f, indent=2)
        logger.info(f"Current data backed up to {backup_file}")
        
        # Reset data
        self.initial_capital = new_balance
        self.data = {
            'initial_capital': new_balance,
            'current_balance': new_balance,
            'trades': [],
            'balance_history': [
                {
                    'date': datetime.now().isoformat(),
                    'balance': new_balance,
                    'event': 'Account reset'
                }
            ],
            'statistics': {
                'total_trades': 0,
                'winning_trades': 0,
                'losing_trades': 0,
                'total_pnl': 0.0,
                'win_rate': 0.0,
                'largest_win': 0.0,
                'largest_loss': 0.0,
                'peak_balance': new_balance,
                'drawdown': 0.0
            }
        }
        
        self._save_data()
        logger.info(f"Account reset to ${new_balance:,.2f}")
    
    def export_performance_report(self) -> str:
        """Generate a text performance report"""
        stats = self.get_statistics()
        recent_trades = self.get_recent_trades(5)
        
        report = f"""
TRADING PERFORMANCE REPORT
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
{'='*50}

ACCOUNT SUMMARY
Initial Capital:     ${self.data['initial_capital']:>12,.2f}
Current Balance:     ${stats['current_balance']:>12,.2f}
Total Return:        {stats['total_return_pct']:>11.1f}%
Peak Balance:        ${stats['peak_balance']:>12,.2f}
Max Drawdown:        {stats['drawdown']:>11.1f}%

TRADE STATISTICS
Total Trades:        {stats['total_trades']:>12}
Winning Trades:      {stats['winning_trades']:>12}
Losing Trades:       {stats['losing_trades']:>12}
Win Rate:            {stats['win_rate']:>11.1f}%
Total P&L:           ${stats['total_pnl']:>12,.2f}
Largest Win:         ${stats['largest_win']:>12,.2f}
Largest Loss:        ${stats['largest_loss']:>12,.2f}

RECENT TRADES (Last 5)
{'='*50}
"""
        
        for trade in recent_trades:
            report += f"#{trade['id']:3} | {trade.get('signal', 'N/A'):5} | "
            report += f"P&L: ${trade.get('pnl', 0):>8,.2f} | "
            report += f"{trade.get('date_closed', 'N/A')[:10]}\n"
        
        return report


# Example usage functions
def example_record_winning_trade():
    """Example of recording a winning trade"""
    manager = CapitalManager()
    
    trade = {
        'signal': 'LONG',
        'entry': 2000.00,
        'exit': 2020.00,
        'position_size': 5,
        'pnl': 100.00,  # $100 profit
        'date_opened': '2024-01-15',
        'date_closed': '2024-01-16',
        'reason': 'Target reached'
    }
    
    manager.record_trade(trade)
    print(manager.export_performance_report())


def example_manual_deposit():
    """Example of adding funds to account"""
    manager = CapitalManager()
    
    # Add $5000 to account
    current = manager.get_current_balance()
    manager.update_balance(current + 5000, "Deposit")
    
    print(f"New balance: ${manager.get_current_balance():,.2f}")