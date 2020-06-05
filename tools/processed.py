import csv


class Processed:
    
    filepath = 'data/processed_companies.csv'
    
    @classmethod
    def update_csv(cls, option_identities, filepath=None):
        if not filepath:
            filepath = cls.filepath
        
        with open(filepath, 'a', newline='', encoding='utf-8') as oufile:
            writer = csv.writer(oufile, delimiter='|', 
                                quotechar='*', quoting=csv.QUOTE_MINIMAL)
            for opt, id_list in option_identities.items():
                writer.writerow([opt] + id_list)
    
    @classmethod
    def load_csv(cls, filepath=None):
        if not filepath:
            filepath = cls.filepath
        
        try:
            with open(filepath, 'r', encoding='utf-8') as infile:
                reader = csv.reader(infile, delimiter='|', quotechar='*')
                processed_companies = {key : id_list for key, *id_list in reader}
            return processed_companies
        except FileNotFoundError:
            print(f'Warning: "{filepath}" not found!')
            return {}
