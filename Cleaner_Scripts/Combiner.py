import csv 
from datetime import date

# csv file name 
CDCfilename = "Clean_CDC.csv"
Homefilename = "Clean_Home_pattern.csv"
Visitsfilename = "Clean_Visits_Pattern.csv"
outputFileName = "Combined.csv"

# initializing the titles and rows list 
CDCfields = ["Date", "State" , "Total_cases", "Confirmed_cases", "New_cases",
             "Total_deaths", "Confirmed_death", "New_deaths"]
Homefields = ["Date", "State", "State_resident_number"]
Visitsfields = ["Month", "State", "State_visitor_number"]
Combinedfields = ["Date", "State" , "Total_cases", "Confirmed_cases",
                  "New_cases","Total_deaths", "Confirmed_death",
                  "New_deaths","State_resident_number", "State_visitor_number"]  
Monthdays = [0,31,29,31,30,31,30,31,31,30,31,30,31]
rows = []
# reading csv file 
with open(CDCfilename, 'r') as CDCcsvfile: 
    CDCcsvreader = csv.reader(CDCcsvfile) 
    next(CDCcsvreader) 
    with open(outputFileName,"w") as result:
        wtr= csv.writer( result )
        wtr.writerow( (Combinedfields) )
        for row in CDCcsvreader:
            year = row[0][6:10]
            day = row[0][3:5]
            month = row[0][0:2]
            state = row[1]
            curr_date = date(int(year), int(month), int(day))
            residentnum = -1
            visitnum = -1
            with open(Visitsfilename, 'r') as Visitcsvfile: 
                Visitcsvreader = csv.reader(Visitcsvfile) 
                next(Visitcsvreader)
                for visitrow in  Visitcsvreader:
                    if int(visitrow[0]) == int(month) and visitrow[1] == state:
                        visitnum = int(int(visitrow[2])/int(Monthdays[int(month)]))
                        break
            with open(Homefilename, 'r') as Homecsvfile: 
                Homecsvreader = csv.reader(Homecsvfile) 
                next(Homecsvreader)
                for Homerow in  Homecsvreader:
                    homeyear = year = Homerow[0][6:10]
                    homeday = Homerow[0][3:5]
                    homemonth = Homerow[0][0:2]
                    home_date = date(int(homeyear), int(homemonth), int(homeday))
                    difference = curr_date - home_date
                    if difference.days < 7 and difference.days > -1 and visitrow[1] == state:
                        residentnum = int(Homerow[2])
                        break
            wtr.writerow( (row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], residentnum, visitnum) )   
            print("Done: %d"%(CDCcsvreader.line_num)) 
    #print("Total no. of rows: %d"%(CDCcsvreader.line_num))
    #print (str(year) + "  " + str(month) + "  " + str(day) + "  " + str(visitnum) + "  " + str(state))
                        