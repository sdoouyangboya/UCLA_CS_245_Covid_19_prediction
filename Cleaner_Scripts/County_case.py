import csv 

# csv file name 
filename = "us-counties.csv"
outputFileName = "Clean_us-counties.csv"

# initializing the titles and rows list 
fields = [] 
rows = [] 

# states to two letter code
us_state_abbrev = {
    'Alabama': 'AL',
    'Alaska': 'AK',
    'American Samoa': 'AS',
    'Arizona': 'AZ',
    'Arkansas': 'AR',
    'California': 'CA',
    'Colorado': 'CO',
    'Connecticut': 'CT',
    'Delaware': 'DE',
    'District of Columbia': 'DC',
    'Florida': 'FL',
    'Georgia': 'GA',
    'Guam': 'GU',
    'Hawaii': 'HI',
    'Idaho': 'ID',
    'Illinois': 'IL',
    'Indiana': 'IN',
    'Iowa': 'IA',
    'Kansas': 'KS',
    'Kentucky': 'KY',
    'Louisiana': 'LA',
    'Maine': 'ME',
    'Maryland': 'MD',
    'Massachusetts': 'MA',
    'Michigan': 'MI',
    'Minnesota': 'MN',
    'Mississippi': 'MS',
    'Missouri': 'MO',
    'Montana': 'MT',
    'Nebraska': 'NE',
    'Nevada': 'NV',
    'New Hampshire': 'NH',
    'New Jersey': 'NJ',
    'New Mexico': 'NM',
    'New York': 'NY',
    'North Carolina': 'NC',
    'North Dakota': 'ND',
    'Northern Mariana Islands':'MP',
    'Ohio': 'OH',
    'Oklahoma': 'OK',
    'Oregon': 'OR',
    'Pennsylvania': 'PA',
    'Puerto Rico': 'PR',
    'Rhode Island': 'RI',
    'South Carolina': 'SC',
    'South Dakota': 'SD',
    'Tennessee': 'TN',
    'Texas': 'TX',
    'Utah': 'UT',
    'Vermont': 'VT',
    'Virgin Islands': 'VI',
    'Virginia': 'VA',
    'Washington': 'WA',
    'West Virginia': 'WV',
    'Wisconsin': 'WI',
    'Wyoming': 'WY'
}

# reading csv file 
with open(filename, 'r') as csvfile: 
    csvreader = csv.reader(csvfile) 
    fields = next(csvreader) 
    for row in csvreader:
        rows.append(row) 
    fields[0] = 'Date'
    fields[1] = 'State'
    fields[2] = 'County_Name'
    fields[3] = 'County_Fips'
    fields[4] = 'Cases'
    fields[5] = 'Deaths'

    with open(outputFileName,"w") as result:
        wtr= csv.writer( result )
        wtr.writerow( (fields[0], fields[1], fields[2], fields[3], fields[4], fields[5]) )
        for r in rows:
            year = r[0][0:4]
            day = r[0][8:10]
            month = r[0][5:7]
            date = str(month) + '/' + str(day) + '/' + str(year)
            state = us_state_abbrev[r[2]].upper()
            
            wtr.writerow( (date, state, r[1], r[3], r[4], r[5]) )

    print("Total no. of rows: %d"%(csvreader.line_num))