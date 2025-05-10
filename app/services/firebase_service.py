import firebase_admin
from firebase_admin import credentials, storage
import uuid

cred = credentials.Certificate("seu_arquivo_service_account.json")
firebase_admin.initialize_app(cred, {
    'storageBucket': 'seu-projeto.appspot.com'
})

async def upload_image(image_file):
    bucket = storage.bucket()
    blob = bucket.blob(f"images/{uuid.uuid4()}_{image_file.filename}")
    blob.upload_from_file(image_file.file, content_type=image_file.content_type)
    blob.make_public()
    return blob.public_url
