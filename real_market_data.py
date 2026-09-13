import yfinance as yf

symbol = input("Enter stock name/symbol: ").upper().strip()

if not symbol.endswith(".NS"):
    symbol += ".NS"

stock = yf.Ticker(symbol)


symbol2 = input("Enter second stock name/symbol: ").upper().strip()

if not symbol2.endswith(".NS"):
    symbol2 += ".NS"

stock2 = yf.Ticker(symbol2)

data = stock.history(period="1mo")
data2 = stock2.history(period="1mo")

if data.empty:
    print("No data found for", symbol)
    exit()

if data2.empty:
    print("No data found for", symbol2)
    exit()

print("\nSECOND STOCK DATA")
print(data2[["Close", "Volume"]].head())

print(data.columns)
print(data[["Close", "Volume"]])

first_price = data["Close"].iloc[0]
last_price = data["Close"].iloc[-1]

return_percent = (last_price - first_price) / first_price * 100

print("First price:", first_price)
print("Last price:", last_price)
print("Return:", return_percent, "%")

data["Return"] = data["Close"].pct_change() * 100

print(data[["Close", "Return"]])

best = data.loc[data["Return"].idxmax()]
worst = data.loc[data["Return"].idxmin()]

print("BEST DAY")
print(best)

print("\nWORST DAY")
print(worst)

average_return = data["Return"].mean()

print("Average daily return:", average_return, "%")

volatility = data["Return"].std()

print("Daily volatility:", volatility, "%")

investment = float(input("Enter investment amount for each stock: ₹"))

final_value = investment * (last_price / first_price)

profit = final_value - investment

print("Initial investment:", investment)
print("Final value:", final_value)
print("Profit/Loss:", profit)

#first stock investment growth


shares = int(investment / first_price)
cash_left = investment - (shares * first_price)

data["Investment Value"] = shares * data["Close"] + cash_left

print("\nINVESTMENT GROWTH")
print(data[["Close", "Investment Value"]])

data["Peak"] = data["Investment Value"].cummax()

data["Drawdown"] = (
    (data["Investment Value"] - data["Peak"])
    / data["Peak"]
) * 100

max_drawdown = data["Drawdown"].min()

print("\nMAXIMUM DRAWDOWN:", max_drawdown, "%")



# SECOND STOCK INVESTMENT GROWTH

second_first_price = data2["Close"].iloc[0]
second_last_price = data2["Close"].iloc[-1]

shares2 = int(investment / second_first_price)
cash_left2 = investment - (shares2 * second_first_price)

data2["Investment Value"] = (
    shares2 * data2["Close"] + cash_left2
)

second_final_value = data2["Investment Value"].iloc[-1]
second_profit = second_final_value - investment

print("\nSECOND STOCK INVESTMENT GROWTH")
print(data2[["Close", "Investment Value"]])

print("Initial investment:", investment)
print("Final value:", second_final_value)
print("Profit/Loss:", second_profit)

data2["Peak"] = data2["Investment Value"].cummax()

data2["Drawdown"] = (
    (data2["Investment Value"] - data2["Peak"])
    / data2["Peak"]
) * 100

second_max_drawdown = data2["Drawdown"].min()

print("\nSECOND STOCK MAXIMUM DRAWDOWN:", second_max_drawdown, "%")


# TWO STOCK COMPARISON

second_return_percent = (
    (second_last_price - second_first_price)
    / second_first_price
) * 100

data2["Daily Return"] = data2["Close"].pct_change() * 100

second_average_return = data2["Daily Return"].mean()
second_volatility = data2["Daily Return"].std()

print("\nTWO STOCK COMPARISON")

print(symbol.replace(".NS", ""), "Return:", return_percent, "%")
print(symbol2.replace(".NS", ""), "Return:", second_return_percent, "%")

print(symbol.replace(".NS", ""), "Final Investment Value: ₹", final_value)
print(symbol2.replace(".NS", ""), "Final Investment Value: ₹", second_final_value)

print(symbol.replace(".NS", ""), "Volatility:", volatility, "%")
print(symbol2.replace(".NS", ""), "Volatility:", second_volatility, "%")

if return_percent > second_return_percent:
    print("BETTER PERFORMER:", symbol.replace(".NS", ""))
