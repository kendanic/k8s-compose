import boto3

ec2 = boto3.resource(ec2)

report = []

for instance in ec2.instances.all():
    report.append({
        "Id": instance.id,
        "Public_ip": str(instance.instance.public_ip_address),
        "Private_ip": str(instance.instance.private_ip_address),
    })

for x in report():
    print(x)

    