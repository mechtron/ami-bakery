import hashlib
import os


def get_all_files_in_directory(directory):
    file_paths = []
    for path, _, files in os.walk(directory):
        for name in files:
            if name[0] is not '.':
                file_paths.append(os.path.join(path, name))
    return file_paths


def get_all_ami_files(ami_definition_directories):
    all_files = []
    for directory in ami_definition_directories:
        all_files.extend(get_all_files_in_directory(directory))
    return all_files


def get_file_sha1(path):
    blocksize = 65536
    hasher = hashlib.sha1()
    with open(path, 'rb') as afile:
        buf = afile.read(blocksize)
        while len(buf) > 0:
            hasher.update(buf)
            buf = afile.read(blocksize)
    return hasher.hexdigest()


def get_string_sha1(string):
    hash_object = hashlib.sha1(string.encode('utf-8'))
    return hash_object.hexdigest()


def calculate_ami_config_checksum(ami_definition_directories):
    ami_file_paths = get_all_ami_files(ami_definition_directories)
    ami_file_paths.sort()
    print('File paths sorted')
    file_sha1s = []
    for file_path in ami_file_paths:
        file_sha1 = get_file_sha1(file_path)
        print("AMI config file {path} has SHA1 {sha1}".format(
            path=file_path,
            sha1=file_sha1,
        ))
        file_sha1s.append(file_sha1)
    sha1s_concatenated = ''.join(file_sha1s)
    ami_config_checksum = get_string_sha1(sha1s_concatenated)
    print("AMI Config Checksum is {}".format(ami_config_checksum))
    return ami_config_checksum
