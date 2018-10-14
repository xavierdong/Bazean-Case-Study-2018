Question 1:
-ND_WELL_DATA is read as pandas dataframe
-Dataframe grouped by operator and separated
-cum_oil column is summed for each operator to calculate aggregate oil production
-Data visulaized in SpotFire using bar charts

Question 2: 
-ND_PRODUCTION_DATA is read as pandas dataframe
-Dataframe grouped by api number and separated
-Separated Dataframe sorted by index to achieve chronological order
-Outliers (wellbore storage, shut in) production data point is removed
-Hyperbolic decline curve fitted to data point and hyperbolic curve parameters (qi, b, Di) are calculated
***Hyperbolic curve is not fitted to wells with less than 5 production data points (NaN value stored as EUR)***
-Determined EUR by integrating determined hyperbolic curve for each well (each assuming 200 month of productions to reach economic limit)
-Total estimated reserve (sum of EUR of all of operator's well) is determined
-Data visualized in SpotFire using pie charts

Question 3:
-first year annual hydrocarbon production (cum_12_oil, cum_12_gas) is plotted against spud_date to capture development of productivity vs. time
-6th degree polynomial fitted to scattered data in SpotFire to compare first year annual productivity of each well vs time the well was drilled
-Identified best increasing trend in first year productivity over time that well was drilled
-WPX ENERGY WILLISTON LLC has the overall best improving trend in first year production as more wells are drilled: wells drilled going forward will should have best productivity
