import boto3

client = boto3.client('ec2')

response = client.describe_tags(
    Filters=[
        {
            'Name': 'resource-id',
            'Values': [
                'i-9f984c4e',
            ],
        },
    ],
)

nome_instance = response['Tags'][2]['Value']
print(nome_instance)