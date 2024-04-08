# LogoFinder

### Project for the BIT

### Datasets
1. Fastfood https://www.kaggle.com/datasets/rohan0301/fast-food-store-images-mcdkfcbksubwaysbucks/data
2. Logos https://www.kaggle.com/datasets/lyly99/logodet3k

### TODO List
1. Create module for uploading images (Anatolii) всем хай
2. Create model for recognizing logos 
3. Create module for recognizing logos 
4. Create module for mapping indexes and text labels
5. Create module for building the path to the nearest place

### Responsibilities

| Function Name                             | Return | Person   | Description                                                                                                                                                                                                                                                                                |
|-------------------------------------------|--------|----------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| main()                                    | -      | Anatolii | Function for running other functions and for visualization                                                                                                                                                                                                                                 |
| uploader(path - String)                   | Image  | Anatolii | Function for uploading image into visualization system (into plot for testing). Gets path for the image as attribute, returns image as python object                                                                                                                                       |
| recognizer(path - String)                 | String |          | Function for recognizing text on the logo/sign, gets image object as attribute, returns recognized text                                                                                                                                                                                    |
| mapper(label - String)                    | String | Georgii  | Function for the converting readable text (e.g MacDonald's) into the index that will be using on the map (graph data base). Gets label of the some place as string, returns index (that will work with graph) as string                                                                    |
| pathFinder(index - String, point - Point) | Image  |          | Function for the finding the path on the map (graph) from some point to the nearest place that satisfies index. Gets index (for the some place) as string and start point (point class should be implemented). Returns image object of the map that can be used in the visualization block |

| Task Name        | Result                    | Person | Description                                                          |
|------------------|---------------------------|--------|----------------------------------------------------------------------|
| Training model   | File with model           |        | Creating structure of the NN, training it                            |
| Testing model    | Visualization, metrics    |        | Checking metrics and performance of the model                        |
| Checking indexes | Structure of the indexes  |        | Checking how to parse indexes, if it impossible, add places manually |

### Example of organizing

````
project/
│
├── main.py
├── upload_photo.py
└── recognize_text.py
````
````
# upload_photo.py

def upload_photo(file_path):
    # Implement your code for uploading photo here
    print("Uploading photo:", file_path)
````
````
# recognize_text.py

def recognize_text(image_path):
    # Implement your code for recognizing text here
    print("Recognizing text from image:", image_path)
````
````
# main.py

import upload_photo
import recognize_text

def main():
    # Example usage
    file_path = "example_photo.jpg"
    upload_photo.upload_photo(file_path)

    # Recognizing text from uploaded photo
    recognize_text.recognize_text(file_path)

if __name__ == "__main__":
    main()
````