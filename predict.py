import os
import cv2
import numpy as np
from sklearn.svm import SVC
import joblib
from skimage.feature import hog
from skimage.filters import sobel
import sys
import matplotlib.pyplot as plt

# Sobel - Region Based Segmentation
def region_based_sobel(image, regions=4):
    h, w = image.shape
    region_size_h = h // regions
    region_size_w = w // regions
    sobel_results = []
    sobel_images = []

    for i in range(regions):
        for j in range(regions):
            region = image[i * region_size_h:(i + 1) * region_size_h, j * region_size_w:(j + 1) * region_size_w]
            sobel_region = sobel(region)
            sobel_results.append(sobel_region.flatten())

            # Make image better visualization
            sobel_region = (sobel_region - sobel_region.min()) / (sobel_region.max() - sobel_region.min()) * 255
            sobel_images.append(sobel_region.astype(np.uint8))
            
    return np.concatenate(sobel_results), sobel_images

# Combined image to 1 picture
def create_image_picture(images, rows, cols):
    h, w = images[0].shape
    picture_image = np.zeros((rows * h, cols * w), dtype=np.uint8)

    for i in range(rows):
        for j in range(cols):
            picture_image[i * h:(i + 1) * h, j * w:(j + 1) * w] = images[i * cols + j]

    return picture_image

# Predict Image
def predict_image_with_sobel_hog(image_path, model_path, regions=4):
    svm = joblib.load(model_path)  
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    image = cv2.resize(image, (64, 64), interpolation=cv2.INTER_AREA)

    # Extract features using region-based Sobel and HOG
    sobel_results, sobel_images = region_based_sobel(image, regions)
    hog_results, hog_image = hog(image, pixels_per_cell=(8, 8), cells_per_block=(2, 2),
                                 feature_vector=True, visualize=True)
    combine_result = np.concatenate((sobel_results, hog_results))
    image_features = combine_result.reshape(1, -1)

    # Predict the class of the image
    prediction = svm.predict(image_features)[0]
    prediction_prob = svm.predict_proba(image_features)[0]
    confidence = max(prediction_prob) * 100
    confidence = round(confidence, 2)  

    # Create a picture for the Sobel images
    sobel_image_picture = create_image_picture(sobel_images, regions, regions)

    # Save Sobel and HOG images
    sobel_image_path = 'C:/xampp/htdocs/phpscript/Project DIP/sobel_result.png'
    hog_image_path = 'C:/xampp/htdocs/phpscript/Project DIP/hog_result.png'
    combined_image_path = 'C:/xampp/htdocs/phpscript/Project DIP/combined_result.png'

    plt.imsave(sobel_image_path, sobel_image_picture, cmap='gray')
    plt.imsave(hog_image_path, hog_image, cmap='gray')

    # Display sobel and HOG image
    fig, axs = plt.subplots(1, 2, figsize=(10, 5))
    axs[0].imshow(sobel_image_picture, cmap='gray')
    axs[0].set_title('Sobel Image')
    axs[0].axis('off')

    axs[1].imshow(hog_image, cmap='gray')
    axs[1].set_title('HOG Image')
    axs[1].axis('off')

    plt.tight_layout(pad=2.0)
    plt.savefig(combined_image_path, bbox_inches='tight')
    plt.close(fig)

    return prediction, confidence, sobel_image_path, hog_image_path, combined_image_path

def main():
    if len(sys.argv) != 2:
        print("Usage: python predict.py <image_path>")
        return

    image_path = sys.argv[1]
    model_path = 'C:/xampp/htdocs/phpscript/Project DIP/svm_model.pkl'  

    prediction, confidence, sobel_image_path, hog_image_path, combined_image_path = predict_image_with_sobel_hog(image_path, model_path)

    print(f"{prediction},{confidence},{sobel_image_path},{hog_image_path},{combined_image_path}")

if __name__ == "__main__":
    main()
