from pathlib import Path

from ..http.client import (
    HttpClient,
)

def download_image(image_id: str, dest: tuple) -> None:
    url = f"http://images.nypl.org/index.php?id={image_id}&t=w&download=1"

    http_client = HttpClient()
    response = http_client.get(url)

    data_bytes = response.bytes

    image_file = Path(*dest)
    image_file.write_bytes(data_bytes)
    
