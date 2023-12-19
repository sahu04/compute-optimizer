#!/bin/bash
if [[ $# -lt 1 ]]; then
  echo "Usage: ${0} <AccountID> [<Region>]"
  exit 1
fi
NOW=$(date +"%m%d%Y%H%M")
AccountID=${1}
AWS_DEFAULT_REGION=${2:-us-east-1}  # Use 'us-east-1' if not provided
script_top="$(pwd)/bin"
outputdir="$(pwd)/output"
csvfile="${outputdir}/${AccountID}_copt-${NOW}.csv"
jsonfile="${outputdir}/${AccountID}_copt-${NOW}.json"

aws compute-optimizer get-ec2-instance-recommendations --output json > "${jsonfile}"

# cat "${jsonfile}"
## Pass the json file to the python script along with the CSV File for the output
python3 "${script_top}/reportComputeOptData.py" "${jsonfile}" "${csvfile}"


echo "CSV File generated... - ${csvfile}"

