import random
import matplotlib.pyplot as plt
import numpy as np
import cv2


def crop_center(data, crop_height, crop_width):
    """
    Crop the center region of the data.

    Args:
        data (numpy.ndarray): The input data.
        crop_height (int): The height of the crop.
        crop_width (int): The width of the crop.

    Returns:
        numpy.ndarray: The cropped data.
    """
    # Get the center of the array
    center_y = data.shape[0] // 2
    center_x = data.shape[1] // 2

    # Calculate the start and end indices for the crop
    start_y = center_y - crop_height // 2
    end_y = center_y + crop_height // 2
    start_x = center_x - crop_width // 2
    end_x = center_x + crop_width // 2

    # Crop the data to the center region
    data_cropped = data[start_y:end_y, start_x:end_x]

    return data_cropped


def detect_ocean(data, threshold=0.7):
    """
    Detect ocean areas in the data.
    :param data: numpy array
    :param threshold: dark points threshold
    :return: regions of darkness representing ocean areas
    """

    # detect dark points on image and dilate up to a threshold
    dark = data < threshold
    dark = dark.astype(np.uint8)
    kernel = np.ones((1, 1), np.uint8)
    dark = cv2.dilate(dark, kernel, iterations=5)

    return dark


def split_ocean_areas(ocean_areas):
    """
    Split ocean areas into connected components.
    :param ocean_areas: dark regions representing ocean areas
    :return: number of connected components and labels to represent individual areas of ocean
    """

    kernel = np.ones((1, 1), np.uint8)
    ocean_areas = cv2.erode(ocean_areas, kernel, iterations=5)
    ocean_areas = cv2.dilate(ocean_areas, kernel, iterations=5)
    num_labels, labels = cv2.connectedComponents(ocean_areas, connectivity=4)

    return num_labels, labels


def visualize_ocean_areas(labels):
    """
    Prep for vis only
    """

    unique_labels, counts = np.unique(labels, return_counts=True)  # some technical debt here
    most_common_label = unique_labels[np.argmax(counts)]

    other_labels = [label for label in unique_labels if label != most_common_label]
    random.shuffle(other_labels)

    label_map = {label: i for i, label in enumerate(other_labels, start=1)}
    label_map[most_common_label] = 255

    # Apply the mapping
    shuffled_labels = np.zeros_like(labels)
    for label, new_label in label_map.items():
        shuffled_labels[labels == label] = new_label

    # Set the colormap to 'gray' for ensuring 255 is white
    shuffled_labels = shuffled_labels.astype(np.uint8)
    shuffled_labels_color = cv2.applyColorMap(shuffled_labels, cv2.COLORMAP_HSV)

    return shuffled_labels_color


def calculate_fragmentation_metrics(labels):
    """
    Calculate fragmentation metrics.
    :param labels: numpy array
    :return: fragmentation metrics
    """
    unique_labels, counts = np.unique(labels, return_counts=True)

    area = np.sum(counts[1:])
    perimeter = cv2.Canny(labels.astype(np.uint8), 100, 200).sum()
    fragmentation_index = perimeter / area
    avg_area = area / len(unique_labels)
    skewness = np.mean((counts[1:] - avg_area) ** 3) / (np.std(counts[1:]) ** 3)
    # ratio_largest to rest
    largest_area = np.max(counts[1:])
    other_areas = np.sum(counts[1:]) - largest_area
    ratio_largest_to_rest = largest_area / other_areas

    return area, perimeter, fragmentation_index, avg_area, skewness, ratio_largest_to_rest


def plot_ocean_areas(data, ocean_areas, labels):
    fig, ax = plt.subplots(1, 3, figsize=(15, 5))

    ax[0].imshow(data, cmap='gray')
    ax[0].set_title('Original Image')
    ax[0].axis('off')

    ax[1].imshow(ocean_areas, cmap='gray')
    ax[1].set_title('Ocean Areas')
    ax[1].axis('off')

    ax[2].imshow(labels)
    ax[2].set_title('Split Ocean Areas')
    ax[2].axis('off')
    plt.savefig('ocean_areas.png', dpi=300)
    plt.show()


def run_fragmentation(data,
                      crop_to_centre=500,
                      plot=True):
    """
    Wrapper function for fragmentation indices, as called by HealthIndex class.
    :param data: numpy array
    :return:
    """
    print("Data:", data)

    if crop_to_centre > 0:
        data = crop_center(data, crop_to_centre, crop_to_centre)

    data = (data - np.nanmin(data)) / (np.nanmax(data) - np.nanmin(data))

    ocean_areas = detect_ocean(data, threshold=0.7)

    num_labels, labels = split_ocean_areas(ocean_areas)

    area, perimeter, fragmentation_index, avg_area, skewness, ratio_largest = calculate_fragmentation_metrics(labels)

    shuffled_labels_color = visualize_ocean_areas(labels)

    if plot:
        plot_ocean_areas(data, ocean_areas, shuffled_labels_color)

    return_dicts = {'data': data,
                    'ocean_areas': ocean_areas,
                    'labels': labels,
                    'total_ocean_area': area,
                    'fragmentation_perimeter': perimeter,
                    'fragmentation_index': fragmentation_index,
                    'average_ocean_fragment_area': avg_area,
                    'fragment_skewness': skewness,
                    'ratio_largest_to_rest': ratio_largest}

    return return_dicts
