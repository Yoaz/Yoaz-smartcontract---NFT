from email.mime import image
from operator import index
from brownie import network, AdvancedCollectible
from metadata.metadata_sample import metadata_template
from scripts.helpful_scripts import get_breed
from pathlib import Path
import requests
from dotenv import load_dotenv
import os
import json

load_dotenv()

breed_to_image_uri = {
    "PUG": "https://ipfs.io/ipfs/QmSsYRx3LpDAb1GZQm7zZ1AuHZjfbPkD6J7s9r41xu1mf8?filename=pug.png",
    "SHIBA-INU": "https://ipfs.io/ipfs/QmYx6GsYAKnNzZ9A6NvEKV9nf1VaDzJrqDR23Y8YSkebLU?filename=shiba-inu.png",
    "ST-BERNARD": "https://ipfs.io/ipfs/QmUPjADFGEKmfohdTaNcWhp7VGk26h5jXDA7v3VtTnTLcW?filename=st-bernard.png",
}


def main():
    advanced_collectible = AdvancedCollectible[-1]
    number_of_advanced_collectible = advanced_collectible.tokenCounter()
    print(f"You have created {number_of_advanced_collectible} NFT's!!")
    token_metadata = metadata_template
    print(token_metadata)

    for token_id in range(number_of_advanced_collectible):
        breed = get_breed(advanced_collectible.tokenIdToBreed(token_id))
        metadata_file_name = (
            f"./metadata/{network.show_active()}/{token_id}-{breed}.json"
        )
        print("Creating metadata file name: " + metadata_file_name)
        if Path(metadata_file_name).exists():
            print(f"{metadata_file_name} file already exist! Delete to overwrite")
        else:
            token_metadata["name"] = breed
            token_metadata["description"] = f"a cute {token_metadata['name']}"
            image_path = "./img/" + breed.lower().replace("_", "-") + ".png"

            # Shortcut from reuploading to IPFS if already uploaded
            image_uri = None
            if os.getenv("UPLOAD_IPFS") == "true":
                # image_uri = upload_to_ipfs(image_path)
                image_uri = upload_to_pinata(image_path)
            image_uri = image_uri if image_uri else breed_to_image_uri[breed]

            token_metadata["image"] = image_uri
            with open(metadata_file_name, "w") as file:
                json.dump(token_metadata, file)
            if os.getenv("UPLOAD_IPFS") == "true":
                # upload_to_ipfs(file)
                upload_to_pinata(metadata_file_name)


def upload_to_ipfs(image_path):
    with Path(image_path).open("rb") as fp:
        image_binary = fp.read()
        ipfs_url = (
            os.getenv("IPFS_URL") if os.getenv("IPFS_URL") else "http://localhost:5001"
        )
        endpoint = "/api/v0/add"
        response = requests.post(ipfs_url + endpoint, files={"file": image_binary})
        ipfs_hash = response.json()["Hash"]
        # ./img/0-shiba-inu.png -> 0-shiba-inu.png
        image_name = image_path.split("/")[-1:][0]
        image_uri = f"https://ipfs.io/ipfs/{ipfs_hash}?filename={image_name}"
    return image_uri


def upload_to_pinata(image_path):
    with Path(image_path).open("rb") as fp:
        image_binary = fp.read()
        pinata_url = (
            os.getenv("PINATA_BASE_URL")
            if os.getenv("PINATA_BASE_URL")
            else "https://api.pinata.cloud"
        )
        end_point = "/pinning/pinFileToIPFS"
        headers = {
            "pinata_api_key": os.getenv("PINATA_API_KEY"),
            "pinata_secret_api_key": os.getenv("PINATA_SECRET"),
        }
        # ./img/0-shiba-inu.png -> 0-shiba-inu.png
        image_name = image_path.split("/")[-1:][0]
        response = requests.post(
            pinata_url + end_point,
            files={"file": (image_name, image_binary)},
            headers=headers,
        )
        print(response.json())
        hash = response.json()["IpfsHash"]
        # https://gateway.pinata.cloud/ipfs/image_name.png
        image_uri = "https://gateway.pinata.cloud/ipfs/" + hash
    return image_uri
