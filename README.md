Put the content of the current folder in any public S3 Bucket.

The below commands could help you to upload this from the console using AWS CLI.

```bash
# pystravans
echo "Please enter a bucket name: "; read bucket;  export MYBUCKET=$bucket

aws s3 mb s3://$MYBUCKET

# Upload files, if all looks good remove the --dryrun flag at the end.
aws s3 cp $(pwd)/front s3://$MYBUCKET/front/ --recursive --acl public-read --dryrun
```


