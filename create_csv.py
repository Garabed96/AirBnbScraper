import csv

HEADERS = ['timestamp', 'daterange', 'description of the airbnb', 'total price of the airbnb',
           'daily price of airbnb', 'property links', ]


class CsvManager:
    def __init__(self):
        pass


    def write_csv(self, timestamp, daterange,
                   description, total_price,
                   daily_price, links):
        with open("airbnb_rentals.csv", "w", encoding="UTF8") as file:
            writer = csv.writer(file)
            writer.writerow(HEADERS)

            # write the header - HEADERS
            # write a row of data
            for i in range(0, len(description)-1):
                row = (timestamp, daterange, description[i], total_price[i], daily_price[i], links[i])
                writer.writerow(row)



