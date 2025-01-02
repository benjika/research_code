Computer Vision and Predictive Models for Individual Feed Intake Measurement in Dairy Cows  
Overview  
This repository contains the code and models developed for the thesis: "A Computer Vision System and Predictive Models for Individual Feed Intake Measurement in Dairy Cows" by Benyamin Katz. The study introduces a system using RGB-D cameras and predictive modeling to measure and analyze individual feed intake of dairy cows under outdoor conditions.  

Features
Cow Detection: YOLOv8-based object detection for identifying cows in feeding zones.  
Feed Volume Calculation: Point cloud manipulation to estimate feed volume.  
Predictive Models:  
Volume decrease prediction.   
Weight decrease prediction.  
Meal weight prediction.  

Data Collection and Integration:  
Data gathered using Zed 2i 3D cameras, weight scales, and weather sensors.  
Synchronization managed by Jetson Xavier NX with Python scripts.  

Experimental Setup  
Hardware:  
Zed 2i 3D Camera positioned at 4 m for large-area coverage.  
Weight scales for consumed and unconsumed feed.  
Weather data from Arduino-based sensors and the nation meteorological station.  
Data Frequency:  
Feed data: Every 20 seconds.  
Weather data: Every 2 minutes.    

Models  
Linear Models: Linear Regression(with and withoiut PCA and with and without feature selection), Ridge, Lasso, Elastic Net.  
Tree-Based Mode  ls: Decision Tree, Random Forest, Gradient Boosting.  
Performance:
Adj. R² of 0.88 R² of up to 0.88 for meal weight prediction.  
Mean Absolute Error (MAE) of 1.547 kg for meal weight prediction.  

Usage  
Preprocessing: Use the scripts in preprocessing/ for data cleaning and augmentation.  
Model Training: Execute the notebooks in models/ for training and evaluation.  
Analysis: Run the scripts in analysis/ for robustness tests and feature importance.  

Repository Structure  
Python  
📂 project-root/  
├── 📁 data/  
├── 📁 arduino_code/  
├── 📁 loop_recorder/  
├── 📁 yolov8_cows/  
├── 📁 preprocessing/  
├── 📁 analysis/  
├── 📜 requirements.txt  
└── 📜 README.md  
Results
Accuracy: Demonstrated significant improvements in prediction accuracy using tree-based models.
Insights: Identified key environmental factors influencing feed intake, paving the way for smarter feed management.
Acknowledgments
Special thanks to my supervisors, Prof. Yael Edan and Prof. Ilan Halachmi, the Precision Livestock Farming Lab, and the Volcani Agricultural Research Organization.

License
This project is licensed under the MIT License. See the LICENSE file for details.

Contact  
For questions or collaborations, please contact: Benyamin Katz  
bennykatz1012@gmail.com  
https://www.linkedin.com/in/benny-katz/
