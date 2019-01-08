#!/bin/bash

echo "Instances";
aws ec2 describe-instances --query 'Reservations[].Instances[].[PrivateIpAddress,InstanceId,State.Name,Tags[?Key==`Name`].Value[]]' --output text | sed 's/None$/None\n/' | sed '$!N;s/\n/ /'

