import matplotlib.pyplot as plt
import cv2
import numpy as np

# read and convert img to rgb format
input_path = "/home/endi/Dropbox/vision/Zlatan.jpg"
input_img = cv2.imread(input_path, 1)
target_path = "/home/endi/Dropbox/vision/r.jpg"
target_img = cv2.imread(target_path, 1)
input_rgb = cv2.cvtColor(input_img, cv2.COLOR_BGR2RGB)
target_rgb = cv2.cvtColor(target_img, cv2.COLOR_BGR2RGB)

# split imgs to channels
input_r, input_g, input_b = cv2.split(input_rgb)
target_r, target_g, target_b = cv2.split(target_rgb)

def findPdf(channel):
    flat = channel.flatten()
    frequency = np.zeros((256), dtype=int)

    for i in flat:
        frequency[i] += 1

    pdf = frequency / np.sum(frequency)

    return pdf

# find R, G, B channel pdf
pdf_input_r = findPdf(input_r)
pdf_input_g = findPdf(input_g)
pdf_input_b = findPdf(input_b)

pdf_target_r = findPdf(target_r)
pdf_target_g = findPdf(target_g)
pdf_target_b = findPdf(target_b)

# find R, G, B channel cdf
cdf_input_r = np.cumsum(pdf_input_r)
cdf_input_g = np.cumsum(pdf_input_g)
cdf_input_b = np.cumsum(pdf_input_b)

cdf_target_r = np.cumsum(pdf_target_r)
cdf_target_g = np.cumsum(pdf_target_g)
cdf_target_b = np.cumsum(pdf_target_b)

# cdf = [cdf_target_r, cdf_target_g, cdf_target_b]

# for i in range(3):
#     plt.subplot(3,1,i+1)
#     plt.bar(range(256), cdf[i], width=0.7, align='center')
#
# plt.show()

def histogramMatch(input, target, cdf_input, cdf_target):
    R, C = input.shape
    K = np.zeros((R,C), dtype=int)

    mi = np.min(input)
    Mi = np.max(input)
    gj = np.min(target)

    for gi in range(mi, Mi):

        while gj < 255 and cdf_target[gj] < cdf_input[gi]:

            gj += 1
        print(gj)
        K = K + (gj * (input == gi))

    return K


anan = histogramMatch(input_r, target_r, cdf_input_r, cdf_target_r)
baban = histogramMatch(input_g, target_g, cdf_input_g, cdf_target_g)
deden = histogramMatch(input_b, target_b, cdf_input_b, cdf_target_b)
print(anan)
hey = findPdf(anan)
hey = np.cumsum(hey)

plt.bar(range(256), cdf_input_r, width=0.7, align='center')
plt.show()
plt.bar(range(256), cdf_target_r, width=0.7, align='center')
plt.show()
plt.bar(range(256), hey, width=0.7, align='center')
plt.show()



ldu = cv2.merge((anan, baban, deden))
plt.imshow(input_rgb)
plt.show()
plt.imshow(target_rgb)
plt.show()
plt.imshow(ldu)
plt.show()




