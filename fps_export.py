import csv
import os
import pandas as pd

# Array of parallel job counts
num_jobs_array = [64, 32, 16, 8, 4, 2]
# Array of presets
presets = ["ultrafast", "veryfast", "medium"]

# Input video resolutions
resolutions = [720, 1080, 2160]

# Base input directory containing all input CSV files
base_input_directory = "/home/ubuntu/uthaya/ARM_script1/"
# Output directory to store the extracted FPS values CSV files
output_directory = os.path.join(base_input_directory, "average_fps")

# Create the output directory if it does not exist
os.makedirs(output_directory, exist_ok=True)

# Function to extract FPS values from CSV files and calculate the average FPS
def extract_average_fps(input_directory):
    fps_values = []

    # Iterate through all CSV files in the input directory
    for file_name in os.listdir(input_directory):
        if file_name.endswith(".csv"):  # Check if the file is a CSV
            file_path = os.path.join(input_directory, file_name)

            try:
                with open(file_path, newline='', encoding='utf-8') as csvfile:
                    reader = csv.reader(csvfile)

                    # Skip the header row
                    next(reader)

                    # Read the second line
                    row = next(reader, None)

                    if row is not None:
                        # Extract the 4th value (index 3) if it exists
                        fps_value = row[3] if len(row) > 3 else None

                        if fps_value is not None:
                            # Try to convert to a float and add to the list
                            try:
                                fps_values.append(float(fps_value))
                            except ValueError:
                                print(f"Invalid FPS value in {file_name}: {fps_value}")
                    else:
                        print(f"No data found in {file_name}")

            except Exception as e:
                print(f"Error processing {file_name}: {e}")

    # Calculate the average FPS if there are any valid values
    if fps_values:
        avg_fps = sum(fps_values) / len(fps_values)
        return avg_fps
    else:
        return None

# Main loop to iterate over resolutions, job counts, and presets
for resolution in resolutions:
    resolution_dir = f"spoc_{resolution}p"
    
    # Prepare a list to store data for each resolution
    resolution_data = []

    for num_jobs in num_jobs_array:
        for preset in presets:
            # Define input directory based on num_jobs, preset, and resolution
            input_directory = os.path.join(base_input_directory, resolution_dir, f"{num_jobs}encode", preset)

            # Extract and calculate the average FPS from CSV files in the input directory
            avg_fps = extract_average_fps(input_directory)

            if avg_fps is not None:
                # Append the data for this (num_jobs, preset) combination
                resolution_data.append({
                    'Resolution': f"{resolution}p",
                    'Num Jobs': num_jobs,
                    'Preset': preset,
                    'Average FPS': avg_fps
                })

    # Save all the data for the current resolution into a single CSV file
    if resolution_data:
        output_csv = os.path.join(output_directory, f"ARM_avgfps_{resolution}p.csv")
        resolution_df = pd.DataFrame(resolution_data)
        resolution_df.to_csv(output_csv, index=False)
        print(f"All average FPS data for {resolution}p has been saved to {output_csv}")
    else:
        print(f"No valid FPS data found for {resolution}p. No CSV file created.")
