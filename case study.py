import pandas as pd
import numpy as np
import scipy.optimize
import scipy.integrate

def grab_headers(filename):
    """
    :param filename: name of raw data file
    :return: string list of headers from extracted from raw data
    """
    with open(filename, 'r') as csvDatafile:
        for line in csvDatafile:
            headers = line.strip().split(',')
            break
    return headers

def read_data(filename, rel_col):
    """
    :param filename: name of raw data file
           rel_col: list of relevant columns to be read in
    :return: dataframe of read data
    """
    return pd.read_csv(filename, usecols= rel_col, index_col=False)

def find_relevant_headers(all_headers, key_words):
    """
    :param all_header: list of all header from csv data
           key_words = list of key_words used to select relevant column
    :return: rel_headers_index: list of index of relevant headers
             rel_headers: list name of relevant headers
    """
    rel_headers = []
    for header in all_headers:
        for key in key_words:
            if key.lower() in header.lower():
                rel_headers.append(header)

    # removes duplicate header from header list while preserving order
    seen = {}
    rel_headers = [seen.setdefault(x, x) for x in rel_headers if x not in seen]

    # grabs index
    rel_headers_index = [i for i, item in enumerate(all_headers) if item in rel_headers]
    return rel_headers_index, rel_headers

def group_data(data, group_by_col):
    """
    :param data: dataframe of well data csv file
           group_by_col: name of column that dataframe needs to be grouped with & splited based on unique values in the column
    :return: list of dataframes splited based on unique value in group_by_col
    """
    unique_list = data[group_by_col].unique().tolist()
    grouped = data.groupby(data[group_by_col])
    data_grouped = []
    for item in unique_list:
        data_grouped.append(grouped.get_group(item))
    return data_grouped

def total_cum_oil_by_op(operator_list, welldata_grouped):
    """
    :param operator_list: list of unique operator name in welldata
           welldata_grouped: list of dataframes splited from well data dataframe based on unique operator
    :return: dictionary with operator name as first entry, and sum of operator's total cum_oil as second entry
    """
    cum_oil_dict = {}
    sum_oil_list = []
    for op_df in welldata_grouped:
        cum_oil = np.array(op_df['cum_oil'])
        sum_oil = np.sum(cum_oil)
        sum_oil_list.append(sum_oil)
    cum_oil_dict.update({"operator_name": operator_list})
    cum_oil_dict.update({"total oil production": sum_oil_list})
    return cum_oil_dict

def hyperbolic_func(t,qi,b,Di):
    return qi/(1+b*Di*t)**(1/b)

def determine_eur_per_well(proddata_grouped):
    """
    Methodology:
    -sort proddate_grouped (grouped by api) by index
    -remove and clean data point corresponding to wellbore storage, and shut in period
    -perform hyperbolic decline curve fit to determine hyperbolic curve parameters and the curve function(qi, b, Di)
    -integrate the curve function to determine EUR (assumed 200 months of production to reach economic limit)

    :param proddata_grouped:
    :return: data_list: [api_list, eur_list, operator_list, wellname_list]: list of api number, calculated eur, corresponding operator name and well name
    """
    df_sorted_list = []
    api_list = []; eur_list = []; operator_list = []; wellname_list = []
    #traverse through each well's production dataframe
    for df in proddata_grouped:
        # sort production data of each well by index (chronological)
        df_sorted = df.sort_values(by=["index"], ascending=True)
        df_sorted_list.append(df_sorted)

        #create list of month and production data
        month = df_sorted['index'].tolist()
        oil_prod = df_sorted['volume_oil_formation_bbls'].tolist()

        #identify and remove wellbore storage data, and remove shut in data (oil_prod = 0).
        max_index = oil_prod.index(max(oil_prod))
        month, oil_prod = month[max_index:], oil_prod[max_index:]

        #reset month index to start at 1
        month_offset = month[0]-1
        month[:] = [i - month_offset for i in month]

        #remove shut in month data (oil_prod = 0)
        a = np.array([month, oil_prod], dtype=int)
        a = a[:, a[1] != 0]

        #perform hyperbolic decline curve fit on data (find qi, b and Di value)
        a_month, a_oil_prod = np.array(a[0,:]), np.array(a[1,:])

        if len(oil_prod) > 5: # must have at least 5 production data point to fit curve
            fitted_param = scipy.optimize.curve_fit(hyperbolic_func, a_month, a_oil_prod, bounds=[0, [50000, 2, 100]])[0]
            #fitted_param = scipy.optimize.curve_fit(expontial_func,a_month,a_oil_prod)[0]
            qi = fitted_param[0]; b= fitted_param[1]; Di = fitted_param[2]
            hyp = lambda t: qi/(1+b*Di*t)**(1/b)
            EUR = int(scipy.integrate.quad(hyp, 0, 200)[0])
        else:
            EUR = 0

        api_list.append(df["api"].iloc[0])
        eur_list.append(EUR)
        operator_list.append(df["operator_name"].iloc[0])
        wellname_list.append(df["well_name"].iloc[0])

    return [api_list, eur_list, operator_list, wellname_list]

