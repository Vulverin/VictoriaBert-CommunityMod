# Economy balance: first pass

Factory purchases now have a 10% floor and a 0.025 daily adjustment factor
instead of a 100% floor and no adjustment. This lets purchases respond to
unsold output. These are initial tuning values, not a measured optimum.

Four factory recipes had negative margins at base goods prices when template
efficiency goods were included. Input reductions preserve their output volumes
and avoid directly increasing global supply:

| Factory | Input change | Previous remainder | New remainder |
| --- | --- | ---: | ---: |
| Synthetic sulphur | shares: 35 to 2.5 | -124.625 | 5.375 |
| Dye | shares: 13 to 2 | -39.58 | 4.42 |
| Telephones | electric_gear: 5 to 3.5 | -5 | 19 |
| Wine | grain: 20 to 14 | -1.375 | 11.825 |

These estimates assume full sales, base prices and one recipe with its template
efficiency basket. They exclude wages, employment scaling, tariffs, technology,
local bonuses and actual engine accounting. They are not predicted daily profits.
Input reductions give these four recipes an initial remainder of roughly 16-26%
of sales under these assumptions. Other narrow positive margins remain candidates
for gameplay review. Artisan recipes, wages, sphere shares and tariffs are unchanged.

## Clerk experiment

The five ordinary factory templates now allocate 80% of jobs to craftsmen
(`throughput`) and 20% to clerks (`output`, multiplier 1.0), replacing the
50/50 split with clerk throughput multiplier 1.7. This makes clerks improve
output per unit of production input. The bank template retains 100% clerks
with throughput. Workforce sizes and capitalist bonuses are unchanged.

Existing saves may have surplus clerks during the transition. Compare employment,
input consumption, output and the clerk output bonus shown in the factory tooltip.
The recipe audit does not model this change; in-game validation is still required.

Run `python tools/economy_audit.py` to recalculate all 47 factory recipes.

## Gameplay comparison still required

Restart the game to load the changed files. Compare separate copies of the same
save with the original and changed configurations. Keep policies, budget sliders,
subsidies and manual factory expansions the same. Record initial conditions and
results after one, three and six months:

- Total subsidies and industrial employment.
- Input availability, goods produced and sold, and factory cash reserves.
- Prices and availability of shares, sulphur, dye, electric gear, grain and wine.
- Worker needs and capitalist income.

Lower subsidies alone are insufficient: check whether employment and sales have
collapsed. If that happens, reassess purchase adjustment speed and demand. Persistent
losses with full sales require inspection of wages, import costs and active modifiers.
Tariff and sphere behavior needs a separate controlled comparison.

Validation performed: all 47 base-price recipe remainders are positive; recipe
files parse in the audit tool; `git diff --check` passes. No in-game run performed.
