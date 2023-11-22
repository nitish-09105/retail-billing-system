from tkinter import *
root=Tk()
root.title("Retail Billing System")
root.geometry('1920x1080')
root.iconbitmap('icon.ico')

headingLabel=Label(root,text='Retail Billing System',font=('times new roman',30,'bold'),bg='gray20',fg='gold',bd=12,relief=GROOVE)
headingLabel.pack(fill=X)

customer_details_frame=LabelFrame(root,text='Customer Details',font=('times new roman',15,'bold'),fg='gold',bd=8,relief=GROOVE,bg='gray20')
customer_details_frame.pack(fill=X)

nameLabel=Label(customer_details_frame,text='Name')
nameLabel.grid(row=0,column=0)
root.mainloop()