'''
Top side control software for UBC Aquabot (UDP Client).
The program will take digital and analog inputs to control the claw, twister, and six thrusters.

Version 1:
Take user inputs
- keyboard: 'w' (forward) 's' (backward) 'a' (twister left) 'd' (twister right) 'z' (claw open) 'c' (claw close)
- speed setting for twister and claw (to be decided)
- Logitech Attack 3 Joystick: yaw, pitch, lift, thruster power

Version 2:
Make aquabot_control a client that packages input as a string and sends it to server using UDP.
'''
import pygame
import socket

# Define some colors
BLACK    = (   0,   0,   0)
WHITE    = ( 255, 255, 255)

# This is a simple class that will help us print to the screen
# It has nothing to do with the joysticks, just outputting the
# information onto GUI.
class TextPrint:
    def __init__(self):
        self.reset()
        self.font = pygame.font.Font(None, 20)

    def print_text(self, screen, textString):
        textBitmap = self.font.render(textString, True, BLACK)
        screen.blit(textBitmap, [self.x, self.y])
        self.y += self.line_height

    def reset(self):
        self.x = 10
        self.y = 10
        self.line_height = 15

    def indent(self):
        self.x += 10

    def unindent(self):
        self.x -= 10


pygame.init()

# Set the width and height of the screen [width,height]
size = [500, 700]
screen = pygame.display.set_mode(size)

pygame.display.set_caption("Aquabot Control")



# Used to manage how fast the screen updates
clock = pygame.time.Clock()

# Initialize the joysticks
pygame.joystick.init()

# Get ready to print_text
textPrint = TextPrint()

# -------- Main Program Loop -----------
def gen_message():
    '''
    w = froward [1]
    s = backward [3]
    a = twister left [5]
    d = twister right [7]
    z = claw open [9]
    c = claw Close [11]

    button 2 = lift [13]
    button 3 = sink [15]

    axis x = yaw (negative = left, positive = right) [17]
    axis y = pitch (negative = up, positive = down) [19]
    axis z = thruster power (negative = less, positive = more) [21]
    '''

    msg = list("w0s0a0d0z0c02030x0y0z0")
    global key_name
    key_name = ""
    #Loop until the user clicks the close button on GUIs.
    done = False

    while done == False:
        # EVENT PROCESSING STEP
        event = pygame.event.wait()

        if event.type == pygame.QUIT:
            done = True

        # for event in pygame.event.get(): # User did something
        #     if event.type == pygame.QUIT: # If user clicked close
        #         done=True # Flag that we are done so we exit this loop
        #     # Possible joystick actions: JOYAXISMOTION JOYBALLMOTION JOYBUTTONDOWN JOYBUTTONUP JOYHATMOTION

        if event.type in (pygame.KEYDOWN, pygame.KEYUP):
            # gets the key name
            key_name = pygame.key.name(event.key)
            # converts to uppercase the key name
            key_name = key_name.upper()

            if event.type == pygame.KEYDOWN:
                print (u'"{}" key pressed'.format(key_name))
            if event.type == pygame.KEYUP:
                print (u'"{}" key released'.format(key_name))
                key_name = ""

        if event.type == pygame.JOYBUTTONDOWN:
            print("Joystick button pressed.")
        if event.type == pygame.JOYBUTTONUP:
            print("Joystick button released.")

        # DRAWING STEP
        # First, clear the screen to white. Don't put other drawing commands
        # above this, or they will be erased with this command.
        screen.fill(WHITE)
        textPrint.reset()

        # Get count of joysticks
        joystick_count = pygame.joystick.get_count()

        textPrint.print_text(screen, "Number of joysticks: {}".format(joystick_count) )
        textPrint.indent()

        # For each joystick:
        for i in range(joystick_count):
            joystick = pygame.joystick.Joystick(i)
            joystick.init()

            textPrint.print_text(screen, "Joystick {}".format(i+1) )
            textPrint.indent()

            # Get the name from the OS for the controller/joystick
            name = joystick.get_name()
            textPrint.print_text(screen, "Joystick name: {}".format(name) )

            # Usually axis run in pairs, up/down for one, and left/right for
            # the other.
            axes = joystick.get_numaxes()
            textPrint.print_text(screen, "Number of axes: {}".format(axes) )
            textPrint.indent()

            for i in range( axes ):
                if (i == 0):
                    axis = joystick.get_axis( i )
                    textPrint.print_text(screen, "Axis {} value: {:>6.3f}".format(i+1, axis) )
                else:
                    axis = axis = joystick.get_axis( i )
                    textPrint.print_text(screen, "Axis {} value: {:>6.3f}".format(i+1, axis* -1.0) )
            textPrint.unindent()

            buttons = joystick.get_numbuttons()
            textPrint.print_text(screen, "Number of buttons: {}".format(buttons) )
            textPrint.indent()

            for i in range( buttons ):
                #get_button: current button state (returns bool)
                button = joystick.get_button( i )
                textPrint.print_text(screen, "Button {:>2} value: {}".format(i+1,button) )
            textPrint.unindent()

            textPrint.unindent()
            textPrint.unindent()
            textPrint.print_text(screen, "Key pressed: {}".format(key_name) )

        # ALL CODE TO DRAW SHOULD GO ABOVE THIS COMMENT

        # Go ahead and update the screen with what we've drawn.
        pygame.display.flip()

        #generate message

        # Limit to 20 frames per second
        clock.tick(20)

        string_msg = "".join(msg)
        print(string_msg)
        #return msg

#def main():

# Close the window and quit.
# If you forget this line, the program will 'hang'
# on exit if running from IDLE.
#pygame.quit()

gen_message()
# if __name__ == '__main__':
#     main()
