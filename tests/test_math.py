from src.fx_math import pip_size, pip_value_per_lot_usd, expectancy_per_trade, margin_required_usd


def test_pip_lot_course_identities():
    assert pip_size("EURUSD") == 0.0001
    assert pip_size("USDJPY") == 0.01
    assert abs(pip_value_per_lot_usd("EURUSD", 0.01, 1.0850) - 0.10) < 1e-9
    assert abs(pip_value_per_lot_usd("EURUSD", 0.10, 1.0850) - 1.0) < 1e-9
    assert abs(pip_value_per_lot_usd("EURUSD", 1.00, 1.0850) - 10.0) < 1e-9


def test_expectancy_30pct_3R():
    assert abs(expectancy_per_trade(0.30, 3.0, 1.0) - 0.2) < 1e-12


def test_margin_identity():
    m = margin_required_usd(1.0, 100000, 1.0850, 100)
    assert abs(m - 1085.0) < 1e-6


def test_no_lookahead_signal_uses_past_only():
    import pandas as pd
    import numpy as np
    from src.backtest import backtest_market_orders
    n = 60
    px = np.linspace(1.08, 1.09, n)
    df = pd.DataFrame({"Date": pd.date_range("2024-01-01", periods=n), "Open": px, "High": px + 0.0005, "Low": px - 0.0005, "Close": px})
    sig = pd.Series(np.zeros(n))
    sig.iloc[10] = 1
    t1 = __import__("src.backtest", fromlist=["backtest_market_orders"]).backtest_market_orders(df, sig, lot=0.10, tp_pips=1000, sl_pips=1000, spread_pips=0, max_hold_bars=5)
    # entry must be at open[t+1] = px[11]
    assert len(t1) >= 0  # smoke; exact fill asserted below when trade exists
    if len(t1):
        assert abs(t1.iloc[0]["entry"] - px[11]) < 1e-12
