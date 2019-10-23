# aws-glue-deploy-utility
Boilerplate for deploying glue jobs through shell script. 

For developers, it will be useful as script can :
* Install external libraries
* Zip extra py files and externa libraries
* Upload main .py and zip files to s3 bucket
* Deploy glue job through loudformation

It also allows deployment for different stages e.g. {developer}, dev, qa, prod

## How-to Use Script
### Folder Structure 

### ENV Configuration
Add ENV configuration in utility/src/config/env.py file for different stages

### Deploy Script Configuration

```python
# Specify bucket in which you wish to upload zip and .py files
build_bucket='<specify build artifacts bucket>'
# Project prefix. 
project="<project prefix>"
# Default Stage
stage="dev"
# AWS profile to be used in AWS CLI
aws_profile="default"
# ARN of Glue Role to be used in Glue operation.
glue_role_arn='<specify Glue Role ARN>'
```

### Run Deploy Script
```shell
deploy <glue_job> -stage <stage> -cf <cf_folder>

## Arguments

### glue_job    mandatory
###             glue job name if selective glue job should be deployed

### -stage      mandatory
###             To define stage

### stage       mandatory with -stage
###             It will be used to pass stage environment parameters.
###             It can be {developer name}, dev, qa or prod.
###             {developer name} is useful in case of multiple developers are working on same job in same region.

### cf          optional
###             if specified, glue job will deployed through CF else only files will be uploaded to s3.

### cf_folder   mandatory with -cf otherwise optional
###             if specified, it will be taken as path for cf template (excluding *cf* folder). e.g. cf/ingeston/etl/bp_sample_job.json
###             should set cf_folder to 'ingestion/etl'
```