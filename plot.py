import re
from pprint import pprint
from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_theme()
# Gather data and keep in a dictionary

YEAR = 2025
days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
time_re = re.compile('\(([^)]+)')

def clean_day_number(x):
    for suffix in ("nd", "th", "st", "rd"):
        x = x.replace(suffix, "")

    return x

def get_data_per_year(year):
    if not year:
        return None
    data = {}
    for fname in sorted(Path(f"{year}").glob(f"{year}*.md")):
        date = str(fname).replace(f"{year}/", "").replace(".md", "").replace(".", "-")

        year, month = map(int, date.split("-"))

        if year not in data:
            data[year] = {}
        if month not in data[year]:
            data[year][month] = {}

        # Read file to gather project total time
        with open(fname) as f:
            for line in f:
                if line.startswith("#"):
                    project = line.strip().replace("# ", "")
                    if project not in data[year][month]:
                        data[year][month][project] = {}
                elif not line.startswith("*") and any(i in line for i in days):
                    day_name, day_number = line.strip().split("(")[0].split()
                    total_time = time_re.findall(line)[0]

                    day_number = int(clean_day_number(day_number))

                    minutes = 0
                    if "hour" in total_time:
                        minutes = float(total_time.split()[0]) * 60
                    elif "min" in total_time:
                        minutes = float(total_time.split()[0])
                    else:
                        print("oops")
                    if day_number not in data[year][month][project]:
                        data[year][month][project][day_number] = 0

                    data[year][month][project][day_number] += minutes
    return data


def plot_time_per_month():
    fig, ax = plt.subplots()
    ax.grid(zorder=0)
    x = [months[i-1] for i in time_per_month.keys()]
    y = [i/60.0 for i in time_per_month.values()]
    ax.bar(x, y, zorder=3)
    ax.set_ylabel('Hours')
    ax.set_title('Total hours per month')
    plt.show()

def plot_time_per_project():
    fig, ax = plt.subplots()
    ax.grid(zorder=0)
    x = list(time_per_project.keys())
    y = [i/60.0 for i in time_per_project.values()]
    ax.bar(x, y, zorder=3)
    plt.xticks(rotation=45, ha="right")
    ax.set_ylabel('Hours')
    ax.set_yscale('log')
    ax.set_title(f'Total hours per project in {YEAR}')
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    data = get_data_per_year(YEAR)

    # Total time per year
    time_per_year = 0
    for year, month_values in data.items():
        for month, days in month_values.items():
            for project, day_time in days.items():
                for day_number, minutes in day_time.items():
                    time_per_year += minutes
    print("Total hours:", time_per_year/60.0)

    # Total time per month
    time_per_month = {}
    for year, month_values in data.items():
        for month, days in month_values.items():
            for project, day_time in days.items():
                for day_number, minutes in day_time.items():
                    if month not in time_per_month:
                        time_per_month[month] = 0
                    time_per_month[month] += minutes
    print("Total hours per month:", {k:v/60.0 for k, v in time_per_month.items()})

    # Total time per project per year
    time_per_project = {}
    for year, month_values in data.items():
        for month, days in month_values.items():
            for project, day_time in days.items():
                if project not in time_per_project:
                    time_per_project[project] = 0
                for day_number, minutes in day_time.items():
                    time_per_project[project] += minutes
    print("Total per project:", {k:v/60.0 for k, v in time_per_project.items()})


    plot_time_per_month()
    plot_time_per_project()
