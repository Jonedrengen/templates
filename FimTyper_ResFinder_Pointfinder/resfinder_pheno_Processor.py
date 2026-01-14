# resfinder_pheno_Processor.py script works with Pegasus run_fim_res_point_int_Finder.sh, which is run on the resFinder folder output.
# Created by: Edward Sung (edward.sung@gwu.edu) on 02/06/23

# Version: 1.0
# Updated: Edward Sung (edward.sung@gwu.edu) on 02/12/25


# %% Import Packages and Dependencies
# Packages
import pandas as pd
import xlsxwriter
import numpy as np
import os
import argparse
import re

# %% Argument Parsers
parser = argparse.ArgumentParser()
parser.add_argument("dir_path", help="User provided directory path to the resFinder results text data files")
parser.add_argument("output_name", help="User provided output_file_name")
args = parser.parse_args()

dir_path = args.dir_path + "/"
output_name = args.output_name

# Testing Purposes
# dir_path = "/Users/edward.sung/Desktop/resfinder/resfinder_testrun_output/processing_files"
# output_name = "resfinder_pheno_outputTEST"

# %% Locate resfinder_output folders and compile the pheno_table.txt output files into a mainData
# Collect all the sample outputs in the processing_files folder
folderList = [folder for folder in os.listdir(dir_path)]

# Obtain the current version database antibiotic list and classes; it requires an output file to generate a template.
# This searches just incase the first output file generated doesn't have any outputs/results.
i = 0
tmp_template_file = dir_path + "/" + folderList[i] + "/resfinder_output" + "/" + folderList[i] + "_resfinder_output" + "/pheno_table.txt"
while (os.path.getsize(tmp_template_file) == 0) and i < len(folderList) - 1:
    i += 1
    tmp_template_file = dir_path + "/" + folderList[i] + "/resfinder_output" + "/" + folderList[i] + "_resfinder_output" + "/pheno_table.txt"

# Generate mainData column lists
template_data = pd.read_csv(tmp_template_file, sep="\t", skiprows=16)

# Order is important since these are a pair
mainData_antimicrobial_cols = list(template_data["# Antimicrobial"])
mainData_antimicrobial_class_cols = ["Class"] + list(template_data["Class"])

# Initialize mainData
mainData_table = []

# Loop and collect the pheno data
for folder in folderList:
    print("Processing: ", folder)
    filepath = dir_path + "/" + folder + "/resfinder_output" + "/" + folder + "_resfinder_output" + "/pheno_table.txt" # Extract data from pheno_table.txt

    base_dict = {
        "Antimicrobial" : folder
    }

    # Check if file is empty, no results, add NAs and move to next file
    if os.path.getsize(filepath) == 0:
        for antimicrobial in mainData_antimicrobial_cols:
            base_dict[antimicrobial] = "NA"

        mainData_table.append(base_dict)
        print(folder, " is empty with no results.")
        continue    

    ''' From the pheno_table.txt informational section
    # The phenotype 'No resistance' should be interpreted with
    # caution, as it only means that nothing in the used
    # database indicate resistance, but resistance could exist
    # from 'unknown' or not yet implemented sources.
    # 
    # The 'Match' column stores one of the integers 0, 1, 2, 3.
    #      0: No match found
    #      1: Match < 100% ID AND match length < ref length
    #      2: Match = 100% ID AND match length < ref length
    #      3: Match = 100% ID AND match length = ref length
    # If several hits causing the same resistance are found,
    # the highest number will be stored in the 'Match' column.
    '''

    # First 17 rows are informational
    rawData = pd.read_csv(filepath, sep="\t", skiprows=16)

    # Extract the respective antimicrobial "Match" number
    for antimicrobial in mainData_antimicrobial_cols:
        base_dict[antimicrobial] = rawData[rawData["# Antimicrobial"] == antimicrobial]["Match"].values[0]

    mainData_table.append(base_dict)

# Convert to dataframe
mainData_df = pd.DataFrame(mainData_table)

# Add the antimicrobial_class associated to the antimicrobial
mainData_df = pd.concat([pd.DataFrame([mainData_antimicrobial_class_cols], columns=mainData_df.columns), mainData_df], ignore_index=True)

#%% Output antimicrobial DataFrame
mainData_df_output_name = output_name + "_pheno_antimicrobial.csv"
mainData_df.to_csv(mainData_df_output_name, index=False)








