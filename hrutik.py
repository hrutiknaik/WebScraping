"***********************************WEB-SCRAPING CODE*************************************"

import requests
import os
import matplotlib.pyplot as plt
import csv
from bs4 import BeautifulSoup


def district(college):
    data = {'Amravati': '1', 'Aurangabad': '2', 'Mumbai': '3', 'Nagpur': '4', 'Nashik': '5', 'Pune': '6'}
    url = 'http://www.dtemaharashtra.gov.in/frmInstituteList.aspx?RegionID=' + data[college] + '&RegionName=' + college
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    if (response.status_code != 200):
        print("Website cannot be found.")
        return False
    print(college, 'district data of colleges is being scraped \n')
    soup = BeautifulSoup(response.content, 'html.parser')
    stat_table = soup.find_all('table', class_='DataGrid')
    stat_table = stat_table[0]
    count = 0
    with open('op.txt', 'w') as r:
        for row in stat_table.find_all('tr'):
            z = []
            for cell in row.find_all('td'):
                z.append(cell.text)

            if (len(z) < 2):
                continue

            elif ('technical' in z[2].lower() or 'engineering' in z[2].lower() or 'technological' in z[
                2].lower() or 'institute of technology' in z[2].lower()):
                r.write("    ".join(z))
                r.write('\n')
                count += 1

    return True


def university(code):
    url = 'http://dtemaharashtra.gov.in/frmInstituteSummary.aspx?InstituteCode=' + str(code)
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    if (response.status_code != 200):
        return False
    else:
        soup = BeautifulSoup(response.content, 'html.parser')
        stat_table = soup.find_all('table', class_='AppFormTable')

        stat_table = stat_table[0]
        with open('op1.txt', 'w') as r:
            for row in stat_table.find_all('tr'):
                for cell in row.find_all('td'):
                    r.write(cell.text.ljust(28))
                r.write('\n')
        file1 = open('op1.txt', 'r')
        Lines = file1.readlines()
        output = ['NULL'] * 11
        flag = 0
        for line in Lines:
            h = list(map(str, line.split()))

            if (len(h) == 2 and h[1] == "Code"):
                return False
            if (len(h) < 3):
                pass

            elif (h[1] == "Code"):
                output[0] = h[2]
            elif (h[1] == "Name"):
                output[1] = ' '.join(h[2:])
            elif (h[0] == "Address"):
                output[2] = ' '.join(h[1:])
            elif (h[0] == 'E-Mail'):
                output[3] = h[2]
            elif (h[0] == 'District'):
                output[4] = ' '.join(h[1:2])
            elif (h[0] == 'Name' and flag == 0):
                output[5] = ' '.join(h[1:])
                flag = 1

            elif (h[0] == "Office"):
                j = 0
                for i in range(len(h)):
                    if (j != 1 and h[i].isdigit() and len(h[i]) > 5):
                        output[6] = h[i]
                        j = 1
                    elif (j == 1 and h[i].isdigit() and len(h[i]) > 5):
                        output[7] = h[i]

            elif (h[0] == 'Name' and flag == 1):
                output[8] = ' '.join(h[1:])
            elif (h[0] == 'Status'):
                for i in range(len(h)):
                    if (h[i] == 'Autonomy'):
                        output[9] = h[i + 2]
                        break
            elif (h[0] == 'Year'):
                output[10] = h[3]
        return output


def college_info(college_region):
    if (district(college_region)):

        no_of_college = 1
        with open('op.txt', 'r') as f:
            for line in f:
                sh = list(map(str, line.split()))
                if (len(sh) < 3):
                    pass
                elif (no_of_college > 180):
                    return
                elif (sh[0].isdigit() and sh[1].isdigit() and len(sh) > 2):
                    o = university(sh[1])
                    f = open('op2.txt', 'a+', newline='')
                    f.write('$'.join(o))
                    f.write('\n')
                    f.close()
                    no_of_college += 1

        return
    else:
        return None


f = open('op2.txt', 'w+', newline='')
f.close()
print('\nWebsite Is Being Scraped \n')
college_info("Amravati")
college_info("Aurangabad")
college_info("Mumbai")
college_info("Nagpur")
college_info("Nashik")
college_info("Pune")
print("CSV is getting ready")

with open('Colleges.csv', 'w', newline='') as f1:
    fieldnames = ['Sr.No', 'College_Code', 'Institue_Name', 'Address', 'Email', 'District', 'Principal_Name',
                  'Office_No', 'Personal_No', 'TPO_Name', 'Autonomy_Status', 'Year_of_Establishment']
    thewriter = csv.DictWriter(f1, fieldnames=fieldnames)
    thewriter.writeheader()
    f1.close()

no_of_college = 1
file = open('op2.txt', 'r')
for f in file:
    o = list(map(str, f.split('$')))
    if (o[0] != 'NULL' and o[1] != 'NULL' and o[2] != 'NULL' and o[3] != 'NULL' and o[4] != 'NULL' and o[
        5] != 'NULL' and o[6] != 'NULL' and o[7] != 'NULL' and o[8] != 'NULL' and o[9] != 'NULL' and o[10] != 'NULL'):
        with open('Colleges.csv', 'a', newline='') as f1:
            fieldnames = ['Sr.No', 'College_Code', 'Institue_Name', 'Address', 'Email', 'District', 'Principal_Name',
                          'Office_No', 'Personal_No', 'TPO_Name', 'Autonomy_Status', 'Year_of_Establishment']
            thewriter = csv.DictWriter(f1, fieldnames=fieldnames)
            thewriter.writerow(
                {'Sr.No': no_of_college, 'College_Code': int(o[0]), 'Institue_Name': o[1], 'Address': o[2],
                 'Email': o[3], 'District': o[4], 'Principal_Name': o[5], 'Office_No': int(o[6]),
                 'Personal_No': int(o[7]), 'TPO_Name': o[8], 'Autonomy_Status': o[9],
                 'Year_of_Establishment': int(o[10])})
            f1.close()
            no_of_college += 1
file.close()
os.remove('op.txt')
os.remove('op1.txt')
os.remove('op2.txt')
print("Information is Scraped Sucessfully.")


"************************************ Visualisation Code*************************************"

x = []
y = []
year = []

with open('Colleges.csv', 'r') as csvfile:
    plots = csv.reader(csvfile, delimiter=',')
    for row in plots:
        y.append(row[5])
        x.append(row[10])
        year.append(row[11])

x.pop(0)
y.pop(0)
year.pop(0)

plt.scatter(y, x, 90, marker='o', color='yellow')

plt.title('District vs Autonomy_Status (Whose all details are fetched completly)')

plt.ylabel('Autonomy Status')
plt.xlabel('District')
plt.xticks(rotation='vertical')
plt.show()

l = sorted(list(set(y)))
r = []
for i in l:
    r.append(y.count(i))

k = dict.fromkeys(list(set(y)), 0)
for i, j in k.items():
    k[i] = y.count(i)

plt.bar(l, r, .35, color='red')
plt.title('District vs No of colleges (whose all details are fetched completly)')
plt.ylabel('No of colleges')
plt.xlabel('District')
plt.xticks(rotation='vertical')
plt.show()



