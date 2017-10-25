#Here we are loading the original csv files. Scraped every half-year
# at a time from RIAA website for efficiency purposes.

years = list(range(2017,1958,-1))
halftwo = [str(i) + '-06-01' for i in years]
halfone = [str(i) + '-01-01' for i in years]
dates = []
for i in range(0,len(halfone),1):
    dates.append(halftwo[i])
    dates.append(halfone[i])

riaa = pd.DataFrame(columns=['Artist', 'Title', 'Certification_Date', 'Label', 'Format_Type', 'Release_Date', 'Group_Type', 'Media_Type', 'Number_of_Units', 'Genre'])

for date in dates:
    csvname = ('riaa_' + date + '.csv')
    temp = pd.read_csv(csvname)
    riaa = riaa.append(temp)
    
riaa = riaa.rename(columns={'Number_of_Units': 'Certification_Type'}) # renaming a misleadingly named column
riaa = riaa.drop_duplicates(keep = 'first') # removing duplicates
riaa.set_index(np.arange(0,len(riaa),1), inplace = True) # setting numerical indices
riaa.to_csv('riaa_all.csv')