"""
This module contains functions for data processing, aggregation, and writing to Excel.

Functions:
- import_excel_file(filename, sheet_name)
- process_dataframe(df, search_string)
- update_headers(df, search_string)
- clean_data(df)
- aggregate_data(df, column_name, drop_rest)
- write_data_to_excel(output_path, dict_of_dfs)
- main()
"""

import numpy as np
import pandas as pd


def import_excel_file(filename, sheet_name):
    """
    Import an Excel file and return the specified sheet as a DataFrame.

    Parameters:
    filename (str): The name of the Excel file (without the extension).
    sheet_name (str): The name of the sheet to import.

    Returns:
    pandas.DataFrame: The imported sheet as a DataFrame.
    """
    file_path = (
        "Z:/14_Personal_Data/a.ramadani/Code/"
        f"01_2024_Aggregate_Attribution/input/{filename}.xlsx"
    )

    df = pd.read_excel(file_path, sheet_name=sheet_name, header=None)
    return df


def process_dataframe(df, search_string):
    """
    Process a dataframe by extracting a subset of rows starting from the row
    containing the specified search string.

    Args:
        df (pandas.DataFrame): The input dataframe.
        search_string (str): The string to search for in the
        first column of the dataframe.

    Returns:
        pandas.DataFrame: The processed dataframe with the subset of rows
        starting from the row containing the search string.
    """
    row_number = df.index[df.iloc[:, 0] == search_string].tolist()[0]
    new_header = df.iloc[row_number]
    df = df.iloc[row_number + 1 :]
    df.columns = new_header
    df.reset_index(drop=True, inplace=True)
    return df


def update_headers(df, search_string):
    """
    Updates the headers of a DataFrame by concatenating the previous
    header with the current header if the current header contains the
    specified search string.

    Args:
        df (pandas.DataFrame): The DataFrame whose headers need to be updated.
        search_string (str): The string to search for in the headers.

    Returns:
        pandas.DataFrame: The DataFrame with updated headers.
    """
    current_headers = df.columns.tolist()
    new_headers = []
    for index, header in enumerate(current_headers):
        if search_string in header:
            new_headers.append(current_headers[index - 1] + " " + df.columns[index])
        else:
            new_headers.append(header)
    df.columns = new_headers
    return df


def clean_data(df):
    """
    Cleans the given DataFrame by performing various data transformations.

    Args:
        df (pandas.DataFrame): The DataFrame to be cleaned.

    Returns:
        pandas.DataFrame: The cleaned DataFrame.
    """
    temp = {
        "Option Ticker": [
            "FIN SW",
            "SIK SW",
            "BEA SW",
            "UBSN SW",
            "GASN SW",
            "BAEN SW",
            "VAGN SW",
        ],
        "Stock Ticker": [
            "GF SW",
            "SIKA SW",
            "BEAN SW",
            "UBSG SW",
            "GALE SW",
            "BAER SW",
            "VACN SW",
        ],
    }
    ticker_map = pd.DataFrame(temp)

    def shorten_strings(value):
        """
        Shortens a string by removing intermediate words if
        the number of words is greater than 3.

        Args:
            value (str): The input string to be shortened.

        Returns:
            str: The shortened string.
        """
        words = value.split()
        if len(words) > 3:
            return " ".join(words[:2] + [words[-1]])
        return value

    def replace_strings_with_smi(df):
        """
        Replaces specific strings in the given DataFrame with 'SMI Index'.

        Args:
            df (pandas.DataFrame): The DataFrame to be modified.

        Returns:
            pandas.DataFrame: The modified DataFrame with replaced strings.
        """
        search_string = "SMI"
        overwrite_string = "SMI Index"
        mask = df["Bloomberg Ticker"].str.contains(search_string, na=False)
        df.loc[mask, "Bloomberg Ticker"] = overwrite_string
        mask = df["Descrizione Titolo"].str.contains(search_string, na=False)
        df.loc[mask, "Descrizione Titolo"] = overwrite_string
        df.loc[
            df["Bloomberg Ticker"].str.contains("SMI Index"), "Descrizione GICS 1"
        ] = "SMI Index"
        df.loc[
            df["Bloomberg Ticker"].str.contains("SMI Index"), "Descrizione GICS 2"
        ] = "SMI Index"
        return df

    def correct_option_ticker(df, ticker_map):
        """
        Corrects the option ticker in the given DataFrame based
        on the provided ticker map.

        Parameters:
        df (pandas.DataFrame): The DataFrame containing the data.
        ticker_map (pandas.DataFrame): The DataFrame containing
        the mapping of old option tickers to new stock tickers.

        Returns:
        pandas.DataFrame: The DataFrame with corrected option tickers.
        """
        for _, row in ticker_map.iterrows():
            old_string = row["Option Ticker"]
            new_string = row["Stock Ticker"]
            df["Bloomberg Ticker"] = df["Bloomberg Ticker"].str.replace(
                old_string, new_string
            )
        return df

    df = df.loc[
        :,
        [
            "Bloomberg Ticker",
            "Descrizione Titolo",
            "P/L Tot %",
            "Peso Iniziale",
            "Peso Finale",
            "Descrizione GICS 1",
            "Descrizione GICS 2",
            "DOMICILE",
        ],
    ]
    df = df.dropna(subset=["Bloomberg Ticker"])
    df.iloc[:, 0] = df.iloc[:, 0].apply(shorten_strings)
    df = replace_strings_with_smi(df)
    df = correct_option_ticker(df, ticker_map)
    df = df.fillna(0)
    return df


