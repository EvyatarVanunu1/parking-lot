REGION=`cat ~/.aws/config | grep "region" | sed -n 's/\(region = \)\(.*\)/\2/p'`
KEY_ID=`cat ~/.aws/credentials | grep "aws_access_key_id" | sed -n 's/\(aws_access_key_id = \)\(.*\)/\2/p'`
KEY_SECRET=`cat ~/.aws/credentials | grep "aws_secret_access_key" | sed -n 's/\(aws_secret_access_key = \)\(.*\)/\2/p'`

echo "AWS_DEFAULT_REGION=${REGION}" >> aws_env_file
echo "AWS_ACCESS_KEY_ID=${KEY_ID}" >> aws_env_file
echo "AWS_SECRET_ACCESS_KEY=${KEY_SECRET}" >> aws_env_file