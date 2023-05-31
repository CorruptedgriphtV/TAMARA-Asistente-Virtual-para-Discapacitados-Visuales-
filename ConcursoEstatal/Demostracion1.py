import os
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from msrest.authentication import CognitiveServicesCredentials
import matplotlib.pyplot as plt
from PIL import Image

# Set your credentials and endpoint
endpoint = '<your-endpoint>'
subscription_key = '<your-subscription-key>'

# Create a ComputerVisionClient
computervision_client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(subscription_key))

# Open the image and display it
image_path = os.path.join(os.path.expanduser('~'), 'Desktop', '<your-image-filename>')
image = Image.open(image_path)
plt.imshow(image)
plt.show()

# Analyze the image
with open(image_path, "rb") as image_file:
    image_data = image_file.read()
analyze_result = computervision_client.analyze_image_in_stream(image_data, visual_features=['Categories', 'Tags', 'Description', 'Color'])

# Display the analysis results
print('Categories:')
for category in analyze_result.categories:
    print(category.name)
print()

print('Tags:')
for tag in analyze_result.tags:
print()

print('Description:')
print(analyze_result.description.captions[0].text)
print()

print('Dominant Color:')
print(analyze_result.color.dominant_color_background)