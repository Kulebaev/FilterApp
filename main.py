import csv
from datetime import datetime
import time


MONTH_DICT = {
    'января': '01',
    'февраля': '02',
    'марта': '03',
    'апреля': '04',
    'мая': '05',
    'июня': '06',
    'июля': '07',
    'августа': '08',
    'сентября': '09',
    'октября': '10',
    'ноября': '11',
    'декабря': '12'
}

def read_csv_file(file_path):
    with open(file_path, 'r', encoding='windows-1251') as csvfile:
        reader =  csv.reader(csvfile, delimiter=';')
        header = next(reader)
        data = list(reader)

        
    for row in data:
            for month_name, month_num in MONTH_DICT.items():
                # Преобразование времени в правильный формат
                row[1] = row[1].replace(month_name, month_num)

            # row[1] = datetime.strptime(row[1], '%d %m %Y  %H:%M:%S.%f')

    return header, data


def write_csv_file(file_path, header, data):
    with open(file_path, 'w', encoding='windows-1251', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(header)
        writer.writerows(data)


def filter_data(input_data, start_time, end_time, aperture):
    filtered_rows = []
    prev_row = None

    for row in input_data:
        row_time = datetime.strptime(row[1], '%d %m %Y г. %H:%M:%S.%f мсек')
        # print(row_time)
        if start_time <= row_time <= end_time:
            # print(start_time, end_time, row_time)
            if prev_row is not None:
                param_changed = False
                for prev_val, current_val in zip(prev_row[2:], row[2:]):

                    prev_val = float(prev_val.replace(',', '.'))
                    current_val = float(current_val.replace(',', '.'))

                    if abs(float(current_val) - float(prev_val)) > aperture:
                        param_changed = True
                        break
                if param_changed:
                    filtered_rows.append(row)
            prev_row = row

    return filtered_rows

if __name__ == "__main__":
    input_file_path = 'test_input.csv'
    output_file_path = 'test_output.csv'

    start_time = datetime(2021, 8, 18, 10, 0, 0)
    end_time = datetime(2023, 12, 31, 23, 59, 59)
    aperture = 100

    header, data = read_csv_file(input_file_path)

    start = time.time()
    filtered_data = filter_data(data, start_time, end_time, aperture)
    end = time.time()

    write_csv_file(output_file_path, header, filtered_data)

    print(f"Отфильтровано {len(filtered_data)} строк за {end - start:.4f} секунд.")
