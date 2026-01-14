#!/bin/sh
#SBATCH --time 2-00:00:00
#SBATCH -p highThru,384gb
#SBATCH -o fim_res_point_int_Finder_Compiler_%j.out
#SBATCH -e fim_res_point_int_Finder_Compiler_%j.err


STARTTIMER="$(date +%s)"


# Conda Enviroment - Please change to load your conda environment
. /GWSPH/groups/liu_price_lab/tools/anaconda3/etc/profile.d/conda.sh
conda activate cge_tools_env

# Modules - Please add any modules required


# Script and Tool Locations - Include any additional script path as needed
scriptLocation="/scratch/liu_price_lab/ehsung/github/Development/ehsung/microbiome/CGE_tools/scripts/fim_res_point_int_Finder"
python_scriptsLocation="/scratch/liu_price_lab/ehsung/github/Development/ehsung/microbiome/CGE_tools/scripts/fim_res_point_int_Finder/python_processor_scripts"


# Inputs
main_output_folder_input=$1
job_name=$2

# Compiled folder
mkdir $main_output_folder_input/compiled_files
mkdir $main_output_folder_input/compiled_files/slurmFiles

# Create a list of your output folders
ls $main_output_folder_input/processing_files > tmplist_output_folders

# Results files
echo -e "Fimtype\tIdentity\tQuery/HSP\tContig\tFASTA_File" > $main_output_folder_input/compiled_files/${job_name}_compiled_fimtyper_results.tsv
echo -e "Resistance_Gene\tIdentity\tAlignment_Length/Gene_Length\tCoverage\tPosition_in_reference\tContig\tPosition_in_contig\tPhenotype\tAccession_no.\tFASTA_File" > $main_output_folder_input/compiled_files/${job_name}_compiled_resfinder_results.tsv
echo -e "#Template\tScore\tExpected\tTemplate_length\tTemplate_Identity\tTemplate_Coverage\tQuery_Identity\tQuery_Coverage\tDepth\tq_value\tp_value\tFASTA_File" > $main_output_folder_input/compiled_files/${job_name}_compiled_intfinder_results.tsv

# fasta hit folder
mkdir $main_output_folder_input/compiled_files/ResFinder_Hit_in_genome_seq


# Loop through your output folders to compile your results
while read -r folder
do
   echo "Extracting results from: $folder"

   # fimtyper
   cat $main_output_folder_input/processing_files/$folder/fimtyper_output/${folder}_fimtyper_results.tsv | tail -n +2 >> $main_output_folder_input/compiled_files/${job_name}_compiled_fimtyper_results.tsv

   # resfinder
   cat $main_output_folder_input/processing_files/$folder/resfinder_output/${folder}_resfinder_results.tsv | tail -n +2 >> $main_output_folder_input/compiled_files/${job_name}_compiled_resfinder_results.tsv

   # intfinder
   cat $main_output_folder_input/processing_files/$folder/intfinder_output/${folder}_intfinder_results.tsv | tail -n +2 >> $main_output_folder_input/compiled_files/${job_name}_compiled_intfinder_results.tsv

   # fasta hit file
   cp $main_output_folder_input/processing_files/$folder/resfinder_output/${folder}_resfinder_output/ResFinder_Hit_in_genome_seq.fsa $main_output_folder_input/compiled_files/ResFinder_Hit_in_genome_seq/${folder}_ResFinder_Hit_in_genome_seq.fsa
done < tmplist_output_folders

# Run python resfinder compiler
python $python_scriptsLocation/resfinder_pheno_Processor.py $main_output_folder_input/processing_files $job_name
python $python_scriptsLocation/resfinder_results_Processor.py $main_output_folder_input/processing_files $job_name

mv ${job_name}_pheno_antimicrobial.csv $main_output_folder_input/compiled_files/
mv ${job_name}_resFinder_results_resistance_Matrix.csv $main_output_folder_input/compiled_files/
mv ${job_name}_resFinder_results_phenotype_Matrix.csv $main_output_folder_input/compiled_files/


# Clean-up file system
rm tmplist_output_folders
mv fim_res_point_int_Finder_Compiler_${SLURM_JOB_ID}.out $main_output_folder_input/compiled_files/slurmFiles
mv fim_res_point_int_Finder_Compiler_${SLURM_JOB_ID}.err $main_output_folder_input/compiled_files/slurmFiles


# Script Timer
ENDTIMER="$(date +%s)"
DURATION=$[${ENDTIMER} - ${STARTTIMER}]
HOURS=$((${DURATION} / 3600))
MINUTES=$(((${DURATION} % 3600)/ 60))
SECONDS=$(((${DURATION} % 3600) % 60))

echo "RUNTIMER: $HOURS:$MINUTES:$SECONDS (hh:mm:ss)"
