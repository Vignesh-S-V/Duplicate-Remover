import csv
import os

class DataCleaner:

    @staticmethod
    def process_csv(example_path, raw_path, output_path):
        # 1. Template columns-ai get panrom (Schema Validation)
        with open(example_path, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            template_columns = next(reader) # First row (header) mattum edukkirom
            if not template_columns:
                raise ValueError("Example file cannot be empty")

        # 2. Raw file-ai read panni, template-ku matharom
        with open(raw_path, 'r', encoding='utf-8') as f_in, \
             open(output_path, 'w', encoding='utf-8', newline='') as f_out:
            
            reader = csv.DictReader(f_in)
            writer = csv.DictWriter(f_out, fieldnames=template_columns)
            writer.writeheader()

            for row in reader:
                # Logic: Doc_Mon1 create panrom (Doc_Month-oda first 5 chars)
                if "Doc_Mon1" not in row and "Doc_Month" in row:
                    doc_month_val = str(row["Doc_Month"] or "")
                    row["Doc_Mon1"] = doc_month_val[:5]

                # Template-la illatha extra columns-ai filter panrom
                # Template-la irunthu missing-ana columns-ukku empty value tharom
                filtered_row = {col: row.get(col, "") for col in template_columns}
                
                writer.writerow(filtered_row)
        
        return output_path
