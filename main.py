from PIL import Image
from colorama import Fore, init
import sys

init()

class image_data():
    width = 0
    height = 0
    image = None

    pixel_matrix = None
    brightness_matrix = None
    ascii_matrix = None

    inverted = False
    link = ""
    matrix_color_scheme = False
    matrix_colored = False

    #create all the data for the image manipulation
    def __init__(self):
        self.get_settings()
        self.pixel_matrix = self.loadImage(self.link)
        #select the lightning option
        self.brightness_matrix = self.generateBrightnessMatrix(self.pixel_matrix, 3, self.inverted)
        self.ascii_matrix = self.generateAscii(self.brightness_matrix)

    def get_settings(self):
        self.link = input("Enter the image link: ")
        print("(Y for yes | N for no)")
        i = input("Would you like the image to be inverted: ")
        if i.lower() == 'y':
            self.inverted = True
        i = input("Would you like the image to be printed in matrix color scheme: ")
        if i.lower() == 'y':
            self.matrix_color_scheme = True
        else:
            i = input("Would you like the image to be printed in colors: ")
            if i.lower() == "y":
                self.matrix_colored = True


    #loading the image
    def loadImage(self, link):
        #open the image and resize to fit
        image = Image.open(link)
        ratio = image.height / image.width
        image = image.resize((600, int(600 * ratio)))

        #assign the global vars
        width = image.width
        height = image.height
        self.image = image
        self.width = width
        self.height = height

        #generating the matrix
        pixel_matrix = [[None for _ in range(width)] for _ in range(height)]

        for y in range(height):
            for x in range(width):
                pixel_matrix[y][x] = self.image.getpixel((x, y))
        return pixel_matrix

    #generating the brightness matrix
    def generateBrightnessMatrix(self, pixel_matrix, option, inverted):
        width = self.width
        height = self.height
        brightness_matrix = [[None for _ in range(width)] for _ in range(height)]
        for y in range(height):
            for x in range(width):
                if option == 1:
                    brightness_matrix[y][x] = int((pixel_matrix[y][x][0] + pixel_matrix[y][x][1] + pixel_matrix[y][x][2]) / 3)
                elif option == 2:
                    brightness_matrix[y][x] = int((max(pixel_matrix[y][x][0], pixel_matrix[y][x][1], pixel_matrix[y][x][2]) + min(pixel_matrix[y][x][0], pixel_matrix[y][x][1], pixel_matrix[y][x][2])) / 2)
                elif option == 3:
                    brightness_matrix[y][x] = int((0.21 * pixel_matrix[y][x][0]) + (0.72 * pixel_matrix[y][x][1]) + (0.07 * pixel_matrix[y][x][2]))
                
                if inverted:
                    brightness_matrix[y][x] = 255 - brightness_matrix[y][x]
        return brightness_matrix

    #generating the ascii part
    def generateAscii(self, brightness_matrix):
        width = self.width
        height = self.height

        char_matrix = [[None for _ in range(width)] for _ in range(height)]
        chars = "`^\",:;Il!i~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"

        for y in range(height):
            for x in range(width):
                index = int((brightness_matrix[y][x] * len(chars)) / 255)
                char_matrix[y][x] = chars[index % len(chars)]

        return char_matrix
    


class image_operations(image_data):
    def __init__(self):
        super().__init__()
        if (self.matrix_color_scheme):
            self.printMatrix_styleMatrix()
        elif (self.matrix_colored):
            self.printColor()
        else:
            self.printMatrix()

    def printMatrix(self):
        for y in self.ascii_matrix:
            for x in y:
                for i in range(3):
                    print(x, end="")
            print()
    
    def printMatrix_styleMatrix(self):
        for y in range(self.height):
            for x in range(self.width):
                for i in range(3):
                    if self.brightness_matrix[y][x] > 128:
                        print(f"{Fore.GREEN}{self.ascii_matrix[y][x]}", end="")
                    else:
                        print(f"{Fore.BLACK}{self.ascii_matrix[y][x]}", end="")
            print()

    def closest_color(self, rgb_color):
        # Predefined standard colors and their RGB values
        standard_colors = {
            'BLACK': (0, 0, 0),
            'RED': (255, 0, 0),
            'GREEN': (0, 255, 0),
            'YELLOW': (255, 255, 0),
            'BLUE': (0, 0, 255),
            'MAGENTA': (255, 0, 255),
            'CYAN': (0, 255, 255),
            'WHITE': (255, 255, 255)
        }

        min_distance = sys.maxsize
        closest_color_name = None

        # Calculate the Euclidean distance for each standard color
        for color_name, color_rgb in standard_colors.items():
            distance = sum((c1 - c2) ** 2 for c1, c2 in zip(rgb_color, color_rgb)) ** 0.5
            if distance < min_distance:
                min_distance = distance
                closest_color_name = color_name

        return closest_color_name

    def printColor(self):
        for y in range(self.height):
            for x in range(self.width):
                for i in range(3):
                    closest_color_name = self.closest_color(self.pixel_matrix[y][x])
                    print(f"{getattr(Fore, closest_color_name)}{self.ascii_matrix[y][x]}", end="")
            print()
                
def main():
    myImage = image_operations()

main()