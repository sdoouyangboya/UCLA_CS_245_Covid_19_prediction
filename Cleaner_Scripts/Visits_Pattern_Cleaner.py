import csv 

# csv file name 
filename = "Visits_Pattern_Raw.csv"
outputFileName = "Clean_Visits_Pattern.csv"

# initializing the titles and rows list 
fields = [] 
rows = [] 

# reading csv file 
with open(filename, 'r') as csvfile: 
    csvreader = csv.reader(csvfile) 
    fields = next(csvreader) 
    for row in csvreader:
        rows.append(row) 
    fields[1] = 'Month'
    fields[2] = 'State'
    fields[4] = 'State_visitor_number'

    with open(outputFileName,"w") as result:
        wtr= csv.writer( result )
        wtr.writerow( (fields[1], fields[2], fields[4]) )
        for r in rows:
            if str(r[2]) != 'ALL_STATES' and str(r[4]) != 'num_unique_visitors':
                r[2] = r[2].upper()
                wtr.writerow( ( r[1], r[2], r[4]) )

    print("Total no. of rows: %d"%(csvreader.line_num))