else:
    print("BETTER PERFORMER:", symbol2.replace(".NS", ""))

if volatility < second_volatility:
    print("LOWER RISK:", symbol.replace(".NS", ""))
else:
    print("LOWER RISK:", symbol2.replace(".NS", ""))

import matplotlib.pyplot as plt

#first stock graph

plt.figure()

plt.plot(data.index, data["Close"])

plt.title(f"{symbol.replace('.NS', '')} Closing Price")
plt.xlabel("Date")
plt.ylabel("Price")

plt.xticks(rotation=45)
plt.tight_layout()

plt.show(block=False)

#second stock graph

plt.figure()

plt.plot(data2.index, data2["Close"])

plt.title(f"{symbol2.replace('.NS', '')} Closing Price")
plt.xlabel("Date")
plt.ylabel("Price")

plt.xticks(rotation=45)
plt.tight_layout()

plt.show(block=False)

# INVESTMENT GROWTH GRAPH

plt.figure()

plt.plot(
    data.index,
    data["Investment Value"],
    label=symbol.replace(".NS", "")
)

plt.plot(
    data2.index,
    data2["Investment Value"],
    label=symbol2.replace(".NS", "")
)

plt.title("Investment Growth Comparison")
plt.xlabel("Date")
plt.ylabel("Investment Value (₹)")

plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()

plt.show(block=False)

# FUNDAMENTAL DATA


financials = stock.financials

print("\nFINANCIAL DATA")
print(financials)

def get_metric(financials, name):
    if name in financials.index:
        return financials.loc[name].iloc[0]
    return None

# FUNDAMENTAL ANALYSIS

print("\nKEY FUNDAMENTAL METRICS")

revenue = get_metric(financials, "Operating Revenue")
operating_income = get_metric(financials, "Operating Income")
net_income = get_metric(financials, "Net Income")
ebitda = get_metric(financials, "EBITDA")
ebit = get_metric(financials, "EBIT")
eps = get_metric(financials, "Diluted EPS")
interest_expense = get_metric(financials, "Interest Expense Non Operating")
print("Revenue:", revenue)
print("Operating Income:", operating_income)
print("Net Income:", net_income)
print("EBITDA:", ebitda)
print("EBIT:", ebit)
print("Diluted EPS:", eps)
print("Interest Expense:", interest_expense)

# SECOND STOCK FUNDAMENTALS

financials2 = stock2.financials

revenue2 = get_metric(financials2, "Operating Revenue")
operating_income2 = get_metric(financials2, "Operating Income")
net_income2 = get_metric(financials2, "Net Income")
ebitda2 = get_metric(financials2, "EBITDA")
eps2 = get_metric(financials2, "Diluted EPS")

operating_margin2 = (operating_income2 / revenue2) * 100 if operating_income2 is not None else None
net_profit_margin2 = (net_income2 / revenue2) * 100 if net_income2 is not None else None

print("\nSECOND STOCK FUNDAMENTALS")

print("Revenue:", revenue2)
print("Operating Income:", operating_income2)
print("Net Income:", net_income2)
print("EBITDA:", ebitda2)
print("Diluted EPS:", eps2)


# PROFITABILITY RATIOS

operating_margin = (
    (operating_income / revenue) * 100
    if operating_income is not None and revenue is not None
    else None
)

net_profit_margin = (
    (net_income / revenue) * 100
    if net_income is not None and revenue is not None
    else None
)

operating_margin2 = (
    (operating_income2 / revenue2) * 100
    if operating_income2 is not None and revenue2 is not None
    else None
)

net_profit_margin2 = (
    (net_income2 / revenue2) * 100
    if net_income2 is not None and revenue2 is not None
    else None
)


# FUNDAMENTAL COMPARISON

print("\nFUNDAMENTAL COMPARISON")

print(
    symbol.replace(".NS", ""),
    "Operating Margin:",
    operating_margin if operating_margin is not None else "Not Available",
    "%"
)

print(
    symbol2.replace(".NS", ""),
    "Operating Margin:",
    operating_margin2 if operating_margin2 is not None else "Not Available",
    "%"
)

print(
    symbol.replace(".NS", ""),
    "Net Profit Margin:",
    net_profit_margin if net_profit_margin is not None else "Not Available",
    "%"
)

