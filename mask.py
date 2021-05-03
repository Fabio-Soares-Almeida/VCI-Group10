# mask.py
#
# Program to apply maks
# This program allows us to select the a color and apply that color mask
#
# Running process:
#   - Write the name of the file where the masks are saved
#   - Write the desired color
#   - Press 'q' to finish the program


import cv2
import numpy as np
import ast

# Load image
image = cv2.imread(cv2.samples.findFile("legos4.png"))

# Reduce the image
height, width = image.shape[:2]
size = (int(width * 0.4), int(height * 0.15))  # bgr
image = cv2.resize(image, size, interpolation=cv2.INTER_AREA)

# Open file
nome_arquivo = input('Nome do ficheiro:')
arquivo = open(nome_arquivo, 'r+')
contente = arquivo.read()

# If file is empty close program
if(contente == ''):
    print('Ficheiro nao contem nenhuma cor')
    cv2.destroyAllWindows()
    quit()

# Import Dictionary
cores = ast.literal_eval(contente)

# Read desired color
cor = input('Cor:')
teste = str(cor+'_l')

# If color exist in the dictionary continue
if(teste in cores):

    string_l = str(cores[cor + '_l'])
    string_u = str(cores[cor + '_u'])

    lower = np.fromstring(string_l, sep=',')
    upper = np.fromstring(string_u, sep=',')

    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Create mask
    mask = cv2.inRange(hsv, lower, upper)
    result = cv2.bitwise_and(image, image, mask=mask)

    while (1):

        # Display result image
        cv2.imshow('image', result)
        k = cv2.waitKey(10) & 0xFF
        if k == ord('q'):
            break
else:
    print('Cor nao existe')

cv2.destroyAllWindows()