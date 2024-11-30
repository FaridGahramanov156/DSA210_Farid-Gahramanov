import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.dates import DateFormatter

# Set the output folder for images
output_folder = "visualizations"
os.makedirs(output_folder, exist_ok=True)

# File paths
search_counts_file = "filtered_daily_search_counts_2024.csv"
exam_counts_file = "exam_counts_with_subjects_2024.csv"

try:
    # Load daily search counts
    search_counts_df = pd.read_csv(search_counts_file)
    search_counts_df['Date'] = pd.to_datetime(search_counts_df['Date'], errors='coerce')

    # Exclude July and August
    search_counts_df = search_counts_df[
        ~search_counts_df['Date'].dt.month.isin([7, 8])
    ]

    # Add 'Month' column with short month names
    search_counts_df['Month'] = search_counts_df['Date'].dt.strftime('%b')  # Short month names

    # Load exam counts
    exam_counts_df = pd.read_csv(exam_counts_file)
    exam_counts_df['Date'] = pd.to_datetime(exam_counts_df['Date'], errors='coerce')

    # Create a set of exact exam dates
    exam_dates = set(exam_counts_df['Date'].dropna())

    # Create a set of dates within the 10-day period before each exam, excluding the exam dates themselves
    previous_exam_dates = {
        date + pd.Timedelta(days=offset)
        for date in exam_dates
        for offset in range(-10, 0)
    } - exam_dates  # Remove any overlap with exact exam dates

    # Assign categories to dates
    search_counts_df['Category'] = search_counts_df['Date'].apply(
        lambda date: 'Exam Period or Exam Date' if date in exam_dates or date in previous_exam_dates
        else 'Other'
    )

    # Calculate means and medians
    blue_part = search_counts_df[search_counts_df['Category'] == 'Other']['Search Count']
    red_green_part = search_counts_df[
        search_counts_df['Category'] == 'Exam Period or Exam Date'
    ]['Search Count']

    blue_mean = blue_part.mean()
    blue_median = blue_part.median()
    red_green_mean = red_green_part.mean()
    red_green_median = red_green_part.median()

    print(f"Other Dates (Blue) - Mean: {blue_mean}, Median: {blue_median}")
    print(f"Exam Period or Exam Date (Green/Red) - Mean: {red_green_mean}, Median: {red_green_median}")

    # Visualization 1: Histogram
    fig, ax = plt.subplots(figsize=(18, 8))
    colors = search_counts_df['Category'].map({'Exam Period or Exam Date': 'green', 'Other': 'blue'})
    ax.bar(search_counts_df['Date'], search_counts_df['Search Count'], color=colors, width=1)

    # Add mean and median lines
    ax.axhline(blue_mean, color='blue', linestyle='--', linewidth=1.5, label=f'Other Mean ({blue_mean:.2f})')
    ax.axhline(blue_median, color='blue', linestyle='-', linewidth=1.5, label=f'Other Median ({blue_median:.2f})')
    ax.axhline(red_green_mean, color='green', linestyle='--', linewidth=1.5, label=f'Exam Period Mean ({red_green_mean:.2f})')
    ax.axhline(red_green_median, color='green', linestyle='-', linewidth=1.5, label=f'Exam Period Median ({red_green_median:.2f})')

    # Customize histogram
    ax.set_title('Daily Search Counts Histogram with Mean and Median', fontsize=16)
    ax.set_xlabel('Date', fontsize=12)
    ax.set_ylabel('Search Count', fontsize=12)
    ax.xaxis.set_major_formatter(DateFormatter("%b"))
    ax.tick_params(axis='x', rotation=90)
    ax.grid(alpha=0.7, linestyle='--')
    ax.legend()

    plt.tight_layout()
    histogram_path = os.path.join(output_folder, "histogram_with_means_medians.png")
    plt.savefig(histogram_path)
    plt.close()
    print(f"Histogram saved as '{histogram_path}'.")

    # Visualization 2: Bar Chart Comparison
    fig, ax = plt.subplots(figsize=(12, 8))
    category_counts = search_counts_df.groupby('Category')['Search Count'].sum()
    sns.barplot(
        x=category_counts.index,
        y=category_counts.values,
        palette={'Exam Period or Exam Date': 'green', 'Other': 'blue'},
        ax=ax
    )
    ax.set_title('Total Search Counts by Category', fontsize=16)
    ax.set_xlabel('Category', fontsize=12)
    ax.set_ylabel('Total Search Counts', fontsize=12)
    ax.grid(axis='y', alpha=0.7, linestyle='--')
    plt.tight_layout()
    bar_chart_path = os.path.join(output_folder, "bar_chart.png")
    plt.savefig(bar_chart_path)
    plt.close()
    print(f"Bar Chart saved as '{bar_chart_path}'.")

    # Visualization 3: Grouped Bar Chart
    grouped_data = search_counts_df.groupby(['Month', 'Category'])['Search Count'].sum().unstack(fill_value=0)
    grouped_data[['Exam Period or Exam Date', 'Other']].plot(
        kind='bar',
        figsize=(14, 7),
        color=['green', 'blue'],
        alpha=0.7
    )

    plt.title('Search Counts by Month and Category', fontsize=16)
    plt.xlabel('Month', fontsize=12)
    plt.ylabel('Total Search Counts', fontsize=12)
    plt.grid(axis='y', alpha=0.7, linestyle='--')
    plt.legend(title='Category', loc='upper right')
    plt.xticks(rotation=45)
    grouped_bar_chart_path = os.path.join(output_folder, "grouped_bar_chart.png")
    plt.savefig(grouped_bar_chart_path)
    plt.close()
    print(f"Grouped Bar Chart saved as '{grouped_bar_chart_path}'.")

    print(f"All visualizations saved in the folder: {output_folder}")

except Exception as e:
    print(f"An error occurred: {e}")
