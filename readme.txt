Question 1:
-ND_WELL_DATA is read as pandas dataframe (only relevant headers are read)
-Dataframe grouped by operator and separated
-cum_oil column is summed for each operator to calculate aggregate oil production

-Data visulaized in SpotFire using bar charts:
case_visualization.dxp > q1

Question 2: 
-ND_PRODUCTION_DATA is read as pandas dataframe (only relevant headers are read)
-Dataframe grouped by api number and separated
-Separated Dataframes are then sorted by index to achieve chronological order
-Outliers (wellbore storage, shut in) production data point is removed
-Hyperbolic decline curve fitted to data point and hyperbolic curve parameters (qi, b, Di) are calculated
***Hyperbolic curve is not fitted to wells with less than 5 production data points (NaN value stored as EUR)***
-Determined EUR by integrating determined hyperbolic curve for each well (each assuming 200 month of productions to reach economic limit)
-Total estimated reserve (sum of EUR for all of an operator's well) is determined for each operator

-Data visualized in SpotFire using pie charts: 
case_study_visualization.dxp > q2 for EUR per well per company
case_study_visualization.dxp > q2_1 for total estimated reserve per company

Question 3:
first method:
-first year annual hydrocarbon production (cum_12_oil, cum_12_gas) is plotted against spud_date to capture first year productivity of an operator's well vs. time
-polynomial curve fitted to scattered data in SpotFire to compare between operators and capture productivity development of wells drilled by an operator vs. time (spud_date), as more wells are drilled
-Identified best increasing trend in first year productivity over time wells were drilled by each operator
-WPX ENERGY WILLISTON LLC seems to have the best (first annual) productivity improvement trend over time using this method for both oil and gas
second method:
-sort production data by company then by date, aggregate production volume for each date and take an average production (for both oil and gas) for each date that an operator was producing
-plot monthly average production data over time (date) in SpotFire by operators 
-capture productivity performance trend over time by fitting a polynomial curve to the scattered monthly average productivity data
-MARATHON OIL COMPANY seem to have the best producivity improvement over time using this method for both oil and gas

-Data visualized in SpotFire using scatter plot and curve fits: 
case_study_visualization.dxp > q3 for method 1
case_study_visualization.dxp > q3_1 for method 2