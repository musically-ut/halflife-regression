def add_filename_cols(df):
    """Adds some columns extracted from file-names, if they are present."""
    try:
        df['N'] = df.file.str.extract(r'N(\d+)', expand=True).astype(int)
    except:
        try:
            df['N'] = df.file.str.extract(r'(\d+)-bins', expand=True).astype(int)
        except:
            print('Column N could not be extracted.')

    try:
        df['h_reg'] = df.file.str.extract(r'(h_reg|hlwt)[-,]([^.]*\.[^.]+)', expand=True).iloc[:, 1].astype(float)
    except:
        print('Column h_reg could not be extracted.')

    try:
        df['l2wt'] = df.file.str.extract(r'l2wt[-,]([^.]*\.[^.]*)', expand=True).astype(float)
    except:
        print('Column l2wt could not be extracted.')

    try:
        df['seed'] = df.file.str.extract(r'(bootstrap|seed)[-,](\d+)', expand=True).iloc[:, 1].astype(float)
    except:
        print('Column seed could not be extracted.')


def find_best_by(measure, df, lower_is_better=False):
    """Find the rows in df which correspond to the best value by 'measure'."""
    groupby = df.groupby('N')[measure]
    idx = groupby.idxmax() if not lower_is_better else groupby.idxmin()
    return df.loc[idx]
