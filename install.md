Install Python: If you don't already have Python installed on your system, you can download it from the official Python website: https://www.python.org/downloads/

Install required libraries: The code uses several Python libraries that you will need to install. You can install them using the following commands:

Azure Cognitive Services: pip install azure-cognitiveservices-vision-computervision
Pygame: pip install pygame
Pillow: pip install Pillow
Matplotlib: pip install matplotlib
Espeak: pip install eSpeak
Ms rest: pip msrest.authentication

Or install it on a single command: pip install azure.cognitiveservices.vision.computervision msrest matplotlib Pillow

Sign up for Azure Cognitive Services: To use Azure Cognitive Services, you need to sign up for an account and create a new Computer Vision resource. Follow the instructions on the Azure Cognitive Services website: https://azure.microsoft.com/en-us/services/cognitive-services/computer-vision/

Before you can use the Azure Cognitive Services API, you need to create a resource in the Azure Portal. Follow these steps to create the resource:

Go to the Azure Portal.
Click on the "+ Create a resource" button in the top left corner of the page.
Search for "Cognitive Services" in the search bar and select the "Cognitive Services" option from the results.
Click on the "Create" button.
Fill in the required information for the resource, such as the name, subscription, location, and pricing tier.
Select "Review + create" and then click on "Create" again to create the resource.
Get your credentials and endpoint: Once you have created a new Computer Vision resource, you will need to get your subscription key and endpoint. You can find these on the "Keys and Endpoint" page of your resource.

Set your credentials and endpoint in the code: Open the Python code and replace <your-endpoint> and <your-subscription-key> with your actual endpoint and subscription key.

Save your image on the Desktop: Save an image that you want to analyze on your Desktop.

Run the code: Open a terminal window, navigate to the directory where the Python code is saved, and run the following command: python analyze_image.py

Press the spacebar to analyze the image: The Pygame window will display the image. Press the spacebar to analyze the image and play the description as an audio prompt using eSpeak.

Last revision: 25/02/2023 Emilio Estefan (CorruptedgriphtV)