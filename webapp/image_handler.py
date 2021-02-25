import googleapiclient.discovery
from google.cloud import storage
from google.api_core.client_options import ClientOptions
from PIL import Image
import numpy as np
from skimage.color import rgb2lab, lab2rgb
from skimage.io import imsave
import os

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'image-colorization-280016-c617dae15ba5.json'

def predict_json(project, region, model, instances, version=None):
    prefix = "{}-ml".format(region) if region else "ml"
    api_endpoint = "https://{}.googleapis.com".format(prefix)
    client_options = ClientOptions(api_endpoint=api_endpoint)
    service = googleapiclient.discovery.build('ml', 'v1', client_options=client_options)
    name = 'projects/{}/models/{}'.format(project, model)

    if version is not None:
        name += '/versions/{}'.format(version)

    response = service.projects().predict(
        name=name,
        body={'instances': instances}
    ).execute()

    if 'error' in response:
        raise RuntimeError(response['error'])

    return response['predictions']

def handle_image(file, new_name):
    project_name = 'image-colorization-280016'
    region_name = 'europe-west4'
    model_name = 'my_model'
    
    im = Image.open(file.stream)
    im_grayscale = im.convert('LA')
    
    old_size = im.size
    
    size = 150           
    
    ratio = float(size) / max(old_size)
    new_size = tuple([int(x * ratio) for x in old_size])
    im = im.resize(new_size, Image.ANTIALIAS)
    im_grayscale = im_grayscale.resize(new_size, Image.ANTIALIAS)
               
    new_im = Image.new('RGB', (size, size))
    new_im.paste(im, ((size - new_size[0]) // 2, (size - new_size[1]) // 2))
    
    new_im_grayscale = Image.new('L', (size, size))
    new_im_grayscale.paste(im_grayscale, ((size - new_size[0]) // 2, (size - new_size[1]) // 2))
    im_arr_grayscale = np.array(new_im_grayscale, dtype='float')
    im_arr = np.array(new_im, dtype='float')
    im_arr *= 1.0 / 255
            
    lab = rgb2lab(im_arr)
    l = lab[:,:,0]
    l = np.expand_dims(l, axis = 0)
    l = np.expand_dims(l, axis = 3)   
    
    ab = predict_json(project_name, region_name, model_name, l.tolist()) 
    ab = np.array(ab)
    ab *= 128
               
    l = np.squeeze(l, axis = 3)
    image_colored = np.zeros((size, size, 3))
    image_colored[:,:,0] = l
    image_colored[:,:,1:] = ab
    image_colored = lab2rgb(image_colored)
    
    image_path = new_name + '.png'
    
    imsave('/tmp/grayscale_' + image_path, im_arr_grayscale)
    imsave('/tmp/colored_' + image_path, image_colored)
    
    bucket_name = 'image-colorization-280016-images'
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob_grayscale = bucket.blob('grayscale/' + image_path)
    blob_colored = bucket.blob('colored/' + image_path)
    
    blob_grayscale.upload_from_filename('/tmp/grayscale_' + image_path)
    blob_colored.upload_from_filename('/tmp/colored_' + image_path)
    
    return image_path