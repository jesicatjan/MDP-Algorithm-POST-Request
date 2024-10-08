import socket
import numpy as np
import cv2
import os
from ultralytics import YOLO
from datetime import datetime

# Load the YOLO model with the specified weights
model = YOLO('/Users/praveenavijayan/Downloads/NTU Computer Science (Mac)/Y3S1/SC2079 - Multidisciplinary Design Project/Image Recognition/content/runs/detect/train/weights/2nd25best.pt')

# Set up the server socket to receive the image
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('0.0.0.0', 8000))  # Bind to all interfaces on port 8000
server_socket.listen(1)

# Define the path where you want to save the images
save_folder = '/Users/praveenavijayan/Downloads/NTU Computer Science (Mac)/Y3S1/SC2079 - Multidisciplinary Design Project/Image Recognition/YOLO_Predicted_Images'

# Ensure the directory exists
if not os.path.exists(save_folder):
    os.makedirs(save_folder)

print('Waiting for connection...')
conn, addr = server_socket.accept()
print(f'Connected by {addr}')

try:
    # Receive the image size (sent as a 16-byte string)
    data = conn.recv(16)
    if not data:
        print("No data received. Closing connection.")
    else:
        img_size = int(data.decode().strip())  # Decode and strip any extra spaces
        print(f"Expecting to receive an image of size: {img_size} bytes.")

        # Receive the image data
        img_bytes = b""
        while len(img_bytes) < img_size:
            packet = conn.recv(4096)  # Receive in chunks of 4096 bytes
            if not packet:
                break
            img_bytes += packet

        print(f"Received image of size {len(img_bytes)} bytes.")

        # Convert the bytes back to an image
        img_array = np.frombuffer(img_bytes, dtype=np.uint8)
        img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
        
        if img is None:
            raise ValueError("Failed to decode image. Image data might be corrupted.")

        print(f"Image decoded successfully, shape: {img.shape}")

        # Convert BGR (OpenCV) to RGB (for the YOLO model and display purposes)
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        # Run YOLO model inference directly on the received image
        results = model(img_rgb)
        
        print("YOLO inference completed")

        # Process and save the results
        for result in results:
            # Get the image with predictions (bounding boxes, labels, etc.)
            img_with_boxes = result.plot()  # This returns a numpy array with the image and drawn boxes

            # Convert to BGR for OpenCV display and saving
            img_bgr = cv2.cvtColor(img_with_boxes, cv2.COLOR_RGB2BGR)

            # Save the image to the specified folder with a timestamp
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            save_path = os.path.join(save_folder, f"predicted_image_{timestamp}.jpg")
            cv2.imwrite(save_path, img_bgr)
            print(f"Predicted image saved to {save_path}")
            
            # Display the image using OpenCV (Optional)
            cv2.imshow("YOLO Detected Image", img_bgr)
            cv2.waitKey(0)  # This waits indefinitely until a key is pressed.
            #cv2.destroyAllWindows()  # Close the window after key press.
            
            # Close the image display window after 1000ms (1 second) or immediately if no key is pressed
            #cv2.waitKey(1000)  # Wait for 1 second, then close the window automatically

            # Close any OpenCV windows (optional)
            cv2.destroyAllWindows()
        
            # Close the connection explicitly
            conn.close()
            print("Connection closed.")
    
            #Exit the script to ensure termination
            server_socket.close()
            print("Server socket closed. Exiting now.")

finally:
    # Close the connection explicitly
    conn.close()
    print("Connection closed.")
    
    #Exit the script to ensure termination
    server_socket.close()
    print("Server socket closed. Exiting now.")



