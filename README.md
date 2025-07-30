# pearl-lab-software-dev

Computer vision algorithm development for *Bootle Blast*, a mixed-reality therapy tool built at Pearl Lab (Holland Bloorview Kids Rehabilitation Hospital).

## About the Project

*Bootle Blast* is a therapeutic game designed by Pearl Lab at Holland Bloorview Kids Rehabilitation Hospital and built using the Unity game engine. It currently features 15 unique mini-games, each aimed at supporting and reinforcing various movement patterns — from upper to lower limb motion. Of these 15 games, 5 incorporate mixed-reality elements, requiring players to grasp and move real-world objects to translate their movements into in-game actions. The focus of this repository is improving the detection system for the mini-game **Magic Block**, which uses color-coded physical blocks (blue, red, yellow, green). In this game, players copy a stack of colored blocks displayed on screen. Points are awarded based on how closely the real-life stack matches the on-screen configuration in both color and order. Bootle Blast uses a 3D camera-computer (Orbbec Persee) and body tracking software to capture 19 distinct skeletal landmarks. It also uses an RGB camera to detect and identify the colored blocks. This data is valuable for tracking physical rehabilitation progress and measuring changes over time.
Currently, a combination of skeletal tracking and RGB input is used to monitor both the player and the physical objects. However, the detection algorithm faces several challenges, including inaccurate recognition when blocks are partially occluded, reduced tracking accuracy when there is significant distance between the player and the camera, and difficulty in detecting fine hand movements.

<div align="center">
  <img src="media/demo.png" alt='"Magic Block" Demo' width="500"/>
</div>


The goal of this repository is to develop modern and alternative computer vision tools to address these challenges and improve the system’s robustness and accuracy. Specifically, we are exploring:
- Integration of modern libraries like **YOLOv8**
- Use of **fiducial markers** (e.g., AprilTags) to improve tracking
- Making the system more accessible to users without access to a 3D camera or specifically colored blocks

To learn more about Pearl Lab, Bootle Blast’s mini-games, and in-game lore, visit the [Pearl Lab website](https://hollandbloorview.ca/research-education/bloorview-research-institute/research-centres-labs/pearl-lab).

## YOLOv8 for Object Detection

I trained a **YOLOv8** model to detect colored blocks using a custom dataset of real-world images in custom home settings.

### Data Collection

1. **Environment Setup**
   To mimic diverse real-life conditions, a controlled setup replicating a standard living room was used.
   
  <p align="center">
    <img src="media/enviro.jpeg" alt="Enviro1" width="500"/>
  </p>
  
   To mimic diverse real-life conditions, photos were captured under a wide range of settings:
   - Distance: Near and far from the camera
   - Lighting: Bright, dim, single lamp, double lamps, natural light from windows
   - Visibility: With and without occlusion (e.g., partially blocked fiducial markers)

  <p align="center">
    <img src="media/enviro2.jpeg" alt="Enviro1" width="500"/>
    <img src="media/enviro3.jpeg" alt="Enviro1" width="500"/>
  </p>

   These variations were intentional to help the YOLOv8 model generalize better and perform accurately in real-world scenarios.

1. **Camera**
  Images were captured using both a 3D Orbbec Persee camera and a standard 2D webcam. This combination allowed us to gather diverse visual data, including depth-aware and RGB-only perspectives,     enhancing the robustness of the training dataset.
  
4. **Image Annotation via [CVAT.ai](https://cvat.ai)**  
   - Annotated over **150+ images**, each image has at least 3 instances of a block.
   - There are four classes: red, blue, yellow and green.
   - Exported in YOLO format for training

     
<p align="center">
  <img src="media/cvat.png" alt="CVAT Labeling" width="500"/>
</p>



### Model Training with YOLOv8

YOLOv8 was selected for its high speed and accuracy in real-time object detection tasks. The training process was carried out using the Ultralytics Python interface, which streamlined dataset loading, augmentation, and optimization. After training, the model's best-performing weights were saved as best.pt for use in inference and deployment.


---

## Web-Based Detection Demo

A lightweight demo was developed to run the trained YOLOv8 model in real-time:

- **Backend:** Python & Flask  
- **Frontend:** HTML, CSS, JavaScript  
- **Detection:** OpenCV + YOLOv8 for live detection

<p align="center">
  <img src="./images/demo-interface.png" alt="YOLOv8 Flask Demo" width="500"/>
</p>


## 🎯 Fiducial Markers

Fiducial markers were used to uniquely identify blocks in the scene for detection and classification. They offer the advantage of not relying on colour, which is highly distorted by differing lighting settings. However, they are affected more by occlusion. Two types were explored: **QR codes** and **AprilTags**.

---

## QR Codes

QR codes were initially tested due to their widespread recognition and built-in data encoding. For detection, OpenCV’s `QRCodeDetector` was used to generate, identify, and decode the markers. Each QR code was encoded with the corresponding block color, allowing the system to read and associate color data directly from the code. Due to the small size of the blocks, the QR codes were printed to be 4 cm per dimension.

<p align="center">
  <img src=" " alt="QR Labeling" width="500"/>
</p>

However, QR codes proved to be extremely unreliable:
- Inconsistent detection when viewed at an angle or in low-light conditions  
- Limited range, with small codes becoming undetectable beyond half a meter  
- Unstable tracking, often flickering in and out of detection even when stationary

To improve the performance of the algorhtimn, more steps were taken in preprocessing:

1. **Grayscale Conversion:**  
   The original color frame is converted to grayscale to simplify processing.
2. **Gaussian Blur:**  
   A small blur is applied to reduce noise and smooth the image.
3. **Sharpening Filter:**  
   A custom kernel enhances edges to emphasize fiducial markers.
4. **Otsu Thresholding:**  
   Adaptive binary thresholding converts the image to black and white based on intensity.
5. **Inversion:**  
   The binary image is inverted to highlight the markers as white on a dark background.
6. **Dilation:**  
   A morphological dilation with a large kernel is applied to close gaps and strengthen shapes.
7. **Contour Detection:**  
   External contours are found in the processed image, filtered by area to exclude noise.
8. **Region of Interest (ROI) Zoom:**  
   Each valid contour is expanded with a margin and zoomed in.
9. **Detect and Drawing Results:**  
   The detecti=ion is run on every zoomed in countour. If a detection occurs, a border is drawn around it and the data is decoded.


While preprocessing significantly improved the effective detection range to approximately **1.3 meters**, it came with a tradeoff: increased computational cost. The zoom operation combined with running detection on multiple cropped regions made the pipeline resource-intensive, limiting performance on lower-end systems.

## AprilTags

AprilTags, specifically from the `tag16h5` family, were used as the primary fiducial system. These markers are designed for robust visual detection under a variety of conditions and provide unique IDs for each tag.

- High contrast design enables **accurate detection at various angles and distances**  
- Tags were **physically printed and affixed to blocks**, making them easily distinguishable  
- Well-supported by pose estimation libraries for future applications (e.g., 3D localization)

<p align="center">
  <img src="./images/apriltags-example.png" alt="AprilTags Example" width="400"/>
</p>

AprilTags offered superior performance compared to QR codes, especially in dynamic or partially occluded environments, and were therefore used for all final annotations and training.
## License

This project is licensed under the [MIT License](LICENSE).
