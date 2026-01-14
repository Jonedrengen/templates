#!/bin/sh
#SBATCH --time 4:00:00
#SBATCH -p tiny,debug,384gb
#SBATCH -e fim_res_point_int_Finder_Runner_%A_%a.err
#SBATCH -o fim_res_point_int_Finder_Runner_%A_%a.out


STARTTIMER="$(date +%s)"


# Conda Enviroment - Please change to load your conda environment
. /GWSPH/groups/liu_price_lab/tools/anaconda3/etc/profile.d/conda.sh
conda activate cge_tools_env


# Modules - Please add any modules required
module load perl5/5.28.1
module load blast+/2.16.0+


# Script and Tool Locations - Include any additional script path as needed
scriptLocation="/scratch/liu_price_lab/ehsung/github/Development/ehsung/microbiome/CGE_tools/scripts/fim_res_point_int_Finder"
cge_scriptsLocation="/scratch/liu_price_lab/ehsung/github/Development/ehsung/microbiome/CGE_tools/scripts/fim_res_point_int_Finder/cge_scripts"
kmaLocation="/scratch/liu_price_lab/ehsung/databases/kma/kma"

# Databases
resfinder_db="/scratch/liu_price_lab/ehsung/databases/resfinder_db/resfinder_db"
disinfinder_db="/scratch/liu_price_lab/ehsung/databases/disinfinder_db/disinfinder_db"
intfinder_db="/scratch/liu_price_lab/ehsung/databases/intfinder_db/intfinder_db"
fimtyper_db="/scratch/liu_price_lab/ehsung/databases/fimtyper_db/fimtyper_db"
pointfinder_db="/scratch/liu_price_lab/ehsung/databases/pointfinder_db/pointfinder_db"


# User Input
Data_Folder_input=$1
Data_Folder_Samplelist_SLURM_ARRAY_READY_input=$2
Data_Folder_Samplelist_SLURM_ARRAY_READY_index_set_input=$3
main_output_folder_input=$4

# Note these tools are targetting Escherichia coli - resFinder
# You can change the target species / database for resFinder by searching and changing: "Escherichia coli"


# Obtains the filename indicated by slurm_array_id
fileInput="$(cat $Data_Folder_Samplelist_SLURM_ARRAY_READY_input | grep "^${Data_Folder_Samplelist_SLURM_ARRAY_READY_index_set_input}__@__${SLURM_ARRAY_TASK_ID}__@__" | awk -F "__@__" '{print $3}')"


# Remove extensions to just get filename
filename=${fileInput%.*}


# Create results folders for outputs, as well as a place for results files
mkdir $main_output_folder_input/processing_files/$filename

mkdir $main_output_folder_input/processing_files/$filename/fimtyper_output
echo -e "Fimtype\tIdentity\tQuery/HSP\tContig\tFASTA_File" > $main_output_folder_input/processing_files/$filename/fimtyper_output/${filename}_fimtyper_results.tsv

mkdir $main_output_folder_input/processing_files/$filename/resfinder_output
echo -e "Resistance_Gene\tIdentity\tAlignment_Length/Gene_Length\tCoverage\tPosition_in_reference\tContig\tPosition_in_contig\tPhenotype\tAccession_no.\tFASTA_File" > $main_output_folder_input/processing_files/$filename/resfinder_output/${filename}_resfinder_results.tsv

mkdir $main_output_folder_input/processing_files/$filename/intfinder_output
echo -e "#Template\tScore\tExpected\tTemplate_length\tTemplate_Identity\tTemplate_Coverage\tQuery_Identity\tQuery_Coverage\tDepth\tq_value\tp_value\tFASTA_File" > $main_output_folder_input/processing_files/$filename/intfinder_output/${filename}_intfinder_results.tsv

mkdir $main_output_folder_input/processing_files/$filename/slurm_outputs



