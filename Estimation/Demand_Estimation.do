cd "C:\Users\behri\OneDrive\Desktop\Master LSE\Essay\Ideas\Pepsi Coke"
set more off
capture log close 
set logtype text 
log using estimation.txt, replace

*Load data
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

estimates store nested_logit_distance 
encode nest_x, gen (nest)

* MODEL 1: MULTINOMIAL LOGIT MODEL 
ivregress 2sls lhs brand__* diet_indicator no_caffeine_indicator flavour_* package_* season_* ///
    age60 ethnic educ nocar income hsizeavg liquid_ml ///
    (price_x = avg_total_liq rival_liquid_avg rival_total_count other_nest_count other_nest_avg total_expenditure), robust
estimates store multinomial_logit_iv

* MODEL 2: STANDARD 1 LEVEL NESTED LOGIT WITHOUT DISTANCES 
ivregress 2sls lhs brand__* diet_indicator no_caffeine_indicator flavour_* package_* season_*  ///
    age60 ethnic educ nocar income hsizeavg liquid_ml ///
    (price_x ln_s_j_g = avg_total_liq rival_liquid_avg rival_total_count ///
    other_nest_count other_nest_avg total_expenditure)

*Store results 
estimates store nested_logit_standard

* MODEL 3: STANDARD 1 LEVEL NESTED LOGIT WITH DISTANCES 
ivregress 2sls lhs brand__* diet_indicator no_caffeine_indicator flavour_* package_* season_*  ///
    age60 ethnic educ nocar income hsizeavg d_j liquid_ml ///
    (price_x ln_s_j_g = avg_total_liq rival_liquid_avg rival_total_count ///
    other_nest_count other_nest_avg total_expenditure)

*Store results 
estimates store nested_logit_distance 

*Encode the company variable first 
encode company, gen (firm_id) 
tab company firm_id 
estimates restore nested_logit_standard

*Run the merger simulation 
mergersim init, market(hyp_market_x) firm(firm_id) price(price_x) /// 
nest(nest) quantity(move) alpha(-1.018006) sigmas(0.3061349)

*Perform the merger simulation 
mergersim market if inrange(week, 147, 200) & store == 48

*Hypothetical merger between Coke and Dr. Pepper 
mergersim simulate if week == 200, seller(7) buyer(4) detail 

*Hypothetical merger between 7UP and Pepsi 
mergersim simulate if week == 200, seller (1) buyer(10) detail 

end log 