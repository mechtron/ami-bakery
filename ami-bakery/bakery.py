#!/usr/bin/env python3
import json
import os

import boto3


from checksum import calculate_ami_config_checksum
from packer import (
    build_new_ami,
    get_packer_json_path,
)


def lookup_ami_by_config_checksum(config_checksum):
    print('Looking up AMI Config Checksum..')
    ec2_client = boto3.client('ec2')
    response = ec2_client.describe_images(
        Filters=[
            {
                'Name': 'tag:ami_config_checksum',
                'Values': [
                    config_checksum,
                ]
            },
        ],
    )
    if len(response['Images']) == 0:
        print('AMI Config Checksum does not exist!')
        return None
    most_recent_image = response['Images'][0]
    for image in response['Images']:
        if image['CreationDate'] > most_recent_image['CreationDate']:
            most_recent_image = image
    print("Most recent AMI ID: {}".format(most_recent_image['ImageId']))
    return most_recent_image['ImageId']


def parse_config_directories():
    def_dirs_raw = os.environ.get('AMI_DEFINITION_DIRS', None)
    if not def_dirs_raw:
        raise Exception(
            'Sorry, required environment variable '
            'AMI_DEFINITION_DIRS is not defined.'
        )
    if ',' not in def_dirs_raw:
        return [def_dirs_raw.strip()]
    return_dirs = []
    for def_dir in def_dirs_raw.split(','):
        if def_dir[0] is '.':
            raise ValueError(
                'Sorry, all AMI definition paths must be absolute'
            )
        return_dirs.append(def_dir.strip())
        print("AMI configuration directory added: {}".format(def_dir.strip()))
    return return_dirs


def disable_output_buffer():
    os.environ['PYTHONUNBUFFERED'] = '1'


def output_ami_id_file(ami_id):
    packer_json_parent_dir = os.path.dirname(get_packer_json_path())
    if not packer_json_parent_dir:
        packer_json_parent_dir = os.getcwd()
    output_path = "{}/.ami_id.json".format(packer_json_parent_dir)
    with open(output_path, 'w') as outfile:
        print("AMI ID output path: {}".format(output_path))
        json.dump(dict(ami_id=ami_id), outfile)


def main():
    disable_output_buffer()
    ami_definition_directories = parse_config_directories()
    ami_config_checksum = calculate_ami_config_checksum(ami_definition_directories)
    ami_id = lookup_ami_by_config_checksum(ami_config_checksum)
    if not ami_id:
        ami_id = build_new_ami(ami_config_checksum)
    output_ami_id_file(ami_id)


if __name__ == '__main__':
    main()
