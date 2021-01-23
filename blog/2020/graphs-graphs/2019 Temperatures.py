import matplotlib.pyplot as plt
import csv
import datetime as dt

data = []
with open("2019 Temperatures.csv") as csvfile:
    csvreader = csv.reader(csvfile, delimiter=',')
    for row in csvreader:
        data.append(row)

colordict = {'Brattleboro':'#880000', 
             'Exeter':'#771100', 
             'MIT':'#662200', 
             'Somerville':'#553300', 
             'Jaffrey':'#444400', 
             'Orlando':'#335500', 
             'Boston':'#226600',
             'Wolfeboro':'#117700',
             'London':'#008800',
             'Cambridge':'#007711',
             'Dubai':'#006622',
             'Bangkok':'#005533',
             'Hua Hin':'#004444',
             'Providence':'#003355',
             'DC':'#002266',
             'Philadelphia':'#001177',
             'New York':'#000088',
             'Monadnock':'#110077',
             'Cleveland':'#220066',
             'Chicago':'#330055',
             'Madison':'#440044',
             'Milwaukee':'#550033',
            }
def to_date(s):
    return dt.datetime.strptime(s, '%m/%d/%Y').date()
fig, axs = plt.subplots(2, 1, figsize=(16, 9))
data = data[1::]
for row in data:
    # Date, Type, Low, High, Rain, Snow
    day = to_date(row[0])
    axs[0].plot([day, day], [float(row[2]), float(row[3])], alpha=0.5, linewidth=2.5, color=colordict[row[1]])

date = [to_date(row[0]) for row in data]
rain = [(0 if row[4] == '' else float(row[4])) for row in data]
y_offset = [0 for row in data]
axs[1].bar(date, rain, bottom=y_offset, color='c')
snow = [(0 if row[5] == '' else float(row[5])) for row in data]
axs[1].bar(date, snow, bottom=rain, color='m')

fig.tight_layout()
fig.savefig("2019 Temperatures.png")
plt.show()