import boto3

client = boto3.client('ec2')

response = client.create_tags(
    Resources=[
        'vol-ea2b51f9',
    ],
    Tags=[
        {
            'Key': 'Teste',
            'Value': 'Python',
        },
    ],
)

print(response)