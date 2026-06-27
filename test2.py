import MetaTrader5 as mt5

mt5.initialize()

info = mt5.symbol_info("XAUUSD.pc")

print(info.point)
print(info.trade_contract_size)
print(info.spread)
print(info.trade_contract_size)
print(info.trade_tick_size)
print(info.trade_tick_value)
print(info.volume_min)
print(info.volume_step)
print(info.volume_max)