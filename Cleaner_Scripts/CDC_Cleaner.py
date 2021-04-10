import csv 

# csv file name 
filename = "starting_File.csv"
outputFileName = "Clean_CDC.csv"

# initializing the titles and rows list 
fields = [] 
rows = [] 

# reading csv file 
with open(filename, 'r') as csvfile: 
    csvreader = csv.reader(csvfile) 
    fields = next(csvreader) 
    for row in csvreader:
        rows.append(row) 
    fields[0] = 'Date'
    fields[1] = 'State'
    fields[2] = 'Total_cases'
    fields[3] = 'Confirmed_cases'
    fields[5] = 'New_cases'
    fields[7] = 'Total_deaths'
    fields[8] = 'Confirmed_death'
    fields[10] = 'New_deaths'

    with open(outputFileName,"w") as result:
        wtr= csv.writer( result )
        wtr.writerow( (fields[0], fields[1], fields[2], fields[3], fields[5], fields[7], fields[8], fields[10]) )
        for r in rows:
            wtr.writerow( (r[0] if r[0] else 0, r[1] if r[1] else 0, r[2] if r[2] else 0, r[3] if r[3] else 0, r[5] if r[5] else 0, r[7] if r[7] else 0, r[8] if r[8] else 0, r[10] if r[10] else 0) )

    print("Total no. of rows: %d"%(csvreader.line_num))