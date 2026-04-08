BTC3.py is current stable version


BTC-Beta.py is buggy as hell - but starts to bring in daily, 12h and 4h measurments. 
Mechanism in place to split data requests to Binance to accomodate 1000 results limitation to allow amount of days*intervals to exceed 1000 (365days*4hs=2190 results split over 3 calls to Binance)



Upcoming enhancements - 
*Sanitise code used to split calls to Binance

*Ensure data is commited to DB to prevent overuse of API and date - A years worth of 4h data intervals should negate need for 12 hour report to pull down further data - only want deltas

*Need to change backtesting capital workflow to occur only when backtesting is called - reduce menu noise and better workflow

*Abilty to save a preferences and load at time of accessing function to track user preference - may extend this record transactions - can save to user DB to preserve if crypto_data.db cache needs resetting - use export and import options or other means of secured backup and recovery.

*Use of API to manage trades - only after significant backtesting 

*Yearly results appear to be 30x12 days which is causing gap - should be 365 days per year