# fimtyper
echo "------------------------------------------------- Running fimtyper on: $fileInput"
perl $cge_scriptsLocation/fimtyper.pl -i $Data_Folder_input/$fileInput -o $main_output_folder_input/processing_files/$filename/fimtyper_output/${filename}_fimtyper_output -d $fimtyper_db -k 95.00 -l 0.60
tail -n +5 $main_output_folder_input/processing_files/$filename/fimtyper_output/${filename}_fimtyper_output/results_tab.txt | cut -f 1-4 > $main_output_folder_input/processing_files/$filename/fimtyper_output/fimtyper_tmpfile
sed "s/$/\t$filename/" $main_output_folder_input/processing_files/$filename/fimtyper_output/fimtyper_tmpfile >> $main_output_folder_input/processing_files/$filename/fimtyper_output/${filename}_fimtyper_results.tsv
rm $main_output_folder_input/processing_files/$filename/fimtyper_output/fimtyper_tmpfile


# resfinder (based off of resfinder settings)
echo "------------------------------------------------- Running resfinder on: $fileInput"
python -m resfinder -ifa $Data_Folder_input/$fileInput -o $main_output_folder_input/processing_files/$filename/resfinder_output/${filename}_resfinder_output -k $kmaLocation/kma -db_res $resfinder_db -db_point $pointfinder_db -s "Escherichia coli" -l 0.6 -t 0.8 --acquired --point
tail -n +2 $main_output_folder_input/processing_files/$filename/resfinder_output/${filename}_resfinder_output/ResFinder_results_tab.txt | cut -f 1-9 > $main_output_folder_input/processing_files/$filename/resfinder_output/resfinder_tmpfile
sed "s/$/\t$filename/" $main_output_folder_input/processing_files/$filename/resfinder_output/resfinder_tmpfile >> $main_output_folder_input/processing_files/$filename/resfinder_output/${filename}_resfinder_results.tsv
rm $main_output_folder_input/processing_files/$filename/resfinder_output/resfinder_tmpfile


# intfinder
echo "------------------------------------------------- Running intfinder on: $fileInput"
mkdir $main_output_folder_input/processing_files/$filename/intfinder_output/${filename}_intfinder_output
python $cge_scriptsLocation/intfinder.py -i $Data_Folder_input/$fileInput -p $intfinder_db -mp $kmaLocation/kma -o $main_output_folder_input/processing_files/$filename/intfinder_output/${filename}_intfinder_output
tail -n +2 $main_output_folder_input/processing_files/$filename/intfinder_output/${filename}_intfinder_output/kma_db1.res | cut -f 1-11 > $main_output_folder_input/processing_files/$filename/intfinder_output/${filename}_intfinder_output/intfinder_tmpfile
sed "s/$/\t$filename/" $main_output_folder_input/processing_files/$filename/intfinder_output/${filename}_intfinder_output/intfinder_tmpfile >> $main_output_folder_input/processing_files/$filename/intfinder_output/${filename}_intfinder_results.tsv
rm $main_output_folder_input/processing_files/$filename/intfinder_output/${filename}_intfinder_output/intfinder_tmpfile




# Clean-up File System
mv fim_res_point_int_Finder_Runner_${SLURM_ARRAY_JOB_ID}_${SLURM_ARRAY_TASK_ID}.err $main_output_folder_input/processing_files/$filename/slurm_outputs
mv fim_res_point_int_Finder_Runner_${SLURM_ARRAY_JOB_ID}_${SLURM_ARRAY_TASK_ID}.out $main_output_folder_input/processing_files/$filename/slurm_outputs


# Script Timer
ENDTIMER="$(date +%s)"
DURATION=$[${ENDTIMER} - ${STARTTIMER}]
HOURS=$((${DURATION} / 3600))
MINUTES=$(((${DURATION} % 3600)/ 60))
SECONDS=$(((${DURATION} % 3600) % 60))

echo "RUNTIMER: $HOURS:$MINUTES:$SECONDS (hh:mm:ss)"
