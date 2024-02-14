import requests
import base64


def file_to_base64(file_path):
    try:
        with open(file_path, 'rb') as file:
            base64_encoded = base64.b64encode(file.read())
            return base64_encoded.decode('utf-8')
    except Exception as e:
        print(f"Error: {e}")
        return None

def url_to_base64(url):
    try:
        if not url.startswith('http'):
            url = 'http://' + url
        response = requests.get(url)
        if response.status_code == 200:
            content_type = response.headers.get('content-type')
            if 'image' in content_type:
                base64_encoded = base64.b64encode(response.content)
                base64_with_scheme = f'data:{content_type};base64,{base64_encoded.decode("utf-8")}'
                return base64_with_scheme
            elif 'pdf' in content_type:
                return file_to_base64(response.content)
            else:
                print("Unsupported file type.")
                return None
        else:
            print("Failed to fetch the content.")
            return None
    except Exception as e:
        print(f"Error: {e}")
        return None
    
def file_to_base64(file_path):
    try:
        with open(file_path, "rb") as file:
            encoded_string = base64.b64encode(file.read())
        return encoded_string.decode("utf-8")
    except FileNotFoundError:
        return None