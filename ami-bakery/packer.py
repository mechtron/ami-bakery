import json
import os
import subprocess


def run_command(command, directory):
    proc = subprocess.Popen(
        command,
        shell=True,
        cwd=directory,
    )
    proc.wait()
    if proc.returncode is not 0:
        raise Exception(
            "Error running command! Exit code was {}".format(proc.returncode)
        )


def parse_packer_output_for_ami_id(base_dir):
    packer_output_path = "{}/.manifest.json".format(base_dir)
    with open(packer_output_path) as f:
        data = json.load(f)
        return data['builds'][-1]['artifact_id'].split(':')[1]


def get_packer_cwd():
    packer_cwd = os.path.dirname(get_packer_json_path())
    if not packer_cwd:
        packer_cwd = os.getcwd()
        print(
            "Warning: no Packer working directory specified - please use "
            "PACKER_CWD to specify one. Defaulting to {}.".format(packer_cwd)
        )
    return packer_cwd.strip()


def get_packer_json_path():
    return os.environ['PACKER_JSON_PATH'].strip()


def build_new_ami(ami_config_checksum):
    print('Building new AMI..')
    packer_build_command = (
        "packer build "
		"-var 'aws_region={aws_region}' "
		"-var 'aws_subnet_id={aws_subnet_id}' "
		"-var 'config_checksum={config_checksum}' "
        "{packer_json_path}"
    ).format(
        aws_region=os.environ['AWS_DEFAULT_REGION'],
        aws_subnet_id=os.environ['AWS_SUBNET_ID'],
        config_checksum=ami_config_checksum,
        packer_json_path=get_packer_json_path(),
    )
    print("Packer build command: {}".format(packer_build_command))
    packer_cwd = get_packer_cwd()
    run_command(packer_build_command, packer_cwd)
    new_ami_id = parse_packer_output_for_ami_id(packer_cwd)
    print("Ding! New AMI ID is {}".format(new_ami_id))
    return new_ami_id
