import csv

from fedex_country_codes import FEDEX_COUNTRY_CODES

class RuleGenerator():
    def __init__(self, zones_csv, rates_csv, shipping_type, title):
        self.zones_csv = zones_csv
        self.rates_csv = rates_csv
        self.shipping_type = shipping_type
        self.title = title

    def generate(self):
        self.parse_zones()
        self.rules = self.generate_rules()
        return self.rules

    def parse_zones(self):
        """ Parses the zone csv and saves as self.zones """
        self.zones = {}
        with open(self.zones_csv, 'r') as zones_csv_file:
            dialect = csv.Sniffer().sniff(zones_csv_file.read(1024))
            zones_csv_file.seek(0)
            reader = csv.reader(zones_csv_file, dialect)
            is_header = True
            for row in reader:
                if is_header:
                    is_header = False
                    continue
                country = row[0].strip()
                zone = row[1]
                if zone not in self.zones:
                    self.zones[zone] = [country]
                else:
                    self.zones[zone].append(country)

    def generate_rules(self):
        """ Returns a list of dictionaries, each one describing a rule to be created """
        rules = []

        with open(self.rates_csv, 'r') as rates_csv_file:
            dialect = csv.Sniffer().sniff(rates_csv_file.read(1024))
            rates_csv_file.seek(0)
            reader = csv.reader(rates_csv_file, dialect)

            headers_map = {}
            min_weight = 0
            row_number = 0

            # process each row separately
            for row in reader:

                # save the headers map {header_name: column_number, ... } 
                if row_number == 0:
                    for col_number in range(0, len(row)):
                        headers_map[col_number] = row[col_number]
                    row_number = row_number + 1
                    continue

                # process each column separately
                for col_number in range(0, len(row)):
                    # extract the weight
                    if col_number == 0:
                        max_weight = row[col_number]
                        continue

                    # get the zone name and code
                    zone = headers_map[col_number]
                    zone_countries = dict.fromkeys(self.zones[zone])

                    for country in zone_countries:
                        zone_countries[country] = FEDEX_COUNTRY_CODES.get(country, None)
                        if zone_countries[country] == None:
                            raise Exception('Could not find country code for country: ' + country)

                    # construct name
                    name = "%(shipping_type)s %(min_weight)s kg - %(max_weight)s kg Zone %(zone)s" % \
                                {"shipping_type": self.shipping_type, "min_weight": min_weight, "max_weight": max_weight, "zone": zone}

                    # construct serialized list of country codes
                    rule_data = {
                        "name": name,
                        "title": self.title,
                        "min_price": row[col_number],
                        "max_price": row[col_number],
                        "min_weight": min_weight,
                        "max_weight": max_weight,
                        "countries": zone_countries,
                        "id": zone + str(row[col_number]) + str(row[col_number]) + str(min_weight) + str(max_weight),
                    }

                    rules.append(rule_data)

                # cache the weight for the next row
                min_weight = max_weight

            # increment row number
            row_number = row_number + 1

        # return
        return rules
