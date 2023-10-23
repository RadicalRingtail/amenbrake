import os, hashlib

# contains generalized helper functions that are used in other scripts

def hash_file(input_file):
    with open(input_file, 'rb') as open_file:
        return hashlib.md5(open_file.read()).digest()   


def remove_dup_files(path):
    # removes all duplicate files in a given path

    files = []

    for f in os.listdir(path):
        full_path = os.path.join(path, f)
        file_hash = hash_file(full_path)

        if file_hash not in files:
            files.append(file_hash)
        else:
            os.remove(full_path)


class Common:
    # contains common methods used in other classses

    def set_data(self, data: dict):
            for key, tag in self.__dict__.items():
                if key in data.keys():
                    setattr(self, key, data[key])