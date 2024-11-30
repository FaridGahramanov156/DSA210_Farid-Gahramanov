import pandas as pd

# File paths
daily_search_counts_file = "filtered_daily_search_counts_2024.csv"
exam_counts_with_subjects_file = "exam_counts_with_subjects_2024.csv"
output_file = "final_visualization_data.csv"

try:
    # Load the daily search counts
    print("Loading daily search counts...")
    daily_search_counts = pd.read_csv(daily_search_counts_file)
    daily_search_counts.columns = ["Date", "Search Count"]  # Rename columns for clarity

    # Load the exam counts with subjects
    print("Loading exam counts with subjects...")
    exam_counts_with_subjects = pd.read_csv(exam_counts_with_subjects_file)
    exam_counts_with_subjects.columns = ["Date", "Exam Count", "Subjects"]  # Rename columns for clarity

    # Merge the data
    print("Merging data...")
    merged_data = pd.merge(
        daily_search_counts,
        exam_counts_with_subjects,
        on="Date",
        how="outer"
    ).fillna({"Search Count": 0, "Exam Count": 0, "Subjects": "None"})  # Fill missing values

    # Save the merged data to a CSV file
    print(f"Saving merged data to {output_file}...")
    merged_data.to_csv(output_file, index=False)

    print("Final visualization data saved successfully!")

except Exception as e:
    print(f"An error occurred: {e}")