#%%
# Archived Code
'''
# %%
# Create dataframe from dictionary
mainData_df = pd.DataFrame.from_dict(mainData_dict)

# Add in the antimicrobial classifications columns
mainData_df["Antimicrobial"] = antimicrobial_List
mainData_df["Class"] = antimicrobial_Class

# Sort by Class column
mainData_df.sort_values(by=["Class"], inplace=True)

# Set the classifications as index
mainData_df.set_index(["Antimicrobial", "Class"], inplace=True)

# Transpose to get standard readable output format
mainData_df_T = mainData_df.transpose()

# Reset index to obtain genome names in dataframe
mainData_df_T.reset_index(inplace=True)

# Rename index back to Genome_Ref
mainData_df_T.rename(columns={"index": "Genome_Ref"}, inplace=True)

#%%

 rawData = pd.read_csv(filepath, sep="\t", skiprows=16)
    # rawData.replace(np.nan, 0, inplace=True) # Convert all NAs to 0, since no value in Match column even though the phenotype column says "Resistant"
    # rawData.columns = ["Match"]  # Add header
    # Genome_Ref = folder.replace(".fasta_resfinder_output", "") # Obtain genome name
    #
    # # Add to the mainData dictionary
    # mainData_dict[Genome_Ref] = rawData["Match"]


# Internal database kept in script
# antimicrobial_List is a 1 to 1 match to antimicrobial_Class, where order matters.
antimicrobial_List = ['gentamicin',
                      'tobramycin',
                      'streptomycin',
                      'amikacin',
                      'isepamicin',
                      'dibekacin',
                      'kanamycin',
                      'neomycin',
                      'lividomycin',
                      'paromomycin',
                      'ribostamycin',
                      'unknown aminoglycoside',
                      'butiromycin',
                      'butirosin',
                      'hygromycin',
                      'netilmicin',
                      'apramycin',
                      'sisomicin',
                      'arbekacin',
                      'kasugamycin',
                      'astromicin',
                      'fortimicin',
                      'g418',
                      'gentamicin c',
                      'kanamycin a',
                      'spectinomycin',
                      'fluoroquinolone',
                      'ciprofloxacin',
                      'unknown quinolone',
                      'nalidixic acid',
                      'amoxicillin',
                      'amoxicillin+clavulanic acid',
                      'ampicillin',
                      'ampicillin+clavulanic acid',
                      'cefepime',
                      'cefixime',
                      'cefotaxime',
                      'cefoxitin',
                      'ceftazidime',
                      'ertapenem',
                      'imipenem',
                      'meropenem',
                      'piperacillin',
                      'piperacillin+tazobactam',
                      'unknown beta-lactam',
                      'aztreonam',
                      'cefotaxime+clavulanic acid',
                      'temocillin',
                      'ticarcillin',
                      'ceftazidime+avibactam',
                      'penicillin',
                      'ceftriaxone',
                      'ticarcillin+clavulanic acid',
                      'cephalothin',
                      'cephalotin',
                      'piperacillin+clavulanic acid',
                      'ceftiofur',
                      'sulfamethoxazole',
                      'trimethoprim',
                      'fosfomycin',
                      'vancomycin',
                      'teicoplanin',
                      'bleomycin',
                      'lincomycin',
                      'clindamycin',
                      'dalfopristin',
                      'pristinamycin iia',
                      'virginiamycin m',
                      'quinupristin+dalfopristin',
                      'tiamulin',
                      'carbomycin',
                      'erythromycin',
                      'azithromycin',
                      'oleandomycin',
                      'spiramycin',
                      'tylosin',
                      'telithromycin',
                      'tetracycline',
                      'doxycycline',
                      'minocycline',
                      'tigecycline',
                      'quinupristin',
                      'pristinamycin ia',
                      'virginiamycin s',
                      'linezolid',
                      'chloramphenicol',
                      'florfenicol',
                      'colistin',
                      'fusidic acid',
                      'mupirocin',
                      'rifampicin',
                      'metronidazole',
                      'narasin',
                      'salinomycin',
                      'maduramicin']

antimicrobial_Class = ["aminoglycoside",
                       "aminoglycoside",
                       "aminoglycoside",
                       "aminoglycoside",
                       "aminoglycoside",
                       "aminoglycoside",
                       "aminoglycoside",
                       "aminoglycoside",
                       "No_Class",
                       "aminoglycoside",
                       "aminoglycoside",
                       "aminoglycoside",
                       "No_Class",
                       "No_Class",
                       "No_Class",
                       "aminoglycoside",
                       "aminoglycoside",
                       "No_Class",
                       "aminoglycoside",
                       "No_Class",
                       "aminoglycoside",
                       "No_Class",
                       "No_Class",
                       "No_Class",
                       "aminoglycoside",
                       "aminocyclitol",
                       "quinolone",
                       "quinolone",
                       "No_Class",
                       "quinolone",
                       "beta-lactam",
                       "beta-lactam",
                       "beta-lactam",
                       "No_Class",
                       "beta-lactam",
                       "beta-lactam",
                       "beta-lactam",
                       "beta-lactam",
                       "beta-lactam",
                       "beta-lactam",
                       "beta-lactam",
                       "beta-lactam",
                       "beta-lactam",
                       "beta-lactam",
                       "No_Class",
                       "beta-lactam",
                       "No_Class",
                       "beta-lactam",
                       "beta-lactam",
                       "beta-lactam",
                       "beta-lactam",
                       "beta-lactam",
                       "beta-lactam",
                       "beta-lactam",
                       "beta-lactam",
                       "No_Class",
                       "beta-lactam",
                       "folate_pathway_antagonist",
                       "folate_pathway_antagonist",
                       "fosfomycin",
                       "glycopeptide",
                       "glycopeptide",
                       "No_Class",
                       "lincosamide",
                       "lincosamide",
                       "streptogramin_a",
                       "streptogramin",
                       "streptogramin",
                       "streptogramin",
                       "pleuromutilin",
                       "No_Class",
                       "macrolide",
                       "macrolide",
                       "macrolide",
                       "macrolide",
                       "macrolide",
                       "macrolide",
                       "tetracycline",
                       "tetracycline",
                       "tetracycline",
                       "tetracycline",
                       "streptogramin",
                       "streptogramin",
                       "streptogramin",
                       "oxazolidinone",
                       "amphenicol",
                       "amphenicol",
                       "polymyxin",
                       "steroid_antibacterial",
                       "pseudomonic_acid",
                       "ansamycins",
                       "nitroimidazole",
                       "No_Class",
                       "No_Class",
                       "No_Class"]
'''