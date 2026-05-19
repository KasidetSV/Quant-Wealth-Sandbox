import numpy as np
import pandas as pd
from typing import Dict

class ERAA_Simulator:
    """
    Economic Regime-Based Asset Allocation (ERAA) Simulator.
    A simplified mockup demonstrating quantitative risk modeling and 
    regime-based portfolio shifts for ETFs.
    """
    
    def __init__(self, target_sri: float):
        # SRI (StashAway Risk Index): Value-at-Risk (99% confidence over 1 year)
        # An SRI of 15% means there's a 99% probability the portfolio won't lose > 15%.
        self.sri = target_sri
        
        # Define economic regimes
        self.regimes = ['Growth', 'Recession', 'Stagflation', 'Recovery']
        
        # Asset classes available
        self.asset_classes = ['Equity_US', 'Equity_Emerging', 'Gov_Bonds', 'Gold']
        
        # Baseline Risk/Return Profiles for Asset Classes (Volatility)
        self.asset_volatility = {
            'Equity_US': 0.16,
            'Equity_Emerging': 0.22,
            'Gov_Bonds': 0.05,
            'Gold': 0.14
        }
    
    def get_regime_weights(self, regime: str) -> Dict[str, float]:
        """
        Adjust asset weights dynamically based on the macroeconomic regime.
        """
        if regime == 'Growth':
            base = {'Equity_US': 0.50, 'Equity_Emerging': 0.30, 'Gov_Bonds': 0.10, 'Gold': 0.10}
        elif regime == 'Recession':
            base = {'Equity_US': 0.20, 'Equity_Emerging': 0.05, 'Gov_Bonds': 0.55, 'Gold': 0.20}
        elif regime == 'Stagflation':
            base = {'Equity_US': 0.15, 'Equity_Emerging': 0.10, 'Gov_Bonds': 0.40, 'Gold': 0.35}
        elif regime == 'Recovery':
            base = {'Equity_US': 0.40, 'Equity_Emerging': 0.40, 'Gov_Bonds': 0.15, 'Gold': 0.05}
        else:
            raise ValueError("Unknown Regime")
            
        return base
        
    def calculate_portfolio_var(self, weights: Dict[str, float]) -> float:
        """
        Calculate simplified 99% VaR (Value at Risk) based on asset volatility.
        Assuming normal distribution (z-score for 99% is approx 2.33).
        """
        z_score = 2.33
        
        # Simplified portfolio variance (assuming 0 correlation for the sake of the mockup)
        port_variance = sum((weights[asset] * self.asset_volatility[asset])**2 for asset in self.asset_classes)
        port_volatility = np.sqrt(port_variance)
        
        # VaR = z_score * portfolio volatility
        var_99 = z_score * port_volatility
        return round(var_99, 4)

    def optimize_for_sri(self, regime: str) -> Dict[str, float]:
        """
        Adjusts weights to ensure the portfolio's VaR does not exceed the Target SRI.
        In reality, this uses advanced mean-variance optimization and Black-Litterman models.
        """
        weights = self.get_regime_weights(regime)
        current_var = self.calculate_portfolio_var(weights)
        
        print(f"--- Optimizing for {regime} Regime ---")
        print(f"Target SRI: {self.sri * 100}% | Initial Regime VaR: {current_var * 100:.2f}%")
        
        if current_var > self.sri:
            print(">> Risk Exceeds Target SRI. Shifting to protective assets (Bonds/Gold).")
            # Shift 10% from highest risk (Emerging) to Bonds iteratively
            while current_var > self.sri and weights['Equity_Emerging'] > 0:
                shift = min(0.05, weights['Equity_Emerging'])
                weights['Equity_Emerging'] -= shift
                weights['Gov_Bonds'] += shift
                current_var = self.calculate_portfolio_var(weights)
                
        print(f"Optimized SRI (VaR): {current_var * 100:.2f}%")
        return {k: round(v, 3) for k, v in weights.items()}


if __name__ == "__main__":
    print("[SYSTEM] Initializing Quant Wealth Sandbox: ERAA Simulator\n")
    
    # Initialize for a balanced risk profile (12% Target SRI)
    simulator = ERAA_Simulator(target_sri=0.12)
    
    # Test during a Growth phase
    growth_portfolio = simulator.optimize_for_sri('Growth')
    print(f"Final Allocation (Growth): {growth_portfolio}\n")
    
    # Test during an economic shock (Stagflation)
    stagflation_portfolio = simulator.optimize_for_sri('Stagflation')
    print(f"Final Allocation (Stagflation): {stagflation_portfolio}\n")
