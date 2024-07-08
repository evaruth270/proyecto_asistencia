import pandas as pd

def load_data(filepath='attendance_database.xlsx'):
    try:
        return pd.read_excel(filepath, index_col=0)
    except FileNotFoundError:
        return pd.DataFrame(columns=['StudentName', 'StudentID', 'Course', 'Date', 'AttendanceStatus'])

def save_data(data, filepath='attendance_database.xlsx'):
    data.to_excel(filepath, index=False)

def add_record(df, record):
    return df.append(record, ignore_index=True)

