 # "
#Trade Manager CLI
#Interactive tool to manage capital and record trades
#"

import sys
from datetime import datetime
from capital_manager import CapitalManager


class TradeManagerCLI:
    """Command-line interface for managing trades and capital"""
    
    def __init__(self):
        self.manager = CapitalManager()
        self.commands = {
            '1': self.record_trade,
            '2': self.update_balance,
            '3': self.view_statistics,
            '4': self.view_recent_trades,
            '5': self.export_report,
            '6': self.reset_account,
            '7': self.exit_program
        }
    
    def run(self):
        """Main CLI loop"""
        print("\n" + "="*60)
        print("TRADE MANAGER - Capital & Performance Tracking")
        print("="*60)
        
        while True:
            self.show_menu()
            choice = input("\nSelect option (1-7): ").strip()
            
            if choice in self.commands:
                self.commands[choice]()
            else:
                print("❌ Invalid option. Please try again.")
    
    def show_menu(self):
        """Display main menu"""
        balance = self.manager.get_current_balance()
        stats = self.manager.get_statistics()
        
        print(f"\n📊 Current Balance: ${balance:,.2f} ({stats['total_return_pct']:+.1f}%)")
        print(f"📈 Win Rate: {stats['win_rate']:.1f}% | Trades: {stats['total_trades']}")
        print("\n" + "-"*40)
        print("1. Record Trade Result")
        print("2. Update Balance (Deposit/Withdrawal)")
        print("3. View Statistics")
        print("4. View Recent Trades")
        print("5. Export Performance Report")
        print("6. Reset Account (⚠️ Warning)")
        print("7. Exit")
    
    def record_trade(self):
        """Record a completed trade"""
        print("\n📝 RECORD TRADE RESULT")
        print("-"*40)
        
        try:
            # Get trade details
            signal = input("Signal (LONG/SHORT): ").upper()
            if signal not in ['LONG', 'SHORT']:
                print("❌ Invalid signal. Must be LONG or SHORT.")
                return
            
            entry = float(input("Entry price: $"))
            exit_price = float(input("Exit price: $"))
            position_size = float(input("Position size (units): "))
            
            # Calculate P&L
            if signal == 'LONG':
                pnl = (exit_price - entry) * position_size
            else:
                pnl = (entry - exit_price) * position_size
            
            date_opened = input("Date opened (YYYY-MM-DD) or press Enter for today: ").strip()
            if not date_opened:
                date_opened = datetime.now().strftime('%Y-%m-%d')
            
            date_closed = input("Date closed (YYYY-MM-DD) or press Enter for today: ").strip()
            if not date_closed:
                date_closed = datetime.now().strftime('%Y-%m-%d')
            
            reason = input("Close reason (target/stop/manual): ").strip() or "manual"
            
            # Confirm trade
            print(f"\n📊 Trade Summary:")
            print(f"  Signal: {signal}")
            print(f"  Entry: ${entry:.2f}")
            print(f"  Exit: ${exit_price:.2f}")
            print(f"  Size: {position_size} units")
            print(f"  P&L: ${pnl:+.2f}")
            
            confirm = input("\nConfirm trade (y/n): ").lower()
            if confirm == 'y':
                trade = {
                    'signal': signal,
                    'entry': entry,
                    'exit': exit_price,
                    'position_size': position_size,
                    'pnl': pnl,
                    'date_opened': date_opened,
                    'date_closed': date_closed,
                    'reason': reason
                }
                
                self.manager.record_trade(trade)
                print(f"✅ Trade recorded! New balance: ${self.manager.get_current_balance():,.2f}")
            else:
                print("❌ Trade cancelled.")
                
        except ValueError as e:
            print(f"❌ Invalid input: {e}")
        except Exception as e:
            print(f"❌ Error recording trade: {e}")
    
    def update_balance(self):
        """Update account balance (deposit/withdrawal)"""
        print("\n💰 UPDATE BALANCE")
        print("-"*40)
        
        current = self.manager.get_current_balance()
        print(f"Current balance: ${current:,.2f}")
        
        try:
            print("\n1. Deposit")
            print("2. Withdrawal")
            print("3. Set new balance")
            
            choice = input("\nSelect option (1-3): ").strip()
            
            if choice == '1':
                amount = float(input("Deposit amount: $"))
                new_balance = current + amount
                reason = input("Reason (optional): ").strip() or "Deposit"
                self.manager.update_balance(new_balance, reason)
                print(f"✅ Deposited ${amount:,.2f}. New balance: ${new_balance:,.2f}")
                
            elif choice == '2':
                amount = float(input("Withdrawal amount: $"))
                if amount > current:
                    print("❌ Insufficient funds!")
                    return
                new_balance = current - amount
                reason = input("Reason (optional): ").strip() or "Withdrawal"
                self.manager.update_balance(new_balance, reason)
                print(f"✅ Withdrew ${amount:,.2f}. New balance: ${new_balance:,.2f}")
                
            elif choice == '3':
                new_balance = float(input("New balance: $"))
                reason = input("Reason: ").strip() or "Manual adjustment"
                self.manager.update_balance(new_balance, reason)
                print(f"✅ Balance set to ${new_balance:,.2f}")
                
            else:
                print("❌ Invalid option.")
                
        except ValueError:
            print("❌ Invalid amount.")
        except Exception as e:
            print(f"❌ Error updating balance: {e}")
    
    def view_statistics(self):
        """View detailed statistics"""
        stats = self.manager.get_statistics()
        
        print("\n📊 TRADING STATISTICS")
        print("="*50)
        print(f"Current Balance:     ${stats['current_balance']:>12,.2f}")
        print(f"Total Return:        {stats['total_return_pct']:>11.1f}%")
        print(f"Peak Balance:        ${stats['peak_balance']:>12,.2f}")
        print(f"Max Drawdown:        {stats['drawdown']:>11.1f}%")
        print("-"*50)
        print(f"Total Trades:        {stats['total_trades']:>12}")
        print(f"Winning Trades:      {stats['winning_trades']:>12}")
        print(f"Losing Trades:       {stats['losing_trades']:>12}")
        print(f"Win Rate:            {stats['win_rate']:>11.1f}%")
        print(f"Total P&L:           ${stats['total_pnl']:>12,.2f}")
        print(f"Largest Win:         ${stats['largest_win']:>12,.2f}")
        print(f"Largest Loss:        ${stats['largest_loss']:>12,.2f}")
        
        input("\nPress Enter to continue...")
    
    def view_recent_trades(self):
        """View recent trades"""
        trades = self.manager.get_recent_trades(10)
        
        print("\n📈 RECENT TRADES (Last 10)")
        print("="*70)
        
        if not trades:
            print("No trades recorded yet.")
        else:
            print(f"{'#':<4} {'Signal':<7} {'Entry':<10} {'Exit':<10} {'P&L':<12} {'Date':<12}")
            print("-"*70)
            
            for trade in trades:
                trade_id = trade.get('id', 'N/A')
                signal = trade.get('signal', 'N/A')
                entry = trade.get('entry', 0)
                exit_price = trade.get('exit', 0)
                pnl = trade.get('pnl', 0)
                date = trade.get('date_closed', 'N/A')[:10]
                
                pnl_color = "🟢" if pnl > 0 else "🔴"
                print(f"{trade_id:<4} {signal:<7} ${entry:<9.2f} ${exit_price:<9.2f} "
                      f"{pnl_color} ${pnl:>8.2f} {date:<12}")
        
        input("\nPress Enter to continue...")
    
    def export_report(self):
        """Export performance report"""
        report = self.manager.export_performance_report()
        
        print(report)
        
        save = input("\nSave to file? (y/n): ").lower()
        if save == 'y':
            filename = f"performance_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            with open(filename, 'w') as f:
                f.write(report)
            print(f"✅ Report saved to {filename}")
        
        input("\nPress Enter to continue...")
    
    def reset_account(self):
        """Reset account (with confirmation)"""
        print("\n⚠️  WARNING: ACCOUNT RESET")
        print("-"*40)
        print("This will DELETE all trade history!")
        print("A backup will be created before reset.")
        
        confirm = input("\nType 'RESET' to confirm: ").strip()
        if confirm == 'RESET':
            try:
                new_balance = input("Enter new starting balance (or press Enter for $10,000): ").strip()
                if new_balance:
                    new_balance = float(new_balance)
                else:
                    new_balance = 10000.0
                
                self.manager.reset_account(new_balance)
                print(f"✅ Account reset to ${new_balance:,.2f}")
                print("Previous data has been backed up.")
            except ValueError:
                print("❌ Invalid balance amount.")
        else:
            print("❌ Reset cancelled.")
    
    def exit_program(self):
        """Exit the program"""
        print("\n👋 Goodbye!")
        sys.exit(0)


if __name__ == "__main__":
    cli = TradeManagerCLI()
    cli.run()

