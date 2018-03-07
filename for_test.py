import boto3
import datetime
import time

def lambda_handler(event, context):

    today=datetime.datetime.now().strftime("%s")
    # epoch_time = int(time.time())
    # delete_time = epoch_time - 2629743
    client = boto3.client('rds')
    #dry_run = True

    my_deletion_counter = 0
    count = 1
    days = 30
    print "Deleting any manual snapshots older than {days} days".format(days=days)
   
    rds_response = client.describe_db_snapshots(SnapshotType='manual')
    response = client.describe_db_instances(DBInstanceIdentifier='test-db')

    #print rds_response
    
    for rdsarn in response['DBInstances']:
        intarn = rdsarn['DBInstanceArn']
    for rds in rds_response['DBSnapshots']:
        dbarn = rds['DBSnapshotArn']
        creTime = rds['SnapshotCreateTime']
        snapName = rds['DBSnapshotIdentifier']
        tag_response = client.list_tags_for_resource(ResourceName=dbarn)
        for tag in tag_response:
            tag_1 = tag_response['TagList']
        for tag in tag_1:
            if tag['Key'] == 'expireDate':
                expireDate = tag['Value']
                if expireDate > today:
                    print "Deleting snapshot: " + snapName + ": Timestamp: " + str(creTime)
                    my_deletion_counter = my_deletion_counter + 1
                # for snapshot in client.describe_db_snapshots(SnapshotType='manual'):
                #     if expireDate > today:
                #         print "Deleting snapshot...." + snapName
                #         client.delete_db_snapshot(DBSnapshotIdentifier=snapN['DBSnapshotIdentifier'])

        
                else:
                    print "No snapshots to delete " + "in: " + intarn

# For when you have thousands of snapshots being deleted! #
    if count % 50 == 0:
        print "Taking a break."
        time.sleep(5)
    count += 1
        
    print "You Have Deleted {number}".format(number = my_deletion_counter) + " Snapshots from: " + intarn
            
lambda_handler(1,1)






    