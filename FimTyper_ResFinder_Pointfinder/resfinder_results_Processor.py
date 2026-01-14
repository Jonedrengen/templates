# resfinder_results_Processor.py script works with Pegasus run_fim_res_point_int_Finder.sh, which is run on the resFinder folder output.
# Created by: Edward Sung (edward.sung@gwu.edu) on 02/06/23

# Version: 1.0
# Updated: Edward Sung (edward.sung@gwu.edu) on 02/12/25


#%%
# Packages
import pandas as pd
import os
import argparse

#%% Argument Parsers
parser = argparse.ArgumentParser()
parser.add_argument("dir_path", help="User provided directory path to the resfinder_output results text data files")
parser.add_argument("output_name", help="User provided output_file_name")
args = parser.parse_args()

dir_path = args.dir_path + "/"
output_name = args.output_name

# Testing Purposes
# dir_path = "/Users/edward.sung/Desktop/resfinder/resfinder_testrun_output/processing_files"
# output_name = "resFinder_results_testoutput"

#%%
# Compiled data
data_table_phenotype = []
data_table_resistance = []

def has_nested_list(lst):
    '''
    Check if it is a nested list

    Use case in pheno_dict and resistance_dict is to check the exception cases where there are multiple best hits.
    Example: 99.88_100.0; 100.0_99.88
    This is a cell for a resistance hit, two values but equally viable results
    '''
    for item in lst:
        if isinstance(item, list):
            return True
    return False


folderList = [folder for folder in os.listdir(dir_path)]

# Loop through and process the resfinder_output folders (ResFinder_results_tab.txt)
for folder in folderList:
    print("Processing: ", folder)

    datapath = dir_path + "/" + folder + "/resfinder_output" + "/" + folder + "_resfinder_output" + "/ResFinder_results_tab.txt" # Extract data from ResFinder_results_tab.txt

    # Check if file is empty, no results, skip file
    if os.path.getsize(datapath) == 0:
        print(folder, " is empty with no results.")
        continue

    res_data = pd.read_csv(datapath, sep="\t")

    # Subset for 80% >= identity and coverage
    res_data_subset = res_data[(res_data["Identity"] >= 80) & (res_data["Coverage"] >= 80)]
    res_data_subset.reset_index(inplace=True, drop=True)

    # Process the Phenotype column
    pheno_dict = {
        "filename": folder
    }

    for index in range(len(res_data_subset)):
        phenotypes = res_data_subset["Phenotype"][index]
        identity = float(res_data_subset["Identity"][index])
        coverage = float(res_data_subset["Coverage"][index])

        # Split out the phenotypes
        for phenotype in phenotypes.split(", "):
            if phenotype in pheno_dict:
                if has_nested_list(pheno_dict[phenotype]):
                    if pheno_dict[phenotype][0][0] <= identity and pheno_dict[phenotype][0][1] <= coverage:
                        pheno_dict[phenotype][0] = [identity, coverage]

                    elif (pheno_dict[phenotype][0][0] < identity and pheno_dict[phenotype][0][1] > coverage) or (pheno_dict[phenotype][0][0] > identity and pheno_dict[phenotype][0][1] < coverage):
                        print("Exception Case Phenotype: Identity or Coverage changed in opposite directions to current best")
                        pheno_dict[phenotype].append([identity, coverage])
                else:
                    if pheno_dict[phenotype][0] <= identity and pheno_dict[phenotype][1] <= coverage:
                        pheno_dict[phenotype] = [identity, coverage]

                    elif (pheno_dict[phenotype][0] < identity and pheno_dict[phenotype][1] > coverage) or (pheno_dict[phenotype][0] > identity and pheno_dict[phenotype][1] < coverage):
                        print("AAAException Case Phenotype: Identity or Coverage changed in opposite directions to current best")
                        pheno_dict[phenotype] = [pheno_dict[phenotype], [identity, coverage]]
            else:
                pheno_dict[phenotype] = [identity, coverage]

    # Concat the identity and coverage results for matrix input, also round to 2 decimals
    for pheno in pheno_dict:
        if pheno != "filename":
            if has_nested_list(pheno_dict[pheno]):
                tmp_list = [f"{round(x, 2)}_{round(y, 2)}" for x, y in pheno_dict[pheno]]
                pheno_dict[pheno] = '; '.join(ph for ph in list(set(tmp_list)))
            else:
                pheno_dict[pheno] = '_'.join(str(round(ph, 2)) for ph in pheno_dict[pheno])

    data_table_phenotype.append(pheno_dict)

    # Process the Resistance gene column
    resistance_dict = {
        "filename": folder
    }
    for index in range(len(res_data_subset)):
        resistance_gene = res_data_subset["Resistance gene"][index]
        identity = float(res_data_subset["Identity"][index])
        coverage = float(res_data_subset["Coverage"][index])

        if resistance_gene in resistance_dict:
            if has_nested_list(resistance_dict[resistance_gene]):
                if resistance_dict[resistance_gene][0][0] <= identity and resistance_dict[resistance_gene][0][1] <= coverage:
                    resistance_dict[resistance_gene][0] = [identity, coverage]

                elif (resistance_dict[resistance_gene][0][0] < identity and resistance_dict[resistance_gene][0][1] > coverage) or (resistance_dict[resistance_gene][0][0] > identity and resistance_dict[resistance_gene][0][1] < coverage):
                    print("Exception Case Resistance Gene: Identity or Coverage changed in opposite directions to current best")
                    resistance_dict[resistance_gene].append([identity, coverage])
            else:
                if resistance_dict[resistance_gene][0] <= identity and resistance_dict[resistance_gene][1] <= coverage:
                    resistance_dict[resistance_gene] = [identity, coverage]

                elif (resistance_dict[resistance_gene][0] < identity and resistance_dict[resistance_gene][1] > coverage) or (resistance_dict[resistance_gene][0] > identity and resistance_dict[resistance_gene][1] < coverage):
                    print("AAAAException Case Resistance Gene: Identity or Coverage changed in opposite directions to current best")
                    resistance_dict[resistance_gene] = [resistance_dict[resistance_gene], [identity, coverage]]
        else:
            resistance_dict[resistance_gene] = [identity, coverage]

    # Concat the identity and coverage results for matrix input, also round to 2 demicals
    for resistance in resistance_dict:
        if resistance != "filename":
            if has_nested_list(resistance_dict[resistance]):
                tmp_list = [f"{round(x, 2)}_{round(y, 2)}" for x, y in resistance_dict[resistance]]
                resistance_dict[resistance] = '; '.join(res for res in list(set(tmp_list)))
            else:
                resistance_dict[resistance] = '_'.join(str(round(res, 2)) for res in resistance_dict[resistance])

    data_table_resistance.append(resistance_dict)


# Convert to dataframe
full_data_table_phenotype = pd.DataFrame(data_table_phenotype)
full_data_table_resistance = pd.DataFrame(data_table_resistance)

# Export dataframe
output_filename_phenotype = output_name + "_resFinder_results_phenotype_Matrix.csv"
full_data_table_phenotype.to_csv(output_filename_phenotype, index=False)

output_filename_resistance = output_name + "_resFinder_results_resistance_Matrix.csv"
full_data_table_resistance.to_csv(output_filename_resistance, index=False)