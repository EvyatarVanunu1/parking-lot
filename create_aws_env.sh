echo "AWS_DEFAULT_REGION=`aws configure get region`" >> aws_env_file
echo "AWS_ACCESS_KEY_ID=`aws configure get aws_access_key_id`" >> aws_env_file
echo "AWS_SECRET_ACCESS_KEY=`aws configure get aws_secret_access_key`" >> aws_env_file