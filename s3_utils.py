import boto3
import os
from dotenv import load_dotenv

load_dotenv()


# ============================================================
# AWS CONFIGURATION
# ============================================================

AWS_REGION = os.getenv(
    "AWS_REGION",
    "ap-south-1"
)

S3_BUCKET = os.getenv(
    "S3_BUCKET"
)


# ============================================================
# CREATE S3 CLIENT
# ============================================================

def get_s3_client():

    return boto3.client(
        "s3",
        region_name=AWS_REGION
    )


# ============================================================
# UPLOAD FILE
# ============================================================

def upload_file(
    file_path,
    s3_key
):

    if not S3_BUCKET:

        raise ValueError(
            "S3_BUCKET is not configured in .env"
        )

    s3 = get_s3_client()

    print(
        f"Uploading {file_path}..."
    )

    s3.upload_file(
        file_path,
        S3_BUCKET,
        s3_key
    )

    print(
        f"Upload successful: s3://{S3_BUCKET}/{s3_key}"
    )


# ============================================================
# LIST FILES
# ============================================================

def list_files():

    s3 = get_s3_client()

    response = s3.list_objects_v2(
        Bucket=S3_BUCKET
    )

    if "Contents" not in response:

        print("Bucket is empty.")

        return

    print("\nFiles in S3:")

    for obj in response["Contents"]:

        print(
            f"  {obj['Key']} "
            f"({obj['Size']:,} bytes)"
        )


# ============================================================
# DOWNLOAD FILE
# ============================================================

def download_file(
    s3_key,
    local_path
):

    s3 = get_s3_client()

    print(
        f"Downloading {s3_key}..."
    )

    s3.download_file(
        S3_BUCKET,
        s3_key,
        local_path
    )

    print(
        f"Downloaded to {local_path}"
    )


# ============================================================
# MAIN TEST
# ============================================================

if __name__ == "__main__":

    print("=" * 60)
    print("S3 CONNECTION TEST")
    print("=" * 60)

    print(
        f"\nRegion: {AWS_REGION}"
    )

    print(
        f"Bucket: {S3_BUCKET}"
    )

    list_files()

    print("\n" + "=" * 60)