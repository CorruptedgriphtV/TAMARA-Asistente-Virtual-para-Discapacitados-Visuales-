import os
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from msrest.authentication import CognitiveServicesCredentials
from PIL import Image
import subprocess
import pygame

# Set your credentials and endpoint
endpoint = '<your-endpoint>'
subscription_key = '<your-subscription-key>'

# Initialize Pygame
pygame.init()

# Set the display size
display_size = (640, 480)
screen = pygame.display.set_mode(display_size)

# Load the image
image_path = os.path.join(os.path.expanduser('~'), 'Desktop', '<your-image-filename>')
image = Image.open(image_path)

# Display the image
pygame.image.save(image, 'temp_image.png')
image_surface = pygame.image.load('temp_image.png')
screen.blit(image_surface, (0, 0))
pygame.display.flip()

# Create a ComputerVisionClient
computervision_client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(subscription_key))

# Define a function to analyze the image and play the description as an audio prompt
def analyze_and_play():
    with open(image_path, "rb") as image_file:
        image_data = image_file.read()
    analyze_result = computervision_client.analyze_image_in_stream(image_data, visual_features=['Categories', 'Tags', 'Description', 'Color'])
    description = analyze_result.description.captions[0].text
    subprocess.call(['espeak', description])

# Run the Pygame event loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                analyze_and_play()
        elif event.type == pygame.QUIT:
            pygame.quit()
            quit()