print(
    symbol2.replace(".NS", ""),
    "Net Profit Margin:",
    net_profit_margin2 if net_profit_margin2 is not None else "Not Available",
    "%"
)


if operating_margin is not None and operating_margin2 is not None:
    if operating_margin > operating_margin2:
        print("Better Operating Margin:", symbol.replace(".NS", ""))
    else:
        print("Better Operating Margin:", symbol2.replace(".NS", ""))
else:
    print("Operating Margin comparison: Not Available")


if net_profit_margin is not None and net_profit_margin2 is not None:
    if net_profit_margin > net_profit_margin2:
        print("Better Net Profit Margin:", symbol.replace(".NS", ""))
    else:
        print("Better Net Profit Margin:", symbol2.replace(".NS", ""))
else:
    print("Net Profit Margin comparison: Not Available")

    
# SECOND STOCK FUNDAMENTAL HEALTH CHECK

print("\nSECOND STOCK FUNDAMENTAL HEALTH CHECK")

if revenue2 is not None and revenue2 > 0:
    print("Revenue: POSITIVE")

if operating_income2 is not None and operating_income2 > 0:
    print("Operating Income: POSITIVE")

if net_income2 is not None and net_income2 > 0:
    print("Net Income: POSITIVE")

if ebitda2 is not None and ebitda2 > 0:
    print("EBITDA: POSITIVE")

if eps2 is not None and eps2 > 0:
    print("EPS: POSITIVE")

if operating_margin2 is not None:
    if operating_margin2 > 10:
        print("Operating Margin: GOOD")
    else:
        print("Operating Margin: LOW")
else:
    print("Operating Margin: NOT AVAILABLE")
    

# RISK ANALYSIS

data["Daily Return"] = data["Close"].pct_change() * 100

volatility = data["Daily Return"].std()

print("\nRISK ANALYSIS")

print("Average Daily Return:", data["Daily Return"].mean(), "%")
print("Daily Volatility:", volatility, "%")

# SECOND STOCK RISK ANALYSIS

data2["Daily Return"] = data2["Close"].pct_change() * 100

second_average_return = data2["Daily Return"].mean()
second_volatility = data2["Daily Return"].std()

print("\nSECOND STOCK RISK ANALYSIS")

print("Average Daily Return:", second_average_return, "%")
print("Daily Volatility:", second_volatility, "%")

# INVESTMENT SUMMARY

initial_investment = investment
final_value = data["Investment Value"].iloc[-1]

total_return = ((final_value - initial_investment) / initial_investment) * 100

print("\nINVESTMENT SUMMARY")

print("Initial Investment: ₹", initial_investment)
print("Final Investment Value: ₹", final_value)
print("Total Return:", total_return, "%")
print("Maximum Drawdown:", max_drawdown, "%")
print("Average Daily Return:", data["Daily Return"].mean(), "%")
print("Daily Volatility:", volatility, "%")


# OVERALL STOCK COMPARISON
# RETURNS
first_return = ((data["Close"].iloc[-1] - data["Close"].iloc[0])
                / data["Close"].iloc[0]) * 100

second_return = ((data2["Close"].iloc[-1] - data2["Close"].iloc[0])
                 / data2["Close"].iloc[0]) * 100

# VOLATILITY
first_volatility = data["Close"].pct_change().std() * 100
second_volatility = data2["Close"].pct_change().std() * 100

print("\n" + "=" * 65)
print("                    OVERALL STOCK COMPARISON")
print("=" * 65)

stock1_name = symbol.replace(".NS", "")
stock2_name = symbol2.replace(".NS", "")

print(f"{'METRIC':<25}{stock1_name:<20}{stock2_name:<20}")
print("-" * 65)

print(f"{'Return':<25}{first_return:<20.2f}{second_return:<20.2f}")
print(f"{'Volatility':<25}{first_volatility:<20.2f}{second_volatility:<20.2f}")

print("-" * 65)

# RETURN COMPARISON

if first_return > second_return:
    better_return = stock1_name
else:
    better_return = stock2_name

print(f"{'Better Return':<25}{better_return}")

# RISK COMPARISON

if first_volatility < second_volatility:
    lower_risk = stock1_name
else:
    lower_risk = stock2_name

print(f"{'Lower Risk':<25}{lower_risk}")

# FINAL VERDICT

