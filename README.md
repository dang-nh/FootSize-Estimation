Mini-project: Foot size estimation
------------------------------------------------------------------------------------------------------------------------

https://github.com/dang-nh/FootSize-Estimation

A demo website using Streamlit with the following functionalities:

- upload images


- foot and paper segmentation: possibly uses image processing techniques or DL-based approaches

- visualize intermediate results: segments of foot, paper, paper's corners...

- output width, height and corresponding size


How to Evaluate?
------------------------------------------------------------------------------------------------------------------------
- Clone the repo: ```git clone https://github.com/dang-nh/FootSize-Estimation.git```
- Download folder ``image_classified`` from this repo or from Goolge Drive: https://bit.ly/3I7Qgyd
- ``cd`` to the cloned directory
- Install required packages: ```pip install -r requirements.txt```
- run the command: ```streamlit run streamlit_demo.py```

Working approach
------------------------------------------------------------------------------------------------------------------------
- Classify type of image by SVM
- Remove noise from original image using Median Blur
- If image background have same color with skin, using Gamma Correction to improve contrast and tuning upper bound and lower bound of HSV to get better result
- Run K-means clustering on preprocessed image for color based segmentation
- Detect the edges in clustered image.
- Find contours in Edge Detection output and filter the largest contour.
- Generate the bounding rectangle from the contour and rotate to extract paper
- Then drop 10% of the paper image to get the foot contour.
- Create the foot's bounding Box to get the height/width of Foot.
- Calculate the foot size base on the ratio between the paper and foot.
https://www.dienmayxanh.com/kinh-nghiem-hay/cach-xac-dinh-size-giay-cho-nam-gioi-don-gian-de-1357862

Limitations
------------------------------------------------------------------------------------------------------------------------
- If floor color is white, then it will difficult to segment the paper but if using K-means with ```num_cluster=3``` it will be easier.
- Feet should not go out of the paper. 
- If the background have many patterns and have some white lines, then it will be difficult to segment the paper.
- The accuracy of the algorithm is not very good. It is about approx. **65%** accurate.

Group members
------------------------------------------------------------------------------------------------------------------------
- Nguyen Hoang Dang 20194423
- Do Quoc An 20194414
- Ha Vu Thanh Dat 20194424
- Le Hai Son 20194449