from BCD import * 
from CPP import *
from ImageProcessing import *

if __name__ == '__main__':
    
    io.imshow(sobel)
    io.show()
    io.imshow(FirstClean)
    io.show()
    io.imshow(SecondClean)
    io.show()

    io.imshow(dilated)
    io.show()
    io.imshow(closed)
    io.show()
       
    cv2.imshow('image', img) 
 
    while (True):
        value = input("Please Enter Contour Number ")
        value = int(value)
        new = img_as_ubyte(closed)
        bits = cv2.bitwise_not(new)
        mask = np.ones_like(bits)
        
        cv2.drawContours(mask, contours, value, color=(255, 255, 255), thickness=cv2.FILLED) 
        out = np.ones_like(bits) 
        out[mask == 255] = bits[mask == 255]
        

        (y, x) = np.where(mask == 255)
        (topy, topx) = (np.min(y), np.min(x))
        (bottomy, bottomx) = (np.max(y), np.max(x))
        out = out[topy:bottomy+1, topx:bottomx+1]
   
        cv2.imshow('Output', out )

        

        BCDImage = np.array(out)
        if len(BCDImage.shape) > 2:
            BCDImage = BCDImage[:, :, 0]
        erode_img = BCDImage / np.max(BCDImage)
        separate_img, cells = bcd(erode_img)
        print('Total cells: ',(int(cells - 1)))
       
        CellsImage = display_separate_map(separate_img, cells)
        print (CellsImage.shape[1])
        plt.imshow(CellsImage)
        plt.show()

        print_graph()
        print("Internal representation: ", graph)
        print('Chinese Postman Distance is:',Chinese_Postman(graph))

        #Graph = CellsImage.tolist()
        #print('Graph: ',Graph)
        t3 = np.arange(cells)
        x3 = x3_func(t3)
        plt.plot(t3,x3)

        plt.show()