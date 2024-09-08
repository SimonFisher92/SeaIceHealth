import datetime

today = datetime.date.today()

root = "https://data.seaice.uni-bremen.de/amsr2/asi_daygrid_swath/n3125/"

months = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']

years = [ '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019',
         '2020', '2021', '2022', '2023', '2024']


def generate_links(root, months, years, today):
    possible_links = []

    for year in years:
        if year == '2012':
            start_month = 7
        else:
            start_month = 1

        for month in months[start_month - 1:]:
            link = f"{root}{year}/{month}/Arctic3125/"
            possible_links.append(link)

            # Stop when reaching the current month of the current year
            if year == str(today.year):
                if month == months[-1]:  # Stop at the last provided month in the list
                    break

    return possible_links

if __name__ == '__main__':
    links = generate_links(root, months, years, today)
    print(links)