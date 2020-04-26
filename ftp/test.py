from itertools import zip_longest

def grouper(inputs, n, fillvalue=None):
    iters = [iter(inputs)] * n
    return zip_longest(*iters, fillvalue=fillvalue)

a = [1, 2, 3, 4]
print(list(grouper(a, 0)))


def get_s3_client():
    client = boto3.client('s3')
    return client


def copy_file(file_name):

    sftp = connect_sftp()
    client = get_s3_client()
    data_file = io.BytesIO()
    sftp.getfo(file_name, data_file)
    logger.info('Copying file from SFTP to S3')
    data_file.seek(0)
    client.put_object(Body=data_file, Bucket='test-ftp', Key=S3_PATH+file_name)
    logger.info('Copying file completed successfully !!!')
