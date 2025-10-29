"""
Signal Generator Module
Simple rule-based logic for generating gold trading signals
"""

import logging
from typing import Dict, Tuple
from enum import Enum

logger = logging.getLogger(__name__)


class Signal(Enum):
    """Trading signal types"""
    LONG = "LONG"
    SHORT = "SHORT"
    WAIT = "WAIT"


class SignalGenerator:
    """
    Generates gold trading signals based on simple Fed + DXY logic.
    
    Core Logic:
    1. Fed Rate Environment:
       - Above 5%: Bearish gold bias
       - 3-5%: Neutral, watch DXY
       - Below 3%: Bullish gold bias
    
    2. DXY Confirmation:
       - Strong dollar (>105): Override bullish bias
       - Weak dollar (<100): Confirm bullish bias
       - Neutral (100-105): Defer to Fed policy
    
    3. Signal Output:
       - LONG: Fed dovish + DXY weak
       - SHORT: Fed hawkish + DXY strong
       - WAIT: Mixed signals or unclear data
    """
    
    def __init__(self, anthropic_api_key: str = None):
        # Fed rate thresholds
        self.FED_HAWKISH_THRESHOLD = 5.0
        self.FED_DOVISH_THRESHOLD = 3.0
        
        # DXY thresholds
        self.DXY_STRONG_THRESHOLD = 105.0
        self.DXY_WEAK_THRESHOLD = 100.0
        
        # Store API key for potential future use
        self.anthropic_api_key = anthropic_api_key
        
        logger.info("SignalGenerator initialized with simple rule-based logic")
    
    def generate_signal(self, data: Dict) -> Dict:
        """
        Generate trading signal based on macro data.
        
        Args:
            data: Dict containing fed_rate, treasury_10y, cpi, gold_price, dxy_level
        
        Returns:
            Dict with signal, bias, confidence, and components
        """
        try:
            fed_rate = data.get('fed_rate', 0)
            dxy_level = data.get('dxy_level', 0)
            
            # Step 1: Determine Fed policy bias
            fed_bias = self._assess_fed_policy(fed_rate)
            
            # Step 2: Determine DXY bias
            dxy_bias = self._assess_dxy_strength(dxy_level)
            
            # Step 3: Combine signals
            signal, overall_bias = self._combine_signals(fed_bias, dxy_bias)
            
            # Step 4: Calculate confidence
            confidence = self._calculate_confidence(fed_bias, dxy_bias, data)
            
            result = {
                'signal': signal.value,
                'bias': overall_bias,
                'confidence': confidence,
                'components': {
                    'fed_bias': fed_bias,
                    'dxy_bias': dxy_bias,
                    'fed_rate': fed_rate,
                    'dxy_level': dxy_level
                }
            }
            
            logger.info(f"Signal generated: {signal.value} with {confidence} confidence")
            return result
            
        except Exception as e:
            logger.error(f"Error generating signal: {e}")
            return {
                'signal': Signal.WAIT.value,
                'bias': 'Neutral',
                'confidence': 'Low',
                'components': {}
            }
    
    def _assess_fed_policy(self, fed_rate: float) -> str:
        """
        Assess Fed policy stance based on rate level.
        
        Returns: 'Hawkish', 'Neutral', or 'Dovish'
        """
        if fed_rate >= self.FED_HAWKISH_THRESHOLD:
            return 'Hawkish'
        elif fed_rate <= self.FED_DOVISH_THRESHOLD:
            return 'Dovish'
        else:
            return 'Neutral'
    
    def _assess_dxy_strength(self, dxy_level: float) -> str:
        """
        Assess DXY strength and its impact on gold.
        
        Returns: 'Strong', 'Neutral', or 'Weak'
        """
        if dxy_level >= self.DXY_STRONG_THRESHOLD:
            return 'Strong'
        elif dxy_level <= self.DXY_WEAK_THRESHOLD:
            return 'Weak'
        else:
            return 'Neutral'
    
    def _combine_signals(self, fed_bias: str, dxy_bias: str) -> Tuple[Signal, str]:
        """
        Combine Fed and DXY signals to generate trading signal.
        
        Signal Matrix:
        Fed Dovish + DXY Weak = LONG (Strong Bullish)
        Fed Dovish + DXY Neutral = LONG (Bullish)
        Fed Dovish + DXY Strong = WAIT (Mixed)
        
        Fed Neutral + DXY Weak = LONG (Bullish)
        Fed Neutral + DXY Neutral = WAIT (Neutral)
        Fed Neutral + DXY Strong = SHORT (Bearish)
        
        Fed Hawkish + DXY Weak = WAIT (Mixed)
        Fed Hawkish + DXY Neutral = SHORT (Bearish)
        Fed Hawkish + DXY Strong = SHORT (Strong Bearish)
        """
        
        # Define signal matrix
        signal_matrix = {
            ('Dovish', 'Weak'): (Signal.LONG, 'Strong Bullish'),
            ('Dovish', 'Neutral'): (Signal.LONG, 'Bullish'),
            ('Dovish', 'Strong'): (Signal.WAIT, 'Mixed - DXY Override'),
            
            ('Neutral', 'Weak'): (Signal.LONG, 'Bullish'),
            ('Neutral', 'Neutral'): (Signal.WAIT, 'Neutral'),
            ('Neutral', 'Strong'): (Signal.SHORT, 'Bearish'),
            
            ('Hawkish', 'Weak'): (Signal.WAIT, 'Mixed - Conflicting'),
            ('Hawkish', 'Neutral'): (Signal.SHORT, 'Bearish'),
            ('Hawkish', 'Strong'): (Signal.SHORT, 'Strong Bearish'),
        }
        
        return signal_matrix.get((fed_bias, dxy_bias), (Signal.WAIT, 'Uncertain'))
    
    def _calculate_confidence(self, fed_bias: str, dxy_bias: str, data: Dict) -> str:
        """
        Calculate confidence level based on signal clarity.
        
        High confidence: Clear alignment between Fed and DXY
        Medium confidence: One factor neutral, other clear
        Low confidence: Mixed or conflicting signals
        """
        fed_rate = data.get('fed_rate', 0)
        dxy_level = data.get('dxy_level', 0)
        
        # Check for strong signals
        strong_conditions = [
            (fed_bias == 'Dovish' and dxy_bias == 'Weak'),      # Strong bullish
            (fed_bias == 'Hawkish' and dxy_bias == 'Strong'),   # Strong bearish
            (fed_rate < 2.0),                                    # Very low rates
            (fed_rate > 6.0),                                    # Very high rates
            (dxy_level < 95),                                    # Very weak dollar
            (dxy_level > 110),                                   # Very strong dollar
        ]
        
        if any(strong_conditions):
            return 'High'
        
        # Check for medium confidence conditions
        medium_conditions = [
            (fed_bias in ['Dovish', 'Hawkish'] and dxy_bias == 'Neutral'),
            (fed_bias == 'Neutral' and dxy_bias in ['Weak', 'Strong']),
            (3.5 <= fed_rate <= 4.5),  # Clear middle range
            (102 <= dxy_level <= 103),  # Clear middle range
        ]
        
        if any(medium_conditions):
            return 'Medium'
        
        # Low confidence for mixed signals
        return 'Low'
    
    def get_signal_explanation(self, signal_data: Dict) -> str:
        """
        Generate human-readable explanation of the signal.
        """
        signal = signal_data['signal']
        fed_bias = signal_data['components']['fed_bias']
        dxy_bias = signal_data['components']['dxy_bias']
        fed_rate = signal_data['components']['fed_rate']
        dxy_level = signal_data['components']['dxy_level']
        
        explanation = f"Fed policy at {fed_rate:.1f}% is {fed_bias.lower()}, "
        explanation += f"while DXY at {dxy_level:.1f} is {dxy_bias.lower()} for gold. "
        
        if signal == 'LONG':
            explanation += "This combination favors higher gold prices."
        elif signal == 'SHORT':
            explanation += "This combination suggests lower gold prices ahead."
        else:
            explanation += "Mixed signals suggest waiting for clearer direction."
        
        return explanation