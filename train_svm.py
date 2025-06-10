import os
import cv2
import numpy as np
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
import joblib
from skimage.feature import hog
from skimage.filters import sobel

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
            sobel_images.append(sobel_region)
    return np.concatenate(sobel_results), sobel_images

# Extract image using Sobel and HOG
def combine_sobel_hog(folder, regions=4):
    data = []
    labels = []
    hog_images = []
    sobel_images_all = []

    for className in os.listdir(folder):
        classDir = os.path.join(folder, className)
        for imageName in os.listdir(classDir):
            imagePath = os.path.join(classDir, imageName)
            image = cv2.imread(imagePath, cv2.IMREAD_GRAYSCALE)
            if image is None:
                continue
            image = cv2.resize(image, (64, 64), interpolation=cv2.INTER_AREA)

            # Implementing region based sobel to image
            sobel_results, sobel_images = region_based_sobel(image, regions)
            sobel_images_all.append(sobel_images)

            # Extracting HOG image
            hog_results, hog_image = hog(image, pixels_per_cell=(8, 8), cells_per_block=(2, 2),
                                          feature_vector=True, visualize=True)
            hog_images.append(hog_image)

            # Combining sobel and HOG
            combine_result = np.concatenate((sobel_results, hog_results))

            data.append(combine_result)
            labels.append(className)
    return np.array(data), np.array(labels), np.array(hog_images), sobel_images_all

def main():
    train_dir = 'C:/xampp/htdocs/phpscript/Project DIP/dataset/vehicleDefault/training_set'
    test_dir = 'C:/xampp/htdocs/phpscript/Project DIP/dataset/vehicleDefault/test_set'
    
    # Training data
    train_data, train_labels, _, _ = combine_sobel_hog(train_dir)
    # Test data
    test_data, test_labels, _, _ = combine_sobel_hog(test_dir)

    # Train SVM Model
    svm = SVC(kernel='poly', probability=True)
    svm.fit(train_data, train_labels)

    # Test predictions
    predicted_labels = svm.predict(test_data)

    # Calculate accuracy
    accuracy = accuracy_score(test_labels, predicted_labels)
    print(f"Accuracy: {accuracy * 100:.2f}%")

    # Save the model
    model_path = 'C:/xampp/htdocs/phpscript/Project DIP/svm_model.pkl'
    joblib.dump(svm, model_path)
    print(f"Model saved to {model_path}")

    # Save the accuracy
    accuracy_path = 'C:/xampp/htdocs/phpscript/Project DIP/accuracy.txt'
    with open(accuracy_path, 'w') as f:
        f.write(f"{accuracy * 100:.2f}")
    print(f"Accuracy saved to {accuracy_path}")

if __name__ == "__main__":
    main()
