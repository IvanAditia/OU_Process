import MetaTrader5 as mt5

mt5.initialize()

info = mt5.symbol_info("XAUUSD")

print("Contract Size :", info.trade_contract_size)
print("Tick Size     :", info.trade_tick_size)
print("Tick Value    :", info.trade_tick_value)

mt5.shutdown()