import json
import os


def get_path_files_path(source_path):
    path_list = [source_path]
    filepath_list = []
    for path in path_list:
        for p in os.listdir(path):
            full_path = os.path.join(path, p)
            if os.path.isdir(full_path):
                path_list.append(full_path)
            else:
                filepath_list.append(full_path)
    return filepath_list


def get_company_file_paths():
    root_path = r"D:\Data\Enterprise-Registration-Data\json"
    return get_path_files_path(root_path)


def get_companies_info():
    companies_info = list()
    file_path_list = get_company_file_paths()
    for path in file_path_list:
        with open(path, encoding="utf8")as f:
            read_line = f.readline()
            info = json.loads(read_line)
            for inf in info['erDataList']:
                companies_info.append(inf)
    return companies_info


if __name__ == '__main__':
    companies_info = get_companies_info()
    for inf in companies_info:
        print(inf)
