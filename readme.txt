Question 1:
-ND_WELL_DATA is read as pandas dataframe
-Dataframe grouped by operator and separated
-cum_oil column is summed for each operator to calculate aggregate oil production

-Data visulaized in SpotFire using bar charts:
case_visualization.dxp > q1

Question 2: 
-ND_PRODUCTION_DATA is read as pandas dataframe
-Dataframe grouped by api number and separated
-Separated Dataframe sorted by index to achieve chronological order
-Outliers (wellbore storage, shut in) production data point is removed
-Hyperbolic decline curve fitted to data point and hyperbolic curve parameters (qi, b, Di) are calculated
***Hyperbolic curve is not fitted to wells with less than 5 production data points (NaN value stored as EUR)***
-Determined EUR by integrating determined hyperbolic curve for each well (each assuming 200 month of productions to reach economic limit)
-Total estimated reserve (sum of EUR of all of operator's well) is determined

-Data visualized in SpotFire using pie charts: 
case_study_visualization.dxp > q2 for EUR per well per company
case_study_visualization.dxp > q2_1 for total estimated reserve per company

Question 3:
first method:
-first year annual hydrocarbon production (cum_12_oil, cum_12_gas) is plotted against spud_date to capture development of productivity vs. time
-polynomial curve fitted to scattered data in SpotFire to compare first year annual productivity of each well vs time the well was drilled
-Identified best increasing trend in first year productivity over time (by spud_date) wells were drilled by each operator
-WPX ENERGY WILLISTON LLC seem to have the best producivity improvement over time using this method
second method:
-sort production data by company then by date, average all production (for both oil and gas) for each given date
-plot data in spotfire by operator to identify productivity performance trend over time by fitting a polynomial curve to the scattered productivity data
-MARATHON OIL COMPANY seem to have the best producivity improvement over time using this method

-Data visualized in SpotFire using scatter plot and curve fits: 
case_study_visualization.dxp > q3 for 
case_study_visualization.dxp > q3_1 for total estimated reserve per company