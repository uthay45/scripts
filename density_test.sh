#!/bin/bash

# Array of parallel job counts
num_jobs_array=(64 32 16 8 4 2)
# Array of presets
presets=("ultrafast" "veryfast" "medium")

# Input video files
input_files=(
   "/home/ubuntu/videos/Samsung_Power_of_Curve_1280x720_59.94_1500f.y4m"
   "/home/ubuntu/videos/Samsung_Power_of_Curve_1920x1080_59.94_1500f.y4m"
   "/home/ubuntu/videos/Samsung_Power_of_Curve_3840x2160_8bit_59.94_1500f.y4m"
)

resolutions=( 720 1080 2160 )

# x265 executable path
x265_executable="/home/ubuntu/uthaya/x265_latest/8bit/x265_git/build/linux/x265"

# Function to run a single encode
run_encode() {
    job_id=$1
    preset=$2
    output_dir=$3
    hevc_dir=$4
    input_file=$5
    output_file="${hevc_dir}spoc_${preset}_hevc_${job_id}.hevc"
    csv_file="${output_dir}spoc_${preset}_csv_${job_id}.csv"

    $x265_executable --input $input_file --preset $preset --pools 1 --frame-threads 1 --no-wpp --output $output_file --csv $csv_file
}

# Main loop to iterate over input files and resolutions
i=0
for input_file in "${input_files[@]}"; do
    resolution=${resolutions[i]}
    # Loop over each num_jobs value
    for num_jobs in "${num_jobs_array[@]}"; do
        # Loop over each preset
        for preset in "${presets[@]}"; do
            # Define output directory for the current num_jobs and preset combination
            hevc_dir="/home/ubuntu/uthaya/temp/spoc_${resolution}p/${num_jobs}encode/${preset}/"
            output_dir="/home/ubuntu/uthaya/ARM_script1/spoc_${resolution}p/${num_jobs}encode/${preset}/"
            mkdir -p "$hevc_dir"
            mkdir -p "$output_dir" # Create the output directory if it doesn't exist
            
            # Loop to start parallel jobs for the current num_jobs
            for j in $(seq 1 $num_jobs); do
                run_encode $j $preset $output_dir $hevc_dir $input_file &
            done
            # Wait for all jobs to finish
            wait
        done
    done
    ((i++))
done
