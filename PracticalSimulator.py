import tkinter as tk
import pygame #Play the Beep Sound


pygame.mixer.init()


#This block of code sets up the window
root = tk.Tk()
root.title("Anatom Practical Simulator")
root.geometry("800x600")


#At the end of the 1 minute (or whatever length user has set) this sound should play and then move on to the next slide
def BeepSound():
	#print("Beep should play")
	pygame.mixer.music.load("Beep.mp3")
	pygame.mixer.music.play()

# 3. Create the buttons
button1 = tk.Button(root, text="Button 1", command=BeepSound)

# 4. Position the buttons
# 'side' determines alignment; 'padx' adds horizontal breathing room
button1.pack(side="left", padx=20, expand=True)

# 5. Start the application
root.mainloop()
