import matplotlib.pyplot as plt
import csv
import datetime as dt
import matplotlib.dates as mdates

data = []
with open("Sleep Cycles.csv") as csvfile:
    csvreader = csv.reader(csvfile, delimiter=',')
    for row in csvreader:
        data.append(row)

colordict = {2015:'#880000', 
             2016:'#444400', 
             2017:'#008800', 
             2018:'#004444', 
             2019:'#000088', 
             2020:'#440044', 
            }
def colorbyquarter(month):
    if month <= 3:
        return '#888800'
    elif month <= 6:
        return '#444400'
    elif month <= 9:
        return '#008800'
    elif month <= 12:
        return '#004444'
def to_date(s):
    return dt.datetime.strptime(s, '%m/%d/%Y').date()
def to_time(s):
    return dt.datetime.strptime(s, '%H:%M')

fig, axs = plt.subplots(2, 1, figsize=(16, 9))
data = data[1::]
date = []
length = []
sod = dt.datetime.strptime("00:00:00.000000", "%H:%M:%S.%f")
eod = dt.datetime.strptime("23:59:59.999999", "%H:%M:%S.%f")
for year_to_plot in range(2015, 2021):
    for row in data:
        # From, To, Date of To
        day = to_date(row[2])
        if (day.year != year_to_plot): continue

        if (row[0] == ''): continue
        time1 = to_time(row[0])

        if (row[1] == ''): continue
        time2 = to_time(row[1])

        if (time1 < time2):
            # same day
            axs[0].plot([day, day], [time1, time2], alpha=0.5, linewidth=2.5, color=colorbyquarter(day.month))
            date.append(day)
            length.append(time2 - time1)
        else:
            # different day
            prevday = day - dt.timedelta(days=1)
            axs[0].plot([prevday, prevday], [time1, eod], alpha=0.5, linewidth=2.5, color=colorbyquarter(day.month))
            axs[0].plot([day, day], [sod, time2], alpha=0.5, linewidth=2.5, color=colorbyquarter(day.month))
            date.append(day)
            length.append(time2 - sod + eod - time1)

    y_offset = [sod]*len(date)
    axs[1].bar(date, length, bottom=y_offset, color='c')

    myFmt = mdates.DateFormatter('%H:%M')
    axs[0].yaxis.set_major_formatter(myFmt)
    axs[1].yaxis.set_major_formatter(myFmt)

    fig.tight_layout()
    fig.savefig("Sleep Cycles" + str(year_to_plot) + ".png")
    plt.show()