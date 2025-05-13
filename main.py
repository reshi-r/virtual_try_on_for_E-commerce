import cv2
import numpy as np

def overlay_image(background, overlay, position):
    """
    Overlay an image (with transparency) onto a background at a specific position.
    :param background: The background image.
    :param overlay: The overlay image with transparency.
    :param position: The x, y position to place the overlay.
    :return: The combined image.
    """
    x, y = position
    h, w, _ = overlay.shape

    # Ensure overlay fits within the background
    if x + w > background.shape[1] or y + h > background.shape[0]:
        print("Overlay image does not fit within the background at the given position.")
        return background

    # Extract alpha channel from overlay
    alpha = overlay[:, :, 3] / 255.0
    for c in range(0, 3):
        background[y:y+h, x:x+w, c] = (
            alpha * overlay[:, :, c] + (1 - alpha) * background[y:y+h, x:x+w, c]
        )
    return background

def virtual_try_on(user_image_path, item_image_path, position=(50, 50)):
    """
    Simulates a virtual try-on by overlaying an item image onto a user image.
    :param user_image_path: Path to the user's image.
    :param item_image_path: Path to the item's image (with transparency).
    :param position: The position to place the item on the user image.
    """
    # Read the user image and item image
    user_image = cv2.imread(user_image_path)
    item_image = cv2.imread(item_image_path, cv2.IMREAD_UNCHANGED)

    if user_image is None or item_image is None:
        print("Error: Could not read input images.")
        return

    # Overlay item onto user image
    combined_image = overlay_image(user_image, item_image, position)

    # Display the result
    cv2.imshow("Virtual Try-On", combined_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # Save the output
    output_path = "output_virtual_try_on.jpg"
    cv2.imwrite(output_path, combined_image)
    print(f"Output saved to {output_path}")

if _name_ == "_main_":
    # Example usage
    user_image_path = "user_image.jpg"  # Replace with the path to your user image
    item_image_path = "sunglasses.png"  # Replace with the path to your item image (with transparency)
    virtual_try_on(user_image_path, item_image_path, position=(100, 150))
