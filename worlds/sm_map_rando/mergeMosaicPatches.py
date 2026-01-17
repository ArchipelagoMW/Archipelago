import os
import json

def create_big_file(input_dir, output_file, index_file):
    index = {}
    offset = 0
    with open(output_file, 'wb') as big_file:
        file_list = os.listdir(input_dir)
        file_list.sort()
        for filename in file_list:
            file_path = os.path.join(input_dir, filename)
            with open(file_path, 'rb') as file:
                data = file.read()
                big_file.write(data)
                index[filename] = {'offset': offset, 'size': len(data)}
                offset += len(data)
    
    with open(index_file, 'w') as index_file:
        json.dump(index, index_file)

if __name__ == '__main__':  
    create_big_file('data\patches\mosaic', 'mosaic_patches.data', 'mosaic_patches_map.json')