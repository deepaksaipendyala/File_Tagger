# import all components
# from the tkinter library

from tkinter import *
# import filedialog module
from tkinter import filedialog

from os.path import exists


import mysql.connector
try:
  mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="yourpassword",database="mydatabase")
  mycursor = mydb.cursor()
except:
  mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="yourpassword")
  mycursor = mydb.cursor()
  mycursor.execute("CREATE DATABASE mydatabase") 


mycursor.execute("CREATE TABLE IF NOT EXISTS tag_details (tag_name varchar(20),Filepath varchar(100))")



# Create the root window
window = Tk()

tag_var=StringVar()
tag_name=StringVar()
# Set window title
window.title('File Tagger')

# Set window size
window.geometry("600x400")

#Set window background color
window.config(background = "white")

# Function for opening the
# file explorer window
def browseFiles():
	global filename
	filename = list(filedialog.askopenfilenames(initialdir = "/",
										title = "Select a File",
										filetypes = (("Text files",
														"*.txt*"),
													("all files",
														"*.*"))))
	# Change label contents
	label_file_explorer.insert(END,"File Tagger using Python")
	label_file_explorer.insert(END,f"File Selected: {filename}")

def submit():
 	
    tag=tag_var.get()
     
    print("The tag is : " + tag)

    for j in filename:
    	recent_file.configure(text="Recent File: "+j+", Tag: "+tag)
    	mycursor.execute("insert into tag_details(tag_name,Filepath) values (%s,%s)",(tag,j))
    	mydb.commit()


    tag_var.set("")

def show():

	show_label.delete(0,END)
	tag_detail=tag_name.get()

	mycursor.execute(f'select Filepath from tag_details where Tag_name="{tag_detail}" \n')
	show_label.insert(END,f"File Having Tags {tag_detail} are: \n")
	
	for i in mycursor:
		i=str(list(i))
		file_exists = exists(i[2:-2])
		if(file_exists):
			show_label.insert(END,f"{i}\n")
		else:
			show_label.insert(END,f"The File At {i[2:-2]} has moved or been deleted")
			print(f"The File At {i[2:-2]} has moved or been deleted")
	tag_name.set("")
# Create a File tagger label
label_file_explorer = Listbox(window,
							width = 100, height = 6)
button_file = Button(window,
						text = "Browse Files to add a tag",
						command = browseFiles)
tag_label = Label(window, text = 'Tag', font=('calibre',10, 'bold'))
tag_entry = Entry(window,textvariable = tag_var, font=('calibre',10,'normal'))	


sub_btn=Button(window,text = 'Submit tag', command = submit)

show_label = Listbox(window,width="100")
show_entry = Entry(window,textvariable = tag_name, font=('calibre',10,'normal'))	
show_btn=Button(window,text = 'Show tag', command = show)
button_exit = Button(window,
					text = "Exit",
					command = exit)
recent_file=Label(window)

# Grid method is chosen for placing
# the widgets at respective positions
# in a table like structure by
# specifying rows and columns
label_file_explorer.grid(column = 1, row = 1)

button_file.grid(column = 1, row = 2)

tag_label.grid(column=1,row=3)

tag_entry.grid(column=1,row=4)

sub_btn.grid(column=1,row=5)

show_label.grid(column=1,row=6)

show_entry.grid(column=1,row=7)

show_btn.grid(column=1,row=8)

button_exit.grid(column = 1,row = 9)

recent_file.grid(column=1, row=10)



# Let the window wait for any events
window.mainloop()