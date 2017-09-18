import boto3
from json import load

def obter_instance(resource_id):
    client = boto3.client('ec2')

    response = client.describe_tags(
    Filters=[
        {
            'Name': 'resource-id',
            'Values': [
                resource_id
            ],
        },
    ],
    )

    tags = response['Tags']
    nome_instanceid = [tag['Value'] for tag in tags if tag['Key'] == 'Name']

    if nome_instanceid:
    
        print(nome_instanceid)
        return nome_instanceid[0]
    
    else:
        return None

def setar_tag(resource_id, nome):
    client = boto3.client('ec2')

    response = client.create_tags(
        Resources=[
            resource_id
        ],
        Tags=[
            {
                'Key': 'Name',
                'Value': nome,
            },
        ],
    )

    print(response)

def main():
    
    with(open('C:\\Users\\aquinto\\Desktop\\Quinto\\Projects\\Scripts\\nomes.json')) as configuracao:
        volumes = load(configuracao)
        
    for volume in volumes['Volumes']:
        try:
            volumeid = volume['Attachments'][0]['VolumeId']
            instanceid = volume['Attachments'][0]['InstanceId']
            nome_instance = obter_instance(instanceid)

            if nome_instance:
                setar_tag(volumeid,nome_instance)

        except Exception as ex:
            print(ex)
            
        
if __name__ == '__main__':
    main()
    
    
