import tkinter as tk
import pygame #Play the Beep Sound
from tkinter import simpledialog, messagebox, filedialog
import os
from PIL import Image, ImageTk

pygame.mixer.init()

#
current_deck={}
timer_seconds=5
current_question_index=0
question_keys=[]
image_window=None
image_label=None


#This block of code sets up the window
root = tk.Tk()
root.title("Anatom Practical Simulator")
root.geometry("800x600")


#At the end of the 1 minute (or whatever length user has set) this sound should play and then move on to the next slide
def BeepSound():
	#print("Beep should play")
	pygame.mixer.music.load("Beep.mp3")
	pygame.mixer.music.play()

def UserInput():
	global timer_seconds
	user_value = simpledialog.askinteger("Adjust Timer", "Enter a time (1-60 seconds):",
                                         parent=root,
                                         minvalue=1)
	if user_value is not None:
		if user_value > 60:
			messagebox.showerror(title="Too High", message="Practical Timers are 60s. Anything over is bad practice")
	timer_seconds=user_value

def ChooseDeck():
    global current_deck
    # 1. Ask user to select the folder
    folder_selected = filedialog.askdirectory(title="Select your Anatomy Deck Folder")
    
    if not folder_selected:
        return # User cancelled

    # 2. Clear the old deck and scan the folder
    current_deck = {}
    files = os.listdir(folder_selected)
    
    # 3. Logic to pair .jpg and .txt
    for file in files:
        if file.endswith(".jpg"):
            # If file is "Question1.jpg", base_name is "Question1"
            base_name = os.path.splitext(file)[0]
            txt_file = base_name + ".txt"
            
            # Check if the matching .txt exists
            if txt_file in files:
                current_deck[base_name] = {
                    "image": os.path.join(folder_selected, file),
                    "text": os.path.join(folder_selected, txt_file)
                }
    
    print(f"Loaded {len(current_deck)} questions from {folder_selected}")
    if len(current_deck) == 0:
        messagebox.showwarning("Empty Deck", "No matching .jpg and .txt pairs found!")

def update_image_window(photo,key):
	global image_window, image_label

	if image_window is None or not tk.Toplevel.winfo_exists(image_window):
		image_window = tk.Toplevel(root)
		image_window.title("Current Station")
		image_window.geometry("800x600")
		image_label = tk.Label(image_window)
		image_label.pack(expand=True, fill="both")

	image_window.title(f"Station: {key}")
	image_label.config(image=photo)
	image_label.image = photo



def BeginSim():
	global current_question_index, image_label, question_keys
	global current_deck
	if not current_deck:
		messagebox.showerror("Error, no deck selected")
		return 
	if not question_keys:
		question_keys=list(current_deck.keys())
	if current_question_index < len(question_keys):
		key=question_keys[current_question_index]
		image_path=current_deck[key]["image"] 
 
	if current_question_index < len(question_keys):
		key = question_keys[current_question_index]
		image_path = current_deck[key]["image"]
		
		# Load and display the image
		img = Image.open(image_path)
		img = img.resize((600, 400)) # Resize to fit your 800x600 window
		photo = ImageTk.PhotoImage(img)

		update_image_window(photo, key)		

		print(f"Showing: {key}. Station ends in {timer_seconds}s")
		
		# Wait for the timer_seconds, then trigger the beep and move on
		# .after() takes milliseconds, so we multiply by 1000
		root.after(timer_seconds * 1000, transition_to_next)
	else:
		messagebox.showinfo("Finished", "Practical Simulation Complete!")
		current_question_index=0
		if image_label:
		    image_label.destroy()
		    image_label = None

def transition_to_next():
    global current_question_index, image_label
    BeepSound() # Call your existing function
    current_question_index += 1

    if image_label:
        image_label.config(image='') #clears the picture
        image_label.image= None

    BeginSim()



# 3. Create the buttons
button1 = tk.Button(root, text="Button 1", command=BeepSound)
button2 = tk.Button(root, text="Adjust Timer", command=UserInput)
button3 = tk.Button(root, text="Choose Deck", command=ChooseDeck)
button4 = tk.Button(root, text="Begin Simulation", command=BeginSim)


# 4. Position the buttons
# 'side' determines alignment; 'padx' adds horizontal breathing room
button1.pack(side="left", padx=20, expand=True)
button2.pack(side="left", padx=20, expand=True)
button3.pack(side="left", padx=20, expand=True)
button4.pack(side="left", padx=20, expand=True)
# 5. Start the application
root.mainloop()
