# Class used to parse AWS's "credentials.csv".
import csv


class CredentialsParser:

    def __init__(self, filename):
        self.dictionary = self.parse_csv(filename)

    @classmethod
    def parse_csv(cls, filename):
        if type(filename) != str:
            raise ValueError("Input must be a string")

        credentials = {}

        try:
            with open(filename, mode='r') as csv_file:
                csv_reader = csv.DictReader(csv_file)
                line_count = 0
                for row in csv_reader:
                    if line_count == 0:
                        print(f'Column names are {", ".join(row)}')
                        line_count += 1
                    username = row.pop("User name")
                    credentials[username] = row
                    line_count += 1
                print(f' {line_count} lines.')
        except:
            raise TypeError("%s must be a csv file" % filename)

        return credentials

    def get(self, key):
        return self.dictionary.get(key,None)
