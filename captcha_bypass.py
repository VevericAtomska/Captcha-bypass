import requests
from bs4 import BeautifulSoup
import pytesseract
from PIL import Image
from io import BytesIO

def test_captcha_security(url, form_data):
    session = requests.Session()
    response = session.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    
    captcha_img_tag = None
    img_tags = soup.find_all('img')
    for img in img_tags:
        if 'captcha' in img['src'].lower():
            captcha_img_tag = img
            break

    if not captcha_img_tag:
        print("No CAPTCHA image found.")
        return

    captcha_url = captcha_img_tag['src']
    if not captcha_url.startswith('http'):
        captcha_url = url + captcha_url

    
    response = session.get(captcha_url)
    img = Image.open(BytesIO(response.content))

    
    captcha_text = pytesseract.image_to_string(img).strip()
    print(f"Detected CAPTCHA text: {captcha_text}")

    
    form = soup.find('form')
    if not form:
        print("No form found on the page.")
        return

    action = form['action']
    if not action.startswith('http'):
        action = url + action

    form_inputs = form.find_all('input')
    post_data = {input_tag['name']: input_tag.get('value', '') for input_tag in form_inputs}
    post_data.update(form_data)
    post_data['captcha'] = captcha_text

    response = session.post(action, data=post_data)
    if "captcha" in response.text.lower():
        print("CAPTCHA bypass failed.")
    else:
        print("CAPTCHA bypass successful.")


target_url = 'https://example.com/login'
form_data = {
    'username': 'testuser',
    'password': 'testpassword'
}
test_captcha_security(target_url, form_data)
