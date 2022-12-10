import os
import configure as c
import csv


def get_warning_info(path):
    warnings = []
    with open(path, 'r') as f:
        reader = csv.reader(f)
        index = 0
        for line in reader:
            if index == 0:
                index += 1
                continue
            path = line[c.index_map['path']]
            start = line[c.index_map['start']]
            end = line[c.index_map['end']]
            method = line[c.index_map['method']]
            field = line[c.index_map['field']]
            warnings.append({'index': index, 'path': path, 'start': start, 'end': end, 'method': method, 'field': field})
            index += 1
    f.close()

    return warnings


def location_warning(warnings: list, feature_list: list):
    location_list = []
    for warning in warnings:
        start = int(warning['start'])
        end = int(warning['end'])
        path = warning['path']
        method = warning['method']
        location_count = 0
        for i in warnings:
            if i['path'] == path and i['method'] == method:
                start_i = int(i['start'])
                end_i = int(i['end'])
                if start_i >= (start - c.offset) and end_i <= (end + c.offset):
                    location_count += 1
        location_list.append(location_count)

    for i in range(len(warnings)):
        feature_list[i]['location_count'] = location_list[i] - 1


def method_warning(warnings: list, feature_list: list):
    method_list = []
    for warning in warnings:
        method = warning['method']
        path = warning['path']
        method_count = 0
        for i in warnings:
            if i['path'] == path and i['method'] == method:
                method_count += 1
        method_list.append(method_count)

    for i in range(len(warnings)):
        feature_list[i]['method_count'] = method_list[i] - 1


def file_warning(warnings: list, feature_list: list):
    file_list = []
    for warning in warnings:
        path = warning['path']
        file_count = 0
        for i in warnings:
            if i['path'] == path:
                file_count += 1
        file_list.append(file_count)

    for i in range(len(warnings)):
        feature_list[i]['file_count'] = file_list[i] - 1


if __name__ == '__main__':
    pro_dirs = os.listdir(c.data_dir)
    for pro in pro_dirs:
        pro_path = os.path.join(c.data_dir, pro)
        if os.path.isdir(pro_path):
            path = os.path.join(pro_path, c.warning_file_name)
            warnings = get_warning_info(path)
            feature_list = []
            for i in range(len(warnings)):
                feature_list.append({})
            location_warning(warnings, feature_list)
            method_warning(warnings, feature_list)
            file_warning(warnings, feature_list)
            print(feature_list)
            with open(pro + '_new_feature.csv', 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['location_count', 'method_count', 'file_count'])
                for i in feature_list:
                    writer.writerow([i['location_count'], i['method_count'], i['file_count']])
            f.close()






