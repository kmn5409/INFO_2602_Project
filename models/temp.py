import csv
with open('../anime.csv', mode='r') as fp:
        csv_reader = csv.DictReader(fp)
        line_count = 0
        for row in csv_reader:
            #p = Anime()
            #p.fromJSON(row)
            '''
            if line_count == 0:
                print(row)
                print(row.keys())
            if(line_count > 40):
                print(row["name"])
            if(line_count == 50):
                break
            '''
	    if(line_count == 51):
		print(row)
            line_count+=1
            print(line_count)
