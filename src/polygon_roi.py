import sys
import math
import cv2 as cv
import numpy as np

class Lane (object):
    def __init__(self):

        self.dst= None 
        
    def main(self):
        default_file = 'Campus_02.png'
        #image=cv.imread(cv.samples.findFile("Test_Road_00.jpg"))
        #filename = input("Enter image file name (press Enter for default): ") or default_file
        filename=default_file
        #Loads an image
        src = cv.imread(cv.samples.findFile(filename), cv.IMREAD_GRAYSCALE)
        # Check if image is loaded fine
        if src is None:
            print('Error opening image!')
            print('Usage: hough_lines.py [image_name -- default ' + default_file + '] \n')
            return -1
    
        blur = cv.GaussianBlur(src, (5, 5), 0)
        self.dst = cv.Canny(blur, 0, 80, None)
        
        return self.dst

# ============================================================================

FINAL_LINE_COLOR = (250, 250, 250)
WORKING_LINE_COLOR = (127, 127, 127)

# ============================================================================

class PolygonDrawer(Lane):
    def __init__(self, window_name):
        super().__init__()
        self.window_name = 'Poygon Region of Interest' # Name for our window

        self.done = False # Flag signalling we're done
        self.current = (0, 0) # Current position, so we can draw the line-in-progress
        self.points = [] # List of points defining our polygon


    def on_mouse(self, event, x, y, buttons, user_param):
        # Mouse callback that gets called for every mouse event (i.e. moving, clicking, etc.)

        if self.done: # Nothing more to do
            return

        if event == cv.EVENT_MOUSEMOVE:
            # We want to be able to draw the line-in-progress, so update current mouse position
            self.current = (x, y)
        elif event == cv.EVENT_LBUTTONDOWN:
            # Left click means adding a point at current position to the list of points
            print("Adding point #%d with position(%d,%d)" % (len(self.points), x, y))
            self.points.append((x, y))
        elif event == cv.EVENT_RBUTTONDOWN:
            # Right click means we're done
            print("Completing polygon with %d points." % len(self.points))
            self.done = True


    def run(self):
        super().main()
        # Let's create our working window and set a mouse callback to handle events
        #cv.namedWindow(self.window_name, flags=cv.WINDOW_AUTOSIZE)
        cv.imshow(self.window_name, self.dst)
        cv.waitKey(1)
        cv.setMouseCallback(self.window_name, self.on_mouse)
        self.cdst = np.copy(self.dst)

        while(not self.done):
            # This is our drawing loop, we just continuously draw new images
            # and show them in the named window
          
            if (len(self.points) > 0):
                # Draw all the current polygon segments
                cv.polylines(self.dst, np.array([self.points]), False, FINAL_LINE_COLOR, 1)
                # And  also show what the current segment would look like
                #cv.line(self.dst, self.points[-1], self.current, WORKING_LINE_COLOR)
            # Update the window
            cv.imshow(self.window_name, self.dst)
            # And wait 50ms before next iteration (this will pump window messages meanwhile)
            if cv.waitKey(50) == 27: # ESC hit
                self.done = True
        
        
        cv.imshow(self.window_name, self.dst)
        # Waiting for the user to press any key
        cv.waitKey()


if __name__ == "__main__":
    
    ln=Lane
    pd = PolygonDrawer("Polygon")
    image = pd.run()
    print("Polygon = %s" % pd.points)
    mask = np.zeros_like(pd.dst)   
    ignore_mask_color = 255
    #filling pixels inside the polygon defined by "vertices" with the fill color    
    cv.fillPoly(mask,np.array([pd.points]), ignore_mask_color)
    #returning the image only where mask pixels are nonzero
    masked_image = cv.bitwise_and(pd.cdst, mask)
    cv.imshow('Region of Interest',masked_image)
    cv.waitKey()


   