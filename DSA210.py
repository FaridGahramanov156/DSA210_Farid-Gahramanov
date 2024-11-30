import os
from bs4 import BeautifulSoup
from collections import Counter
from datetime import datetime
from dateutil import parser

# Set the file path to 'search-history.html' in the current directory
file_path = "search-history.html"

# Ensure the file exists
if not os.path.exists(file_path):
    print(f"Error: The file '{file_path}' was not found in the current directory.")
    exit()

try:
    # Parse the HTML file
    with open(file_path, "r", encoding="utf-8") as file:
        soup = BeautifulSoup(file, "html.parser")

    # Extract search history details
    search_dates = []
    for entry in soup.find_all("div", class_="content-cell mdl-cell mdl-cell--6-col mdl-typography--body-1"):
        text = entry.get_text(separator=" ").strip()
        if "Searched for" in text:
            try:
                # Extract the part after the last newline for the date
                date_text = text.split("\n")[-1].strip()
                # Remove the "Searched for" part if it's still there
                if "Searched for" in date_text:
                    date_text = date_text.replace("Searched for", "").strip()
                # Parse the date
                search_date = parser.parse(date_text, fuzzy=True)
                # Validate the year and exclude July and August
                if (
                    search_date.year == 2024 and
                    search_date.month not in [7, 8]
                ):
                    search_dates.append(search_date.date())  # Append only the date part (YYYY-MM-DD)
                else:
                    print(f"Excluding date: {date_text}")
            except (ValueError, parser.ParserError) as e:
                print(f"Skipping invalid date format: {text} - Error: {e}")
                continue

    # Count the searches per day
    daily_search_counts = Counter(search_dates)

    # Check if there are results
    if not daily_search_counts:
        print("No valid search history found in the file.")
    else:
        # Print the daily search counts with the number of searches
        print("Daily Search Counts (2024, excluding July and August):")
        for date, count in sorted(daily_search_counts.items()):
            print(f"{date}: {count} searches")

        # Save the results to a CSV file
        output_file = "filtered_daily_search_counts_2024.csv"
        with open(output_file, mode="w", encoding="utf-8", newline="") as csv_file:
            csv_file.write("Date,Search Count\n")
            for date, count in sorted(daily_search_counts.items()):
                csv_file.write(f"{date},{count}\n")
        print(f"Filtered daily search counts saved to {output_file}.")

except Exception as e:
    print(f"An error occurred: {e}")
