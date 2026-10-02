from pathlib import Path
import csv

class DataExtractor:
    """Access and extracts weevil names."""
    def __init__(self):
        pass

    def acces_document(self):
        self.path = Path("data/nameusage.csv")
        self.lines = self.path.read_text().splitlines()

        # attention à structure du document !
        # ici, colones délimitées par ";"
        self.reader = csv.reader(self.lines, delimiter=";")
        self.header_row = next(self.reader)

        # Get names ID
        # fonction dédiée ?
        self.names_id = self.header_row.index("col:scientificName")

    def extract_data(self):
        self.weevil_names = []
        for row in self.reader:
            try:
                name = str(row[self.names_id])
            except ValueError:
                print("The data couldn't be accessed.")
                continue
            else:
                self.weevil_names.append(name)
        return self.weevil_names

    def write_data(self):
        """Writes weevil names in weevil_names.txt"""
        with open("weevil_names.txt", "w+", encoding="utf-8") as t:
            for name in sorted(self.weevil_names):
                t.write("%s\n" %name)

data = DataExtractor()
data.acces_document()
data.extract_data()
data.write_data()