total = 100

odds_one = 3.75
odds_two = 2.18
odds_draw = 3.65

arb = 1/odds_one + 1/odds_two + 1/odds_draw

print(str(arb))

if arb < 1:
    print("PROFIT")
else:
    print("NO PROFIT")

wage_one = total / (1 + ( odds_one / odds_two) + (odds_one / odds_draw))
wage_two = total / (1 + ( odds_two / odds_one) + (odds_two / odds_draw))
wage_draw = total / (1 + ( odds_draw / odds_one) + (odds_draw / odds_two))
final_total = wage_one + wage_two + wage_two

one_win = (wage_one * odds_one) - total
two_win = (wage_two * odds_two) - total
draw_win = (wage_draw * odds_draw) - total

print(str(wage_one))
print(str(wage_two))
print(str(wage_draw))
print(str(one_win))
print(str(two_win))
print(str(draw_win))