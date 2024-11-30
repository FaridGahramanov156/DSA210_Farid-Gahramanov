import json
from collections import defaultdict

# File path to exam dates JSON
file_path = "exam_dates.json"

# Ensure the file exists
try:
    # Load the JSON data
    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    # Extract exam dates and subjects
    exam_dates = data.get("exam_dates", [])
    exam_details = defaultdict(list)

    # Group subjects for each day, filtering only for 2024
    for exam_entry in exam_dates:
        date = exam_entry[0]  # The first element is the date
        if date.startswith("2024"):  # Filter for dates in 2024
            subjects = exam_entry[1:]  # The remaining elements are the subjects
            exam_details[date].extend(subjects)

    # Print the results
    print("Exam Counts and Subjects Per Day (2024):")
    for date, subjects in sorted(exam_details.items()):
        print(f"{date}: {len(subjects)} exams ({', '.join(subjects)})")

    # Save results to a CSV file
    output_file = "exam_counts_with_subjects_2024.csv"
    with open(output_file, mode="w", encoding="utf-8", newline="") as csv_file:
        csv_file.write("Date,Exam Count,Subjects\n")
        for date, subjects in sorted(exam_details.items()):
            csv_file.write(f"{date},{len(subjects)},\"{', '.join(subjects)}\"\n")
    print(f"Exam counts and subjects saved to {output_file}.")

except Exception as e:
    print(f"An error occurred: {e}")
