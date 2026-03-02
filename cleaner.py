import pandas as pd

class DataCleaner:

    @staticmethod
    def validate_schema(example_df: pd.DataFrame):
        if example_df.empty:
            raise ValueError("Example file cannot be empty")

        return list(example_df.columns)

    @staticmethod
    def create_doc_mon1(raw_df: pd.DataFrame):
        if "Doc_Mon1" not in raw_df.columns and "Doc_Month" in raw_df.columns:
            # Ensure string formatting
            raw_df["Doc_Month"] = raw_df["Doc_Month"].astype(str)

            # Extract first 5 characters
            raw_df["Doc_Mon1"] = raw_df["Doc_Month"].str[:5]

        return raw_df

    @staticmethod
    def align_to_template(example_df: pd.DataFrame, raw_df: pd.DataFrame):

        template_columns = DataCleaner.validate_schema(example_df)

        # Create Doc_Mon1 if needed
        raw_df = DataCleaner.create_doc_mon1(raw_df)

        # Add missing columns
        for col in template_columns:
            if col not in raw_df.columns:
                raw_df[col] = pd.NA

        # Remove extra columns (strict schema enforcement)
        raw_df = raw_df[template_columns]

        return raw_df