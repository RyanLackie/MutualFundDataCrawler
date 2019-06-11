import sys
import csv
import xml.etree.ElementTree as tree
import util

# Get user input
user_input = input("Enter a CIK or ticker: ")

# If input isn't a CIK, convert it to a CIK
[company_name, CIK] = util.getCompanyNameAndCIK(user_input)

# Some cases for trouble with the CIK / Ticker
if not CIK or len(CIK) != 10:
    sys.exit("Could not find company from user input")

# Get the 13F-... form, form_name, and form_date
[xml, form_name, form_date] = util.get13F_Form(CIK)
if not xml:
    sys.exit("Could not find a 13F form")

# Write table of holdings to a file
filename = CIK + "_" + form_name + "_" + form_date + ".tsv"
file = open(filename, 'w')
file.write(company_name + "\t" + CIK + "\t" + form_name + "\t" + form_date + "\n")

# Parse through the xml
elementTree = tree.fromstring(xml)
# Open a csv writer with large tab sizes to add information into the file
# excel-tab will allow other software to read the information
writer = csv.writer(file, dialect='excel-tab')

# Field names
columns = []
for column in elementTree[0]:
    columns.append(column.tag.replace("{http://www.sec.gov/edgar/document/thirteenf/informationtable}", ""))
    # Columns may break into multiple parts
    for sub_column in column:
        columns.append(sub_column.tag.replace("{http://www.sec.gov/edgar/document/thirteenf/informationtable}", ""))

# Write fields into file
writer.writerow(columns)

# Parse through xml fields and write them into the file 1 row at a time
# I was unsure of the formatting of CSV files but I found some info on it online - I think this should be right
for element in elementTree:
    row = []
    for column in element:
        if "\n" not in column.text:
            row.append(column.text)
        else:
            row.append("")

        for sub_column in column:
            if "\n" not in sub_column.text:
                row.append(sub_column.text)
    writer.writerow(row)

# Close the file and the writer accessing it
file.close()

# Print an confirmation message that the process is complete
print(company_name + " " + form_name + " file writing complete")
