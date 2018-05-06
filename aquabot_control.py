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

debug = True

key_commands = ["W", "S", "A", "D", "Z", "C"] #Q for quit
joy_dict = {"2":"13", "3": "15", "X":"17", "Y":"19", "Z":"21"}

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
    axis z = thruster power (negative = less, positive = more) [21] (T)

    example message: "W0S0A0D0Z0C02030X0Y0Z0R"
    R = message ending character
    '''

    msg = list("W0S0A0D0Z0C02030X0Y0T0R;")
    #dictionary for joystick

    global key_name
    key_name = ""
    #Loop until the user clicks the close button on GUIs.
    global done
    done = False

    while done == False:
        # EVENT PROCESSING STEP
        event = pygame.event.wait()
        pygame.event.set_blocked(pygame.MOUSEMOTION)

        if event.type == pygame.QUIT:
            done = True
            #pygame.quit()

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
                counter = 1
                if key_name in key_commands:
                    for cmd in (key_commands):
                        if debug :
                            #print(key_name)
                            print(cmd)

                        if key_name == cmd:
                            print (u'"{}" key pressed'.format(key_name))
                            #print(counter)
                            msg[counter] = "1"
                        counter += 2
                else:
                    #msg = ""
                    #return msg 
                    continue


            if event.type == pygame.KEYUP:
                counter = 1
                if key_name in key_commands:
                    for cmd in (key_commands):
                        if key_name == key_commands:
                            print (u'"{}" key released'.format(key_name))
                            msg[counter] = "0"
                        counter += 2
                    key_name = ""
                else:
                    #msg = ""
                    #return msg
                    continue

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
                    msg[int(joy_dict.get("X"))] =  ("%.5f" %axis)
                    textPrint.print_text(screen, "Axis {} value: {:>6.3f}".format(i+1, axis) )

                else:
                    axis = axis = joystick.get_axis( i )
                    textPrint.print_text(screen, "Axis {} value: {:>6.3f}".format(i+1, axis* -1.0) )

                    axis = axis * -1.0

                    if (i == 1):
                        msg[int(joy_dict.get("Y"))] = ("%.5f" %axis)
                    if (i == 2):
                        msg[int(joy_dict.get("Z"))] = ("%.5f" %axis)

            textPrint.unindent()

            buttons = joystick.get_numbuttons()
            textPrint.print_text(screen, "Number of buttons: {}".format(buttons) )
            textPrint.indent()

            for i in range( buttons ):
                #get_button: current button state (returns bool)
                button = joystick.get_button( i )
                #button 2 or button 3
                textPrint.print_text(screen, "Button {:>2} value: {}".format(i+1,button) )

                if button:
                    if i == 1:
                        #get button 2
                        msg[int(joy_dict.get("2"))] = "1"
                    elif i == 2:
                        #get button 3
                        msg[int(joy_dict.get("3"))] = "1"
                    else:
                        continue

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
        print(string_msg) #if no new message, keep current state
        return string_msg

#udp client
def main():
    #host = "192.168.1.100"
    host = "127.0.0.1"
    port = 5001 #different port from server (we will create server ourselves)

   # server = ("192.168.1.101", 5000) #pi
    server = ("127.0.0.1", 5000)

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind((host, port))

    message = gen_message()

    while done != True :
        s.sendto(message.encode('utf-8'), server)
        data, addr = s.recvfrom(1024)
        data = data.decode('utf-8')
        print("Received from server: " + data)
        message = gen_message()

    s.close()
    pygame.quit()


main()
# if __name__ == '__main__':
#     main()
