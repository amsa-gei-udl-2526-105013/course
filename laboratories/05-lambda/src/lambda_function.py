import boto3
import cv2
import os
import numpy as np
import matplotlib.pyplot as plt

def handler(event, context):

    os.environ['MPLCONFIGDIR'] = '/tmp/matplotlib'
    output_bucket = os.environ['DST_BUCKET']

    s3 = boto3.client('s3')
    input_bucket = event['Records'][0]['s3']['bucket']['name']
    input_key = event['Records'][0]['s3']['object']['key']
    filename = os.path.basename(input_key)
    local_path = '/tmp/' + filename

    s3.download_file(input_bucket, input_key, local_path)

    image = cv2.imread(local_path, cv2.IMREAD_COLOR)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    circles = cv2.HoughCircles(blurred, cv2.HOUGH_GRADIENT, dp=1, minDist=20, param1=50, param2=30, minRadius=5, maxRadius=30)

    if circles is not None:
        circles = np.round(circles[0, :]).astype("int")

        for (x, y, r) in circles:
            cv2.circle(image, (x, y), r, (0, 255, 0), 4)
            cv2.rectangle(image, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)

    fig = plt.figure()
    plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    plt.axis('off')
    output_path = '/tmp/' + filename + '_processed.jpg'
    plt.savefig(output_path)

    s3.upload_file(output_path, output_bucket, filename + '_processed.jpg')

    return {
        'statusCode': 200,
        'body': {"message": "Image processed and uploaded to S3!, Number of cells: " + str(len(circles))}
    }