print("\n" + "=" * 65)
print("                    FINAL VERDICT")
print("=" * 65)

if first_return > second_return and first_volatility < second_volatility:
    winner = stock1_name

elif second_return > first_return and second_volatility < first_volatility:
    winner = stock2_name

else:
    winner = None

if winner is not None:
    print("FINAL WINNER:", winner)

    print("\nREASONS:")

    if winner == stock1_name:
        print("• Higher return")
        print("• Lower risk")
    else:
        print("• Higher return")
        print("• Lower risk")

else:
    print("NO CLEAR WINNER")

print("=" * 65)


# FUNDAMENTAL SCORE

score1 = 0
score2 = 0

if operating_margin is not None and operating_margin2 is not None:
    if operating_margin > operating_margin2:
        score1 += 1
    else:
        score2 += 1

if net_profit_margin is not None and net_profit_margin2 is not None:
    if net_profit_margin > net_profit_margin2:
        score1 += 1
    else:
        score2 += 1

print("\nFUNDAMENTAL SCORE")

print(symbol.replace(".NS", ""), "Score:", score1, "/ 3")
print(symbol2.replace(".NS", ""), "Score:", score2, "/ 3")

if score1 > score2:
    print("BETTER FUNDAMENTALS:", symbol.replace(".NS", ""))
elif score2 > score1:
    print("BETTER FUNDAMENTALS:", symbol2.replace(".NS", ""))
else:
    print("FUNDAMENTALS: TIE")

# WEIGHTED OVERALL SCORE

# Return score
if first_return > second_return:
    return_score1 = 1
    return_score2 = 0
else:
    return_score1 = 0
    return_score2 = 1

# Risk score
if first_volatility < second_volatility:
    risk_score1 = 1
    risk_score2 = 0
else:
    risk_score1 = 0
    risk_score2 = 1

# Calculate overall scores
overall_score1 = (
    return_score1 * 40
    + risk_score1 * 20
    + score1 * (40 / 3)
)

overall_score2 = (
    return_score2 * 40
    + risk_score2 * 20
    + score2 * (40 / 3)
)

print("\nWEIGHTED OVERALL SCORE")

print(symbol.replace(".NS", ""), "Overall Score:", round(overall_score1, 2), "/ 100")
print(symbol2.replace(".NS", ""), "Overall Score:", round(overall_score2, 2), "/ 100")

if overall_score1 > overall_score2:
    final_winner = stock1_name
    final_score = overall_score1
    winner_score = score1
    loser_score = score2
else:
    final_winner = stock2_name
    final_score = overall_score2
    winner_score = score2
    loser_score = score1

print("FINAL WINNER:", final_winner)
print("OVERALL SCORE:", round(final_score, 2), "/ 100")

print("\nWHY", final_winner + "?")

if final_winner == stock1_name:
    if first_return > second_return:
        print("• Better return")
    if first_volatility < second_volatility:
        print("• Lower risk")
    if score1 > score2:
        print("• Better fundamentals")
else:
    if second_return > first_return:
        print("• Better return")
    if second_volatility < first_volatility:
        print("• Lower risk")
    if score2 > score1:
        print("• Better fundamentals")

print("=" * 65)

# PORTFOLIO SUMMARY

investment_per_stock = investment

first_final_value = data["Investment Value"].iloc[-1]
second_final_value = data2["Investment Value"].iloc[-1]

total_investment = investment_per_stock * 2
total_portfolio_value = first_final_value + second_final_value
portfolio_profit = total_portfolio_value - total_investment

portfolio_return = (
    (total_portfolio_value - total_investment)
    / total_investment
) * 100

print("\nPORTFOLIO SUMMARY")

print("Total Investment: ₹", total_investment)

print(
    symbol.replace(".NS", ""),
    "Investment: ₹", investment_per_stock
)

print(
    symbol.replace(".NS", ""),
    "Final Value: ₹", first_final_value
)

print(
    symbol2.replace(".NS", ""),
    "Investment: ₹", investment_per_stock
)

print(
    symbol2.replace(".NS", ""),
    "Final Value: ₹", second_final_value
)

print("Total Portfolio Value: ₹", total_portfolio_value)
print("Total Profit/Loss: ₹", portfolio_profit)
print("Portfolio Return:", portfolio_return, "%")
