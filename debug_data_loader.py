import torch
from data_loader import get_loader  # Ensure this import works based on your project structure

def debug_data_loader(image_path, batch_size=1):
    # Use the same image size, num_workers, mode, and augmentation_prob as in your main script
    image_size = 720  # or the size you are using in your main script
    num_workers = 2
    mode = 'train'  # change if necessary
    augmentation_prob = 0.4  # adjust based on your setting

    # Initialize DataLoader
    data_loader = get_loader(image_path, image_size, batch_size, num_workers, mode, augmentation_prob)
    
    # Fetch one batch of data
    for images, GT_masks in data_loader:
        print("Images batch shape:", images.shape)
        print("Ground Truth batch shape:", GT_masks.shape)
        break  # Only process one batch

# Example usage
debug_data_loader('/notebooks/pleural_line_segment/init_play/repos/Image_Segmentation/baby_dataset/train/image')
