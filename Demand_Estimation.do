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
bysort store week nest_x: egen total_nest_share = sum(adju	sted_market_share)
gen s_j_g = adjusted_market_share / total_nest_share
gen ln_s_j_g = ln(s_j_g)

* FIRST-STAGE REGRESSIONS OF PRICES ON THE ENDOGENOUS VARIABLES TO ELIMINATE THE WORRY OF 
* WEAK INSTRUMENTS 

* First-stage regression on prices in multinomial_logit
reg price_x rival_liquid_avg rival_total_count total_expenditure

* First-stage regression on prices in nested logit 

reg price_x nest_count nest_avg rival_liquid_avg rival_total_count other_nest_count other_nest_avg total_expenditure

* First-stage regression on within-nest market share 

reg ln_s_j_g nest_count nest_avg rival_liquid_avg rival_total_count other_nest_count other_nest_avg total_expenditure

estimates store nested_logit_distance 
encode nest_x, gen (nest)

* MODEL 1: MULTINOMIAL LOGIT MODEL 
ivregress 2sls lhs diet_indicator no_caffeine_indicator liquid_ml brand__* flavour_* package_* season_* ///
    age60 ethnic educ nocar income hsizeavg ///
    (price_x = rival_liquid_avg rival_total_count total_expenditure), robust
	
estat overid

estimates store multinomial_logit_iv

* MODEL 2: STANDARD 1 LEVEL NESTED LOGIT WITHOUT DISTANCES 
ivregress 2sls lhs diet_indicator no_caffeine_indicator liquid_ml nest brand__* flavour_* package_* season_*  ///
    age60 ethnic educ nocar income hsizeavg ///
    (price_x ln_s_j_g = rival_liquid_avg rival_total_count other_nest_count other_nest_avg total_expenditure), robust

estat overid
	
*Store results 
estimates store nested_logit_standard

* MODEL 3: STANDARD 1 LEVEL NESTED LOGIT WITH DISTANCES 
ivregress 2sls lhs d_j diet_indicator no_caffeine_indicator liquid_ml nest brand__* flavour_* package_* season_*  ///
    age60 ethnic educ nocar income hsizeavg ///
    (price_x ln_s_j_g = nest_count nest_avg rival_liquid_avg rival_total_count other_nest_count other_nest_avg total_expenditure), robust

estat overid

* MODEL 4: STANDARD 1 LEVEL NESTED LOGIT WITH DISTANCES WITHOUT COST INSTRUMENT
ivregress 2sls lhs d_j diet_indicator no_caffeine_indicator liquid_ml nest brand__* flavour_* package_* season_*  ///
    age60 ethnic educ nocar income hsizeavg ///
    (price_x ln_s_j_g = nest_count nest_avg rival_liquid_avg rival_total_count other_nest_count other_nest_avg), robust

estat overid

*Store results 
estimates store nested_logit_distance 

*Encode the company variable first 
encode company, gen (firm_id) 
tab company firm_id 
estimates restore nested_logit_standard

*Run the merger simulation 
mergersim init, market(hyp_market_x) firm(firm_id) price(price_x) /// 
nest(nest) quantity(move) alpha(-1.023) sigmas(0.1798)

*Perform the merger simulation	 
mergersim market if inrange(week, 147, 200) & inrange(store, 1, 20)

*Hypothetical merger between Coke and Dr. Pepper 
mergersim simulate if inrange(week, 147, 200) & inrange(store, 1, 20), seller(7) buyer(4) detail 

*Hypothetical merger between 7UP and Pepsi 
mergersim simulate if inrange(week, 147, 200) & inrange(store, 1, 20), seller (1) buyer(10) detail 

end log 