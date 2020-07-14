from tkinter import *
from tkinter import filedialog
from tkinter import simpledialog
from PyPDF2 import PdfFileReader, PdfFileWriter
import os

#******************* Function section **********************
def process_pdfs():
    # Open file dialog:
    root.filenames = filedialog.askopenfilenames(initialdir = "C:/Desktop", title = "Choose PDF files", 
    #filetypes = (("PDF files", "*.pdf"), ("All files", "*.*")))
    filetypes = [("PDF files", "*.pdf")])

    # Get user Desktop location:
    desktop_dir = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')

    # Create output directory:
    output_dir = desktop_dir + r"\merged.pdf"

    # Merge the pdfs by calling merge_pdfs:
    merge_pdfs(root.filenames, output_dir)

    # Print out successful message:
    msg = Label(root, text = "Merge completed! Please check your Desktop")
    msg.pack()




#ENCRYPTED_FILE_PATH = 'bank_statement.pdf'
#FILE_OUT_PATH = 'bank_statement_decrypt.pdf'

#PASSWORD = '04224X'

def merge_pdfs(paths, output):
    pdf_writer = PdfFileWriter()

    for path in paths:
        pdf_reader = PdfFileReader(path)
        # Decrypt the file if it's encrypted:
        if pdf_reader.isEncrypted:
            # Split the file path and file name:
            # Ref: https://stackoverflow.com/questions/35483700/python-how-to-get-the-filename-in-tkinter-file-dialog
            ##encrypted_filename = os.path.basename(path)   # This only gets the file name
            (file_dir, encrypted_filename) = os.path.split(path)
            
            # Pop up password entry window:
            #pw_window = Toplevel(root)
            #pw_window.title = "Password"
            #pw_label = Label(pw_window, text = "Please enter the password for " + encrypted_filename)
            #pw = Entry(pw_window)
            #pw.pack()
            pw_dialog_prompt = "Please enter the password for file: " + encrypted_filename
            pw = simpledialog.askstring("Password Entry", pw_dialog_prompt)

            PASSWORD = pw
            ENCRYPTED_FILE_PATH = path 
            FILE_OUT_PATH = file_dir + r'/decrypted.pdf'

            try:
                pdf_reader.decrypt(PASSWORD)
            except NotImplementedError:
                print("\nException!")
                command=f'qpdf --password="{PASSWORD}" --decrypt "{ENCRYPTED_FILE_PATH}" "{FILE_OUT_PATH}"'
                print("\n\nThe command is: ", command)
                os.system(command)
                pdf_reader = PdfFileReader(FILE_OUT_PATH)

        for page in range(pdf_reader.getNumPages()):
            # Add each page to the writer object
            pdf_writer.addPage(pdf_reader.getPage(page))

    # Write out the merged PDF
    with open(output, 'wb') as out:
        pdf_writer.write(out)





#******************* Main program section ******************
root = Tk() # The thing that you have to put at the beginning

# Set root window properties:
root.geometry("500x100")
root.title("Welcome to merge PDFs")

myLabel = Label(root, text = "Hello!")
myLabel.pack()

# Create a button for user to click to choose pdf files to merge:
myButton = Button(root, text = "Choose PDF files to merge!", command = process_pdfs)
myButton.pack()




root.mainloop()