import csv
import os
from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
    help = 'Update odgovori.csv with IDs based on pitanja.csv'

    def add_arguments(self, parser):
        parser.add_argument('directory', type=str, help='Path to the directory')

    def handle(self, *args, **kwargs):
        directory = kwargs['directory']

        pitanja_path = os.path.join(directory, 'pitanja.csv')
        odgovori_path = os.path.join(directory, 'odgovori.csv')

        if not os.path.exists(pitanja_path):
            raise CommandError(f"File pitanja.csv not found in {directory}")

        if not os.path.exists(odgovori_path):
            raise CommandError(f"File odgovori.csv not found in {directory}")

        # Read pitanja.csv and create a mapping of Pitanje to ID
        pitanje_to_id = {}
        with open(pitanja_path, mode='r', encoding='utf-8') as pitanja_file:
            reader = csv.DictReader(pitanja_file)
            if 'Pitanje' not in reader.fieldnames or 'ID' not in reader.fieldnames:
                raise CommandError("pitanja.csv must contain 'Pitanje' and 'ID' columns")

            for row in reader:
                pitanje_to_id[row['Pitanje']] = row['ID']

        # Read odgovori.csv, add ID column if missing, and populate it
        updated_rows = []
        with open(odgovori_path, mode='r', encoding='utf-8') as odgovori_file:
            reader = csv.DictReader(odgovori_file)
            fieldnames = reader.fieldnames

            if 'Pitanje' not in fieldnames:
                raise CommandError("odgovori.csv must contain 'Pitanje' column")

            if 'ID' not in fieldnames:
                fieldnames.append('ID')

            for row in reader:
                pitanje = row['Pitanje']
                row['ID'] = pitanje_to_id.get(pitanje, '')  # Add ID or empty string if not found
                updated_rows.append(row)

        # Write the updated rows back to odgovori.csv
        with open(odgovori_path, mode='w', encoding='utf-8', newline='') as odgovori_file:
            writer = csv.DictWriter(odgovori_file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(updated_rows)

        self.stdout.write(self.style.SUCCESS(f"Updated {odgovori_path} successfully."))
