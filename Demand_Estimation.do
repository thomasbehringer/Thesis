** Do File for demand estimation 
cd "C:\Users\behri\OneDrive\Desktop\Master LSE\Essay\Ideas\Pepsi Coke"
set more off
capture log close 
set logtype text 
log using estimation.txt, replace

** Load data
insheet using "data_estimation.csv", clear

* Generate "market_id" to initialise dataset 
egen market_id = group(week store)
xtset upc market_id

* Calculate shares within nests (s_j_g) - was missing before
bysort store week nest_x: egen total_nest_share = sum(adjusted_market_share)
gen s_j_g = adjusted_market_share / total_nest_share
gen ln_s_j_g = ln(s_j_g)

* FIRST-STAGE REGRESSIONS OF PRICES ON THE ENDOGENOUS VARIABLES TO ELIMINATE THE WORRY OF 
* WEAK INSTRUMENTS 

* First-stage regression on prices 
reg price_x avg_total_liq rival_liquid_avg rival_total_count other_nest_count other_nest_avg total_expenditure

* First-stage regression on within-nest market share 
reg ln_s_j_g avg_total_liq rival_liquid_avg rival_total_count other_nest_count other_nest_avg total_expenditure

* MODEL 1: MARIUZZO MODEL
ivregress 2sls lhs brand__* diet_indicator no_caffeine_indicator flavour_* package_* holiday_indicator ///
	age60 age9 ethnic educ nocar income hsizeavg liquid_ml dummy_*  ///
    (price_x ln_s_j_g distance_p d_j = avg_total_liq rival_liquid_avg ///
    rival_total_count other_nest_count other_nest_avg total_expenditure)

* Store results 
estimates store nested_logit_distance 


* MODEL 2: STANDARD 1 LEVEL NESTED LOGIT WITHOUT DISTANCES 
ivregress 2sls lhs brand__* diet_indicator no_caffeine_indicator flavour_* package_* season_*  ///
    age60 ethnic educ nocar income hsizeavg liquid_ml ///
    (price_x ln_s_j_g = avg_total_liq rival_liquid_avg rival_total_count ///
    other_nest_count other_nest_avg total_expenditure)

* Store results
estimates store nested_logit_standard


** MERGER SIMULATION FOR STANDARD MODEL ** 

* NEED TO ADD MARKET SIZE * 

* Encode the company variable first* 
encode company, gen (firm_id)
encode nest_x, gen (nest)
tab company firm_id

estimates restore nested_logit_standard


* Extract nesting parameter from estimation
local gamma = _b[ln_s_j_g]
local sigma = 1- `gamma'

* Initialise merger simulation
mergersim init, market(market_id) firm(firm_id) price(price_x) ///
	nest(nest) sigma(`sigma') quantity(move)

** MERGER SIMULATION FOR MARIUZZO MODEL ** 
estimates restore nested_logit_distance

* We need to extract the coefficients in order to calculate the elasticities given by the formula in the paper 

matrix b = e(b)

matrix list b

* Extract the key parameters 
local price_pos = 1 
local sigma_pos = 2
local dist_price_pos = 3
local dist_pos = 4

* Extract coefficient values 
local alpha = -b[1, `price_pos']
local sigma = b[1, `sigma_pos']
local alpha_dist = b[1, `dist_price_pos']
local beta_dist = b[1, `dist_pos']

* Alpha_j calculation
gen alpha_j = `alpha' + `alpha_dist' * d_j

* Calculate own_price elasticities
gen e_jj = alpha_j * price_x * (adjusted_market_share - 1/(1-`sigma') + (`sigma' / (1-`sigma')) * s_j_g)