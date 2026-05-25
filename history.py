import pandas as pd
import os

FILE = "history.csv"


def save_history(data):

    new_df = pd.DataFrame([data])

    # If file exists, align columns safely
    if os.path.exists(FILE):

        try:
            old_df = pd.read_csv(FILE)

            # Merge columns
            combined_columns = list(
                set(old_df.columns).union(set(new_df.columns))
            )

            old_df = old_df.reindex(columns=combined_columns)
            new_df = new_df.reindex(columns=combined_columns)

            final_df = pd.concat([old_df, new_df], ignore_index=True)

        except:
            final_df = new_df

    else:
        final_df = new_df

    final_df.to_csv(FILE, index=False)


def load_history():

    if os.path.exists(FILE):

        try:
            return pd.read_csv(FILE)

        except:
            return pd.DataFrame()

    return pd.DataFrame()