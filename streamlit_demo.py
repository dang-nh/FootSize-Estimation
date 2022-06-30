import streamlit as st
import pandas as pd
import numpy as np
import skimage
from foot_estimate import *
import os
import cv2
from sklearn import svm

def classifier():

    dict_label = {'normal_img': 0,
                'white_background_img': 1,
                'skin_background_img': 2,
                'pattern_background_img': 3,
                'curve_background_img': 4}
    X = []
    y = []
    for folder in os.listdir('image_classified'):
        for img_path in os.listdir('image_classified/' + folder):
            img = cv2.imread('image_classified/' + folder + '/' + img_path)
            img = cv2.resize(img, (128, 128))
            img = img/255
            img = img.flatten()
            X.append(img)
            y.append(dict_label[folder])
            
    n_samples = len(os.listdir('images/'))
    clf = svm.SVC(gamma=0.001, C=100)
    clf.fit(X, y)
    
    return clf




st.title('Welcome To Project Foot size Estimation!')
st.write("Choose any image and get corresponding foot size:")
uploaded_file = st.file_uploader("Choose an image...")

if uploaded_file is not None:
    # img_class = classifier(uploaded_file)
    
    dict_label = {0: 'normal_img',
              1: 'white_background_img',
              2: 'skin_background_img',
              3: 'pattern_background_img',
              4: 'curve_background_img'}
    
    height_size = [24.4, 24.8, 25.2, 25.7, 26, 26.5, 26.8, 27.3, 27.8, 28.3, 28.6, 29.4]
    Size_VN_h = ['40', '40-41', '41', '41-42', '42', '42-43', '43', '43-44', '44-45', '45', '46']
    Size_UK_h = ['6', '6.5', '7', '7.5', '8', '8.5', '9', '9.5', '10', '10.5', '11', '12']
    Size_US_h = ['7', '7.5', '8', '8.5', '9', '9.5', '10', '10.5', '11', '11.5', '12', '13']

    width_size = [9.8, 10, 10, 10.2, 10.2, 10.4, 10.4, 10.6, 10.6, 10.8, 10.8, 11, 11]
    Size_VN_w = ['38', '38-39', '39', '39-40', '40','40-41', '41', '41-42', '42', '42-43', '43', '43-44', '44']
    Size_UK_w = ['4.5', '5', '5.5', '6', '6.5', '7', '7.5', '8', '8.5', '9', '9.5', '10', '10.5']
    Size_US_w = ['5', '5.5', '6', '6.5', '7', '7.5', '8', '8.5', '9', '9.5', '10', '10.5', '11']
    # menu = ["Height", "Width"]
    
    st.title("Here is the image you've selected")
    st.image(uploaded_file, caption='Input Image', use_column_width=True)
    
    og_img = skimage.io.imread(uploaded_file)
    # test = cv2.imread(uploaded_file)
    
    test_img = skimage.io.imread(uploaded_file)
    test_img = cv2.cvtColor(test_img, cv2.COLOR_RGB2BGR)
    test_img = cv2.resize(test_img, (128, 128))
    # test_img = cv2.cvtColor(test_img, cv2.COLOR_BGR2GRAY)
    # resize test_img to (128, 128)
    test_img = test_img/255
    # print(test_img.shape)
            
    # flatten test_img to 1D array
    test_img = test_img.flatten()

    img_class = classifier().predict([test_img])[0]
    
    # img_class = classifier(uploaded_file=uploaded_file)
    preprocess_img = preprocess(og_img, img_class)
    
    st.title("Here is the image after preprocessing")
    st.image(preprocess_img, caption='Preprocessed Image', use_column_width=True)

    clustered_img = kMeans_cluster(preprocess_img, img_class)
    
    st.title("Here is the image after KMeans clustering")
    st.image(clustered_img, caption='Clustered Image', use_column_width=True)

    edge_detected_img = paperEdgeDetection(clustered_img)
    
    st.title("Here is the image after using Canny detection")
    st.image(edge_detected_img, caption='Edge Detected Image', use_column_width=True)

    boundRect, contours, contours_poly, img = getBoundingBox(edge_detected_img)
    
    # st.title("Here is the image after find countours")
    # st.image(img, caption='Image after find countours', use_column_width=True)
    
    if img_class == 0:
        pdraw = drawCnt(boundRect[0], contours, contours_poly, img)
        cropped_img, pcropped_img = cropOrig(boundRect[0], clustered_img)
    else:
        pdraw = drawCnt(boundRect[1], contours, contours_poly, img)
        cropped_img, pcropped_img = cropOrig(boundRect[1], clustered_img)
    st.title("Here is the bounding box of the a4 paper")
    st.image(pdraw, caption='Bounding box of paper', use_column_width=True)
    
    
    st.title("Here is the image after cropping")
    st.image(cropped_img, caption='Cropped Image', use_column_width=True)

    new_img = overlayImage(cropped_img, pcropped_img)
    
    st.title("Here is the image after overlay, We use it as a a4 paper")
    st.image(new_img, caption='Overlay Image', use_column_width=True)

    fedged = footEdgeDetection(new_img)
    fboundRect, fcnt, fcntpoly, fimg = getBoundingBox(fedged)
    fdraw = drawCnt(fboundRect[0], fcnt, fcntpoly, fimg)
    
    st.title("Here is the image after foot edge detection")
    st.image(fdraw, caption='Foot Edge Detected Image', use_column_width=True)

    ofs_w, ofs_h, fh, fw, ph, pw = calcFeetSize(pcropped_img, fboundRect)
    
    index_w = -1
    for i in range(len(width_size)-1):
        if width_size[i] <= ofs_w < width_size[i + 1]:
            index_w = i
            
    index_h = -1
    for i in range(len(height_size)-1):
        if height_size[i] <= ofs_h <= height_size[i+1]:
            index_w = i
    
    txt = f"[INFO] Foot's length (cm): {round(ofs_h, 3)} - Foot's width (cm): {round(ofs_w, 3)}"
    
    # resized_image = og_img.resize((336, 336))
    # st.image(resized_image)
    st.write(txt)
    st.title('[FOOT WIDTH SIZE] Size VN: {}\n + Size UK: {}\n + Size US: {}'.format(Size_VN_w[index_w], Size_UK_w[index_w],
                                                                                Size_US_w[index_w]))

    st.title('[FOOT HEIGHT SIZE] Size VN: {}\n + Size UK: {}\n + Size US: {}'.format(Size_VN_h[index_h], Size_UK_h[index_h],
                                                                                Size_US_h[index_h]))