def eur_by_well(data_list):
    """
    :param data_list: [api_list, eur_list, operator_list, wellname_list]: list of unique api number, calculated EUR, corresponding operator name, and well name
    :return: dictionary with api value as first entry, EUR of the well as second entry, and operator name as third entry
    """
    eur_dict = {}
    eur_dict.update({"api": data_list[0]})
    eur_dict.update({"EUR oil": data_list[1]})
    eur_dict.update({"operator_name": data_list[2]})
    eur_dict.update({"well_name": data_list[3]})
    return eur_dict

def estimate_total_reserve_by_op(operator_list, eur_data):
    """
    :param operator_list: list of unique operator name in welldata
           eur_data: dataframe of eur data for each well
    :return: dictionary with operator name as first entry, and operator's total estimated reserve as second entry
    """
    eur_grouped = group_data(eur_data, "operator_name")
    eur_by_op_dict = {}
    total_reserve_list = []
    for op_df in eur_grouped:
        eur_oil = np.array(op_df['EUR oil'])
        total_reserve = np.sum(eur_oil)
        total_reserve_list.append(total_reserve)
    eur_by_op_dict.update({"operator_name": operator_list})
    eur_by_op_dict.update({"Total Estimated Reserve": total_reserve_list})
    return eur_by_op_dict


def main():
    #grab all headers in csv data
    filename = "ND_WELL_DATA.csv"; filename1 = "ND_PRODUCTION_DATA.csv"
    all_well_header = grab_headers(filename)
    all_prod_header = grab_headers(filename1)

    #define relevant columns from each csv through selecting key words in headers
    key_words = [["api", "date", "operator", "cum", "field","spud", "well"], ["api", "date", "index", "volume"]]
    well_rel_headers_index, well_rel_headers = find_relevant_headers(all_well_header, key_words[0])
    prod_rel_headers_index, prod_rel_headers = find_relevant_headers(all_prod_header, key_words[1])

    #read csv data using only relevant column
    welldata = read_data(filename, well_rel_headers_index)
    proddata = read_data(filename1, prod_rel_headers_index)

    """""""""""""""QUESTION 1"""""""""""""""""

    #group and split well data by operator
    welldata_grouped = group_data(welldata, "operator_name")
    unique_operator_list = welldata['operator_name'].unique().tolist()
    cum_oil_dict = total_cum_oil_by_op(unique_operator_list, welldata_grouped)

    #print question 1 results:
    print("Question 1: Total Historical Oil Production by Operators")
    for i in range (len(unique_operator_list)):
        print("\t", unique_operator_list[i], ":", cum_oil_dict.get("total oil production")[i],"bbl")

    #write question 1 result to csv
    q1_df = pd.DataFrame(data=cum_oil_dict)
    q1_df.to_csv("q1_total_oil_prod_by_op.csv", index=False)

    """
    See "case_study_visualization.dxp > q1" for visualized total historical production by company in SpotFire
    """

    """""""""""""""QUESTION 2"""""""""""""""""

    #create a dictionary of api numbers and their operator names
    api_list = welldata["api"].tolist()
    op_of_api_list = welldata["operator_name"].tolist()
    well_name_list = welldata["well_name"].tolist()
    api_to_op_dict = dict(zip(api_list, op_of_api_list))
    api_to_wellname_dict = dict(zip(api_list, well_name_list))

    #map operator name to production data based on api number
    proddata['operator_name'] = proddata['api'].map(api_to_op_dict)
    proddata['well_name'] = proddata['api'].map(api_to_wellname_dict)

    # group production data by api number
    proddata_grouped = group_data(proddata, "api")

    #calculate EUR of each well using hyperbolic decline curve analysis
    data_list = determine_eur_per_well(proddata_grouped)
    
    #map calculated eur data to dictionary then to csv
    eur_dict = eur_by_well(data_list)
    q2_df = pd.DataFrame(data=eur_dict)
    q2_df.to_csv("q2_eur_per_well.csv", index=False)

    print("Question 2: Determine EUR per well by company")
    eur_list = [np.NaN if x == 0 else x for x in data_list[1]]
    for i in range(len(eur_list)):
        print("\tWell:", data_list[3][i], "(", data_list[0][i], "), EUR:", eur_list[i], "bbl, Operator:", data_list[2][i])

    #determine total estimated reserve for each operator
    eur_by_op_dict = estimate_total_reserve_by_op(unique_operator_list, q2_df)
    q2_1_df = pd.DataFrame(data=eur_by_op_dict)
    q2_1_df.to_csv("q2_total_reserve_by_op.csv", index=False)


    """
    NOTE: EUR was not determined (EUR = NaN) for wells with less than 5 production data point after removal of outliers (wellbore storage, shut in, etc.)
    
    See "case_study_visualization.dxp > q2" for visualized oil eur per well by company in SpotFire
    

    """"""""""""QUESTION 3""""""""""""""
    
    See "case_study_visualization.dxp > q3" for visualized oil eur per well by company in SpotFire
    
    Methodology:
    -first year annual hydrocarbon production (cum_12_oil, cum_12_gas) is plotted against spud_date to capture development of productivity vs. time
    -6th degree polynomial fitted to scattered data in SpotFire to compare first year annual productivity of each well vs time the well was drilled
    -Identified best increasing trend in first year productivity over time that well was drilled
    """
    print("Question 3: Company that will drill the most most productive well:")
    print("\tWPX ENERGY WILLISTON LLC is likely to drill the most productive oil and gas well based on analysis in SpotFire")

main()
