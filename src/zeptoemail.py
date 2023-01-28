import boto3
from botocore.exceptions import ClientError

accessKey=''
secretAccessKey=''
region='us-east-1'

def verifyIdentity(a):
    client=boto3.client('ses',aws_access_key_id=accessKey,aws_secret_access_key=secretAccessKey,region_name=region)
    response=client.verify_email_identity(EmailAddress=a)
    print(response)

def sendEmail(sub,r):
    client=boto3.client('ses',aws_access_key_id=accessKey,aws_secret_access_key=secretAccessKey,region_name=region)
    SENDER='otp.service@makeskilled.com'
    RECIPIENT=r
    SUBJECT=sub
    BODY_HTML="""<html>
    <head></head>
    <body>
    <h1>"""+SUBJECT+"""</h1>
    <p> Your bid finalized, arrange Meeting with officials """""".<br><br>
    Thanks, <br/>
    Team B8<br>
    </p>
    </body>
    </html>
    """
    CHARSET='utf-8'
    try:
        response=client.send_email(Destination={'ToAddresses':[RECIPIENT,],},
        Message={'Body':{'Html':{'Charset':CHARSET,'Data':BODY_HTML,},
        'Text':{'Charset':CHARSET,'Data':""},},
        'Subject':{'Charset': CHARSET,'Data': SUBJECT,},},
        Source=SENDER)
    except ClientError as e:
        print(e.response['Error']['Message'])
        return False
    else:
        print('Email Sent!')
        return True