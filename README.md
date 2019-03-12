# GumGum AMI Bakery (Public Edition)

By Corey Gale (corey@gumgum.com)

## Project Goals

1. Automated, idempotent AMI builds with [Packer](https://www.packer.io/) 
    AMIs are only re-built when their definition changes
1. CI-friendly solution

## Project Overview

To learn more about the GumGum AMI Bakery, checkout [our slideshow](https://slides.com/coreygale/ami-bakery/)!

## Usage

Docker image: `docker pull docker.io/mechtron/ami-bakery`

To use the GumGum AMI Bakery in your CI environment, see the following configuration options:

#### Environment variables

To specify where the ephemeral Packer instance is launched:

- `AWS_DEFAULT_REGION`
- `AWS_SUBNET_ID`

To specify the AMI configuration files:

- `PACKER_JSON_PATH`: path to the Packer JSON file
- `AMI_DEFINITION_DIRS`: comma-separated list of directories containing the AMI's configuration code

#### Example

```
docker run --rm -t \
    -e AWS_DEFAULT_REGION=$AWS_DEFAULT_REGION \
    -e AWS_SUBNET_ID=$AWS_SUBNET_ID \
    -e PACKER_JSON_PATH=`pwd`/example-app/ami/packer/ami.json \
    -e AMI_DEFINITION_DIRS=`pwd`/example-app/ami/ \
    --mount type=bind,source=`pwd`,target=`pwd` \
    --mount type=bind,source=$HOME/.aws/,target=/root/.aws \
    docker.io/mechtron/ami-bakery:latest
```

#### Getting the AMI ID

In addition to the build's `stdout`, the new AMI ID is also outputted to the file `.ami_id.json`. Here's an example of the contents of that file:

    {"ami_id": "ami-0d8ebf1e938f7f16e"}

##### Grab the AMI ID from Bash

    cat .ami_id.json | jq .ami_id

### Implementation Details

##### AMI Config Checksum Algorithm

To compute the desired "AMI Config Checksum" within the "Build AMI" container:

2.  Within the service's repository, get a list of all files contained in the AMI's passed configuration directories
3.  Sort the list of files alphabetically
4.  Calculate the SHA1 checksums of every file
5.  Concatenate the list of file checksums
6.  Calculate the SHA1 checksum of the concatenated list of checksums - this is the AMI Config Checksum

To look-up an AMI ID by AMI Config Checksum:

1.  List all AMIs tagged with the desired AMI Config Checksum (tag name is `ami_config_checksum`)
2.  If no AMIs exist with that AMI Config Checksum, build and tag a new AMI and return it's AMI ID
3.  If an AMI has already been built, return it's AMI ID. Should multiple AMIs exist with the same AMI Config Checksum, return the AMI ID of the newest image.
