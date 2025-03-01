# csv-processor
Required Config:
{    dbname = 'mydb'
    user = 'myuser'
    password = 'mypassword'
    host = 'localhost'
    port = '5432'
    minio_host = 'localhost:9000'
    minio_key = 'minioadmin'
    minio_secret = 'minioadmin'
    minio_bucket = 'test'}

1 to upload the csv:

curl --location 'http://localhost:5000/upload_csv' \
--form 'file=@"/C:/Users/USER/Downloads/sheet1 - Sheet1.csv"'

2 get the status 

curl --location 'http://localhost:5000/status/78014dd3-b2ad-4b78-84b9-6788c85bf6cb'

3 download the file 

curl --location 'http://localhost:5000/download_csv/78014dd3-b2ad-4b78-84b9-6788c85bf6cb'
