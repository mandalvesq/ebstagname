import boto3

client = boto3.client('ec2')

response = client.create_tags(
    Resources=[
        '',
    ],
    Tags=[
        {
            'Key': 'Teste',
            'Value': 'Python',
        },
    ],
)

print(response)
