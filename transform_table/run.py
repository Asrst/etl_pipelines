import pandas as pd
import datetime


def tableize(df):

    all_rows = []
    header_names = []
    grouped = df.groupby('pageid')
    for grp_key in grouped.groups.keys():
        grp_df = grouped.get_group(grp_key)
        # print(grp_key)

        # find missing columns
        missing_cols = set([0, 1, 2, 3]) - set(grp_df['columns'].values)
        add_rows = []
        for col in missing_cols:
            add_rows.append([pd.NA, pd.NA, pd.NA, pd.NA, pd.NA, col, pd.NA])

        # add missing rows
        grp_df = pd.concat([grp_df, (pd.DataFrame(add_rows, columns=grp_df.columns))])
        # sort by columns
        grp_df = grp_df.sort_values('columns')
        row_values = grp_df['stringvalue'].values

        for i in range(0, len(row_values)):
            if isinstance(row_values[i], str):
                if row_values[i].startswith("@@"):
                    row_values[i] = pd.NA
        all_rows.append(row_values)

        if grp_df['header'].unique()[0] == 1:
            header_names = row_values
            # print(header_names)


    if not len(header_names):
        header_names = range(len(all_rows[0]))

    df = pd.DataFrame(all_rows, columns=header_names)
    df = df.dropna(how="all")
    df["Header"] = df.index.values + 1

    return df


if __name__ == "__main__":
    df = pd.read_excel("python-test-1.xlsx")
    print(df.shape, df.columns)
    
    df_out = tableize(df)
    df_new = df_out[['(b) Identity of Issuer, Borrower, Lessor or Similar Party ', '(e) Current Value', 'Header']].copy()
    df_new.columns = ['entityname', 'amount', 'rowid']
    df_new['timestamp'] = datetime.datetime.now()
    df_new['othername'] = pd.NA
    df_new['uid'] = 10001

    df_new.to_csv("output.csv", index=False)
