import hashlib


def generate_file_signature(filename):
    # Generate SHA256 hash for the file
    hasher = hashlib.sha256()
    with open(filename, "rb") as f:
        while chunk := f.read(4096):
            hasher.update(chunk)
    return hasher.hexdigest()
