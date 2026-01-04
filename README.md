# Omnitrade Governance & Trading OS

Omnitrade is a high-performance, governed algorithmic trading command center designed for institutional-grade market analysis and execution. It combines a sophisticated React-based frontend with a robust Python/FastAPI backend, integrated via real-time WebSockets.

![Omnitrade Dashboard](https://raw.githubusercontent.com/opendev-labs/omnitrade/main/dashboard_preview.png)

## 🏛 architecture

The system follows a strict **Governance-First** philosophy. Every execution module (Bot) is governed by a central Health Score engine that adjusts system exposure based on real-time market risk.

- **Frontend**: Vite + React + Tailwind CSS (Deep Obsidian & Neon design system).
- **Backend**: Python 3.10+ + FastAPI (Asynchronous state engine).
- **Communication**: Full-duplex WebSockets for <5ms data synchronization.

## 🕵️‍♂️ Scanners (The Eyes)

1.  **Market State**: ATR-based volatility, EMA-based trend identification, and Phase (Accumulation/Expansion/Distribution/Reset).
2.  **Clock Cycle**: Automated session tracking (Asia, London, NY) and cycle phase (Early/Mid/Late).
3.  **Token Rotation**: Relative strength ranking against BTC for dynamic asset selection.
4.  **Correlation**: Multi-asset correlation matrix to detect concentration risk.
5.  **Uncertainty**: Advanced signal disagreement and loss clustering detection.

## 🤖 Fleet Management (The Muscle)

The system manages 10 specialized execution modules:
- VWAP Mean Reversion
- Volatility Expansion (BB Squeeze)
- Trend Pullback
- Range Scalper
- Liquidity Sweep
- Session Open Alpha
- Funding Arbitrage
- Cross-Asset Divergence
- Momentum Micro
- **NO-TRADE GUARDIAN**: The ultimate system circuit breaker.

## 🛡 Governance (The brain)

The Health Score formula ensures capital preservation:
`Health = 100 - (Drawdown % + Loss Cluster Penalty + Correlation Stress + Uncertainty Penalty)`

- **Health > 80**: Full Execution Enabled.
- **60-80**: Reduced Size / Defensive Mode.
- **40-60**: Aggressive Risk Mitigation.
- **< 40**: System-wide Lockdown (Guardian Active).

## 🚀 Quick Start

### Backend Setup
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py
```

### Frontend Setup
```bash
npm install
npm run dev
```

---

Developed by **OpenDev Labs**.