def aggregate_data(df, column_name, drop_rest):
    """
    Aggregate data based on a specified column name.

    Parameters:
    - df: pandas.DataFrame
        The input DataFrame.
    - column_name: str
        The column name to group by.
    - drop_rest: bool
        Whether to drop the rest of the columns or not.

    Returns:
    - df: pandas.DataFrame
        The aggregated DataFrame.
    """
    numeric_columns = df.select_dtypes(include=np.number).columns
    if drop_rest:
        df = df.groupby(column_name, as_index=False)[numeric_columns].sum()

    df[numeric_columns] = df.groupby(column_name)[numeric_columns].transform("sum")
    df = df.drop_duplicates(subset=df.columns[0])
    return df


def write_data_to_excel(output_path, dict_of_dfs):
    """
    Write multiple DataFrames to separate sheets in an Excel file.

    Parameters:
        output_path (str): The path to save the Excel file.
        dict_of_dfs (dict): A dictionary containing DataFrame objects,
        where the keys are the sheet names.

    Returns:
        None
    """
    writer = pd.ExcelWriter(  # pylint: disable=abstract-class-instantiated
        output_path, engine="xlsxwriter"
    )

    # Write each DataFrame to a separate sheet with sheet names based on DataFrame names
    for df_name, df in dict_of_dfs.items():
        df.to_excel(writer, sheet_name=df_name.split("_")[1], index=False)

    # Save the Excel file
    writer.close()


def main():
    """
    Main function that performs the data processing and aggregation.

    This function loads data from an Excel file, processes the data, updates headers,
    cleans the data, aggregates the data based on different columns, and writes the
    aggregated data to an Excel file.

    Returns:
        None
    """
    # Load data
    df = import_excel_file("input", "RIEPILOGO")

    # Process data
    df = process_dataframe(df, "Cod Tit")

    # Update headers
    df = update_headers(df, "%")

    # Clean data
    df = clean_data(df)

    # Aggregate data
    dict_of_dfs = {}

    dict_of_dfs["df_stock"] = aggregate_data(df, "Bloomberg Ticker", drop_rest=False)
    dict_of_dfs["df_gics1"] = aggregate_data(
        dict_of_dfs["df_stock"], "Descrizione GICS 1", drop_rest=True
    )
    dict_of_dfs["df_gics2"] = aggregate_data(
        dict_of_dfs["df_stock"], "Descrizione GICS 2", drop_rest=True
    )
    dict_of_dfs["df_region"] = aggregate_data(
        dict_of_dfs["df_stock"], "DOMICILE", drop_rest=True
    )

    # Create a Pandas Excel writer using the file path
    output_path = (
        r"Z:\14_Personal_Data\a.ramadani\Code"
        r"\01_2024_Aggregate_Attribution\output\output_file.xlsx"
    )
    write_data_to_excel(output_path, dict_of_dfs)


if __name__ == "__main__":
    main()
