import csv 

# csv file name 
filename = "Home_Pattern_Raw.csv"
outputFileName = "Clean_Home_pattern.csv"

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
    fields[2] = 'State'
    fields[4] = 'State_resident_number'

    with open(outputFileName,"w") as result:
        wtr= csv.writer( result )
        wtr.writerow( (fields[0], fields[2], fields[4]) )
        prevState = 'NONE'
        prevDate = 'NONE'
        cur_sum = 0
        for r in rows:
            r[0] = r[0][5:10].replace('-','/') + '/' + r[0][:4].replace('-','/')
            if prevState == str(r[2]) and prevDate == str(r[0]):
                cur_sum += int(r[4])
            elif str(r[4]) != 'number_devices_residing':
                r[2] = r[2].upper()
                if prevState is not 'NONE':
                    wtr.writerow( ( r[0], r[2], cur_sum) )
                cur_sum = int(r[4])
                prevState = r[2].lower()
                prevDate = r[0]

    print("Total no. of rows: %d"%(csvreader.line_num))