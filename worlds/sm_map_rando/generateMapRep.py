import os
import json

def parse(item):
        parts = item.split('-')
        return int(parts[0]), int(parts[1])

def write_file_list(directory_path, output_file_path):
    filenames = os.listdir(directory_path)
    filenames_without_extensions = [os.path.splitext(filename)[0] for filename in filenames]
    sorted_filenames = sorted(filenames_without_extensions, key=lambda x: parse(x))
    with open(output_file_path, 'w') as output_file:
        json.dump(sorted_filenames, output_file)

if __name__ == '__main__':
    # Set the directory path and output file path here
    directory_path_tame = '../MapRepositoryV117c_Standard'
    output_file_path_tame = 'worlds/sm_map_rando\data/mapRepositoryStandard.json'
    directory_path_wild = '../MapRepositoryV117c_Wild'
    output_file_path_wild = 'worlds/sm_map_rando\data/mapRepositoryWild.json'

    # Call the write_file_list function with the specified directory and output file paths
    write_file_list(directory_path_tame, output_file_path_tame)
    write_file_list(directory_path_wild, output_file_path_wild)