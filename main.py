from tkinter import *
from tkinter import messagebox
import random
import os
import tempfile,smtplib
# ****************** Functionality ***************************

# clear the whole content
def clear():
    entries_to_clear = [
        bathsoapEntry, facecreamEntry, facewashEntry, hairsprayEntry, hairgelEntry, bodylotionEntry,
        riceEntry, oilEntry, sugarEntry, pulsesEntry, wheatEntry, teaEntry,
        pepsiEntry, limcaEntry, cocacolaEntry, mountaindewEntry, maazaEntry, spriteEntry
    ]
    for entry in entries_to_clear:
        entry.delete(0, END)
        entry.insert(0, 0)
    prices_to_clear = [cosmeticpriceEntry, grocerypriceEntry, drinkpriceEntry]
    taxes_to_clear = [cosmetictaxEntry, grocerytaxEntry, drinktaxEntry]
    other_entries_to_clear = [nameEntry, phoneEntry, billnumberEntry]
    for entry in prices_to_clear + taxes_to_clear + other_entries_to_clear:
        entry.delete(0, END)
    textarea.delete(1.0, END)



# sending the bill on any mail
# gui
def send_email():
    def send_gmail():
        try:
            ob=smtplib.SMTP('smtp.gmail.com',587)  
            ob.starttls()
            ob.login(senderEntry.get(),passwordEntry.get()) 
            message=email_textarea.get(1.0,END)
            ob.sendmail(senderEntry.get(),receiverEntry.get(),message)
            ob.quit()
            messagebox.showinfo('Success','Bill is successfully sent',parent=root1)  
            root1.destroy()
        except:
            messagebox.showerror('Error','Something went wrong Please try again',parent=root1)   

    if textarea.get(1.0,END)=='\n':
        messagebox.showerror('Error','Bill is Empty')
    else:
        root1=Toplevel()
        root1.grab_set()
        root1.title('Send gmail')
        root1.config(bg='gray20')
        root1.resizable(0,0)

        # sender frame
        senderFrame=LabelFrame(root1,text='SENDER',font=('arial',16,'bold'),bd=6,bg='gray20',fg='white')
        senderFrame.grid(row=0,column=0,padx=40,pady=20)
        # 1
        senderLabel=Label(senderFrame,text="Sender' Email",font=('arial',14,'bold'),bg='gray20',fg='white')
        senderLabel.grid(row=0,column=0,padx=10,pady=8)
        senderEntry=Entry(senderFrame,font=('arial',14,'bold'),bd=2,width=23,relief=RIDGE)
        senderEntry.grid(row=0,column=1,padx=10,pady=8)
        # 2
        passwordLabel=Label(senderFrame,text="Password",font=('arial',14,'bold'),bg='gray20',fg='white')
        passwordLabel.grid(row=1,column=0,padx=10,pady=8)
        passwordEntry=Entry(senderFrame,font=('arial',14,'bold'),bd=2,width=23,relief=RIDGE,show='*')
        passwordEntry.grid(row=1,column=1,padx=10,pady=8)

        # receiver frame
        recipientFrame=LabelFrame(root1,text='RECIPIENT',font=('arial',16,'bold'),bd=6,bg='gray20',fg='white')
        recipientFrame.grid(row=1,column=0,padx=40,pady=20)
        # 1
        receiverLabel=Label(recipientFrame,text="Email Address",font=('arial',14,'bold'),bg='gray20',fg='white')
        receiverLabel.grid(row=0,column=0,padx=10,pady=8)
        # 2
        receiverEntry=Entry(recipientFrame,font=('arial',14,'bold'),bd=2,width=23,relief=RIDGE)
        receiverEntry.grid(row=0,column=1,padx=10,pady=8)

        # message frame
        messageLabel=Label(recipientFrame,text="Message",font=('arial',14,'bold'),bg='gray20',fg='white')
        messageLabel.grid(row=1,column=0,padx=10,pady=8)
        email_textarea=Text(recipientFrame,font=('arial',14,'bold'),bd=2,relief=SUNKEN,width=40,height=10)
        email_textarea.grid(row=2,column=0,columnspan=2)
        email_textarea.delete(1.0,END)
        email_textarea.insert(END,textarea.get(1.0,END).replace('=','').replace('-','').replace('\t\t\t','\t\t'))

        # email send button
        sendButton=Button(root1,text='SEND',font=('arial',16,'bold'),width=15,command=send_gmail)
        sendButton.grid(row=2,column=0,pady=20)
        root1.mainloop()


# printing the bill
def print_bill():
    if textarea.get(1.0,END)=='\n':
        messagebox.showerror('Error','Bill is Empty')
    else:
        file=tempfile.mktemp('.txt')
        open(file,'w').write(textarea.get(1.0,END))
        os.startfile(file,'print')

# searching the past generated bills
def search_bill():
    for i in os.listdir('bills/'):
        if i.split('.')[0]==billnumberEntry.get():
            file=open(f'bills/{i}','r')
            textarea.delete(1.0,END)
            textarea.insert(END,file.read())
            file.close()
            break      
    else:
        messagebox.showerror('Error','Invalid Bill Number')      



# if bill file not exist then it will generate a new file
if not os.path.exists('bills'):
    os.mkdir('bills')

# save the generated bill
def save_bill():
    global billnumber
    result=messagebox.askyesno('Confirm','Do you want to save the bill?')
    if result:
        bill_content=textarea.get(1.0,END)
        file=open(f'bills/{billnumber}.txt','w')
        file.write(bill_content)
        file.close()
        messagebox.showinfo('Success',f'bill number {billnumber} is save successfully')
        billnumber=random.randint(500,1000)

# generate the bill number
billnumber=random.randint(500,1000)

# content inserting in the bill
def bill_area():
    if nameEntry.get()=='' or phoneEntry.get()=='':
        messagebox.showerror('Error','Customer details are Required')
    elif cosmeticpriceEntry.get()=='' and grocerypriceEntry.get()=='' and drinkpriceEntry.get()=='':
        messagebox.showerror('Error','No Products are Selected')
    elif cosmeticpriceEntry.get()=='0 Rs' and grocerypriceEntry.get()=='0 Rs' and drinkpriceEntry.get()=='0 Rs':
        messagebox.showerror('Error','No Products are Selected')
    else:
        textarea.delete(1.0,END)
        textarea.insert(END,'\t\t**Welcome Customer**\n\n')
        textarea.insert(END,f'Bill Number: {billnumber}\n')
        textarea.insert(END,f'\nCustomer Name: {nameEntry.get()}\n')
        textarea.insert(END,f'\nCustomer Phone Number: {phoneEntry.get()}\n')
        textarea.insert(END,'\n=======================================================\n\n')
        textarea.insert(END,'Product\t\t\tQuantity\t\t\tPrice\n')
        textarea.insert(END,'\n=======================================================\n\n')


        # if bathsoapEntry.get()!='0':
        #     textarea.insert(END,f'Bath Soap\t\t\t   {bathsoapEntry.get()}\t\t\t{soapprice} Rs')
        # if hairsprayEntry.get()!='0':
        #     textarea.insert(END,f'Hair Sray\t\t\t   {hairsprayEntry.get()}\t\t\t{hairsprayprice} Rs')
        # if facecreamEntry.get()!='0':
        #     textarea.insert(END,f'Hair Sray\t\t\t   {facecreamEntry.get()}\t\t\t{facecreamprice} Rs')

        # alternative way of above
        product_entries = {
        "Bath Soap": bathsoapEntry,
        "Hair Spray": hairsprayEntry,
        "Face Cream": facecreamEntry,
        'Face Wash': facewashEntry,
        'Hair Gel': hairgelEntry,
        'Body Lotion': bodylotionEntry,
        'Rice': riceEntry,
        'Oil': oilEntry,
        'Sugar': sugarEntry,
        'Pulses': pulsesEntry,
        'Wheat': wheatEntry,
        'Tea': teaEntry,
        'Pepsi': pepsiEntry,
        'Limca': limcaEntry,
        'Coca Cola': cocacolaEntry,
        'Mountain Dew': mountaindewEntry,
        'Maaza': maazaEntry,
        'Sprite': spriteEntry,    
        }
        product_prices = {
            "Bath Soap": soapprice,
            "Hair Spray": hairsprayprice,
            "Face Cream": facecreamprice,
            'Face Wash': facewashprice,
            'Hair Gel': hairgelprice,
            'Body Lotion': bodylotionprice,
            'Rice': riceprice,
            'Oil': oilprice,
            'Sugar': sugarprice,
            'Pulses': pulsesprice,
            'Wheat': wheatprice,
            'Tea': teaprice,
            'Pepsi': pepsiprice,
            'Limca': limcaprice,
            'Coca Cola': cocacolaprice,
            'Mountain Dew': mountaindewprice,
            'Maaza': maazaprice,
            'Sprite': spriteprice,
        }
        for product, entry in product_entries.items():
            entry_value = entry.get()
            if entry_value != '0':
                textarea.insert(END, f'{product}\t\t\t {entry_value}\t\t\t{product_prices[product]} Rs\n')

        textarea.insert(END,'\n-------------------------------------------------------\n\n')


        if cosmetictaxEntry.get()!='0.0 Rs':
            textarea.insert(END,f'\nCosmetic Tax\t\t{cosmetictaxEntry.get()}')
        if grocerytaxEntry.get()!='0.0 Rs':
            textarea.insert(END,f'\nGrocery Tax\t\t{grocerytaxEntry.get()}')
        if drinktaxEntry.get()!='0.0 Rs':
            textarea.insert(END,f'\nCold Drinks Tax\t\t{drinktaxEntry.get()}')
        textarea.insert(END,f'\n\nTotal Bill: \t\t{totalbill}\n')
        textarea.insert(END,'\n-------------------------------------------------------')

        # save the bill function
        save_bill()

# total bill calculator
def total():
    # cosmetic price calculator
    global soapprice, hairsprayprice,facecreamprice,facewashprice,hairgelprice,bodylotionprice
    global riceprice,oilprice,sugarprice,pulsesprice,wheatprice,teaprice
    global pepsiprice,limcaprice,cocacolaprice,mountaindewprice,maazaprice,spriteprice
    global totalbill
    soapprice=int(bathsoapEntry.get())*20
    facecreamprice=int(facecreamEntry.get())*50
    facewashprice=int(facewashEntry.get())*150
    hairsprayprice=int(hairsprayEntry.get())*100
    hairgelprice=int(hairgelEntry.get())*80
    bodylotionprice=int(bodylotionEntry.get())*200
    toalcosmeticprice=soapprice+facecreamprice+facewashprice+hairsprayprice+hairgelprice+bodylotionprice
    cosmeticpriceEntry.delete(0,END)
    cosmeticpriceEntry.insert(0,f'{toalcosmeticprice} Rs')
    cosmetictax=toalcosmeticprice*0.12
    cosmetictaxEntry.delete(0,END)
    cosmetictaxEntry.insert(0,str(cosmetictax)+ ' Rs')

    # grocery price calculator
    riceprice=int(riceEntry.get())*90
    oilprice=int(oilEntry.get())*160
    sugarprice=int(sugarEntry.get())*45
    pulsesprice=int(pulsesEntry.get())*120
    wheatprice=int(wheatEntry.get())*40
    teaprice=int(teaEntry.get())*180
    totalgroceryprice=riceprice+oilprice+sugarprice+pulsesprice+wheatprice+teaprice
    grocerypriceEntry.delete(0,END)
    grocerypriceEntry.insert(0,f'{totalgroceryprice} Rs')
    grocerytax=totalgroceryprice*0.05
    grocerytaxEntry.delete(0,END)
    grocerytaxEntry.insert(0,str(grocerytax)+ ' Rs')

    # cold drink price calculator
    pepsiprice=int(pepsiEntry.get())*50
    limcaprice=int(limcaEntry.get())*50
    cocacolaprice=int(cocacolaEntry.get())*50
    mountaindewprice=int(mountaindewEntry.get())*50
    maazaprice=int(maazaEntry.get())*50
    spriteprice=int(spriteEntry.get())*50
    totaldrinkprice=pepsiprice+limcaprice+cocacolaprice+mountaindewprice+maazaprice+spriteprice
    drinkpriceEntry.delete(0,END)
    drinkpriceEntry.insert(0,f'{totaldrinkprice} Rs')
    drinktax=totaldrinkprice*0.18
    drinktaxEntry.delete(0,END)
    drinktaxEntry.insert(0,str(drinktax) +' Rs')

    # complete bill after tax
    totalbill=toalcosmeticprice+totalgroceryprice+totaldrinkprice+cosmetictax+grocerytax+drinktax

# ******************* GUI ******************************
root=Tk()
root.title("Retail Billing System")
root.geometry('1920x1080')
root.iconbitmap('icon.ico')

headingLabel=Label(root,text='Retail Billing System',font=('times new roman',30,'bold'),bg='gray20',fg='gold',bd=12,relief=GROOVE)
headingLabel.pack(fill=X)


# Customer Details Frame
customer_details_frame=LabelFrame(root,text='Customer Details',font=('times new roman',15,'bold'),fg='gold',bd=8,relief=GROOVE,bg='gray20')
customer_details_frame.pack(fill=X,pady=18)
# 1
nameLabel=Label(customer_details_frame,text='Name',font=('times new roman',15,'bold'),bg='gray20',fg='white')
nameLabel.grid(row=0,column=0,padx=20)
nameEntry=Entry(customer_details_frame,font=('arial',15),bd=7,width=18)
nameEntry.grid(row=0, column=1,padx=18)
# 2
phoneLabel=Label(customer_details_frame,text='Phone Number',font=('times new roman',15,'bold'),bg='gray20',fg='white')
phoneLabel.grid(row=0,column=2,padx=20,pady=2)
phoneEntry=Entry(customer_details_frame,font=('arial',15),bd=7,width=18)
phoneEntry.grid(row=0, column=3,padx=18)
# 3
billnumberLabel=Label(customer_details_frame,text='Bill Number',font=('times new roman',15,'bold'),bg='gray20',fg='white')
billnumberLabel.grid(row=0,column=4,padx=20,pady=2)
billnumberEntry=Entry(customer_details_frame,font=('arial',15),bd=7,width=18)
billnumberEntry.grid(row=0, column=5,padx=18)
# 4
searchButton=Button(customer_details_frame,text='SEARCH',font=('arial',12,'bold'),border=7,width=10,command=search_bill)
searchButton.grid(row=0,column=7,padx=80,pady=8)


# products Frame
productsFrame=Label(root)
productsFrame.pack(pady=10)

# 1
cosmeticFrame=LabelFrame(productsFrame,text='Cosmetics',font=('times new roman',15,'bold'),fg='gold',bd=8,relief=GROOVE,bg='gray20')
cosmeticFrame.grid(row=0,column=0)
# 1.1
batsoapLabel=Label(cosmeticFrame,text='Bath Soap',font=('times new roman',15,'bold'),bg='gray20',fg='white')
batsoapLabel.grid(row=0,column=0,pady=9,padx=15,sticky='w')
bathsoapEntry=Entry(cosmeticFrame,font=('arial',15),bd=5,width=15)
bathsoapEntry.grid(row=0,column=1,pady=9,padx=15)
bathsoapEntry.insert(0,0)
# 1.2
facecreamLabel=Label(cosmeticFrame,text='Face Cream',font=('times new roman',15,'bold'),bg='gray20',fg='white')
facecreamLabel.grid(row=1 ,column=0,pady=9,padx=15,sticky='w')
facecreamEntry=Entry(cosmeticFrame,font=('arial',15),bd=5,width=15)
facecreamEntry.grid(row=1,column=1,pady=9,padx=15)
facecreamEntry.insert(0,0)
# 1.3
facewashLabel=Label(cosmeticFrame,text='Face Wash',font=('times new roman',15,'bold'),bg='gray20',fg='white')
facewashLabel.grid(row=2 ,column=0,pady=9,padx=15,sticky='w')
facewashEntry=Entry(cosmeticFrame,font=('arial',15),bd=5,width=15)
facewashEntry.grid(row=2,column=1,pady=9,padx=15)
facewashEntry.insert(0,0)
# 1.4
hairsprayLabel=Label(cosmeticFrame,text='Hair Spray',font=('times new roman',15,'bold'),bg='gray20',fg='white')
hairsprayLabel.grid(row=3 ,column=0,pady=9,padx=15,sticky='w')
hairsprayEntry=Entry(cosmeticFrame,font=('arial',15),bd=5,width=15)
hairsprayEntry.grid(row=3,column=1,pady=9,padx=15)
hairsprayEntry.insert(0,0)
# 1.5
hairgelLabel=Label(cosmeticFrame,text='Hair Gel',font=('times new roman',15,'bold'),bg='gray20',fg='white')
hairgelLabel.grid(row=4 ,column=0,pady=9,padx=15,sticky='w')
hairgelEntry=Entry(cosmeticFrame,font=('arial',15),bd=5,width=15)
hairgelEntry.grid(row=4,column=1,pady=9,padx=15)
hairgelEntry.insert(0,0)
# 1.6
bodylotionLabel=Label(cosmeticFrame,text='Body Lotion',font=('times new roman',15,'bold'),bg='gray20',fg='white')
bodylotionLabel.grid(row=5 ,column=0,pady=9,padx=15,sticky='w')
bodylotionEntry=Entry(cosmeticFrame,font=('arial',15),bd=5,width=15)
bodylotionEntry.grid(row=5,column=1,pady=9,padx=15)
bodylotionEntry.insert(0,0)

# 2
groceryFrame=LabelFrame(productsFrame,text='Grocery',font=('times new roman',15,'bold'),fg='gold',bd=8,relief=GROOVE,bg='gray20')
groceryFrame.grid(row=0,column=1)
# 2.1
riceLabel=Label(groceryFrame,text='Rice',font=('times new roman',15,'bold'),bg='gray20',fg='white')
riceLabel.grid(row=0,column=0,pady=9,padx=15,sticky='w')
riceEntry=Entry(groceryFrame,font=('arial',15),bd=5,width=15)
riceEntry.grid(row=0,column=1,pady=9,padx=15)
riceEntry.insert(0,0)
# 2.2
oilLabel=Label(groceryFrame,text='Oil',font=('times new roman',15,'bold'),bg='gray20',fg='white')
oilLabel.grid(row=1 ,column=0,pady=9,padx=15,sticky='w')
oilEntry=Entry(groceryFrame,font=('arial',15),bd=5,width=15)
oilEntry.grid(row=1,column=1,pady=9,padx=15)
oilEntry.insert(0,0)
# 2.3
sugarLabel=Label(groceryFrame,text='Sugar',font=('times new roman',15,'bold'),bg='gray20',fg='white')
sugarLabel.grid(row=2 ,column=0,pady=9,padx=15,sticky='w')
sugarEntry=Entry(groceryFrame,font=('arial',15),bd=5,width=15)
sugarEntry.grid(row=2,column=1,pady=9,padx=15)
sugarEntry.insert(0,0)
# 2.4
pulsesLabel=Label(groceryFrame,text='Pulses',font=('times new roman',15,'bold'),bg='gray20',fg='white')
pulsesLabel.grid(row=3 ,column=0,pady=9,padx=15,sticky='w')
pulsesEntry=Entry(groceryFrame,font=('arial',15),bd=5,width=15)
pulsesEntry.grid(row=3,column=1,pady=9,padx=15)
pulsesEntry.insert(0,0)
# 2.5
wheatLabel=Label(groceryFrame,text='Wheat',font=('times new roman',15,'bold'),bg='gray20',fg='white')
wheatLabel.grid(row=4 ,column=0,pady=9,padx=15,sticky='w')
wheatEntry=Entry(groceryFrame,font=('arial',15),bd=5,width=15)
wheatEntry.grid(row=4,column=1,pady=9,padx=15)
wheatEntry.insert(0,0)
# 2.6
teaLabel=Label(groceryFrame,text='Tea',font=('times new roman',15,'bold'),bg='gray20',fg='white')
teaLabel.grid(row=5 ,column=0,pady=9,padx=15,sticky='w')
teaEntry=Entry(groceryFrame,font=('arial',15),bd=5,width=15)
teaEntry.grid(row=5,column=1,pady=9,padx=15)
teaEntry.insert(0,0)

# 3
drinksFrame=LabelFrame(productsFrame,text='Cold Drinks',font=('times new roman',15,'bold'),fg='gold',bd=8,relief=GROOVE,bg='gray20')
drinksFrame.grid(row=0,column=2)
# 3.1
pepsiLabel=Label(drinksFrame,text='pepsi',font=('times new roman',15,'bold'),bg='gray20',fg='white')
pepsiLabel.grid(row=0,column=0,pady=9,padx=14,sticky='w')
pepsiEntry=Entry(drinksFrame,font=('arial',15),bd=5,width=14)
pepsiEntry.grid(row=0,column=1,pady=9,padx=14)
pepsiEntry.insert(0,0)
# 3.2
limcaLabel=Label(drinksFrame,text='Limca',font=('times new roman',15,'bold'),bg='gray20',fg='white')
limcaLabel.grid(row=1 ,column=0,pady=9,padx=14,sticky='w')
limcaEntry=Entry(drinksFrame,font=('arial',15),bd=5,width=14)
limcaEntry.grid(row=1,column=1,pady=9,padx=14)
limcaEntry.insert(0,0)
# 3.3
cocacolaLabel=Label(drinksFrame,text='Coca Cola',font=('times new roman',15,'bold'),bg='gray20',fg='white')
cocacolaLabel.grid(row=2 ,column=0,pady=9,padx=14,sticky='w')
cocacolaEntry=Entry(drinksFrame,font=('arial',15),bd=5,width=14)
cocacolaEntry.grid(row=2,column=1,pady=9,padx=14)
cocacolaEntry.insert(0,0)
# 3.4
mountaindewLabel=Label(drinksFrame,text='Mountain Dew',font=('times new roman',15,'bold'),bg='gray20',fg='white')
mountaindewLabel.grid(row=3 ,column=0,pady=9,padx=14,sticky='w')
mountaindewEntry=Entry(drinksFrame,font=('arial',15),bd=5,width=14)
mountaindewEntry.grid(row=3,column=1,pady=9,padx=14)
mountaindewEntry.insert(0,0)
# 3.5
maazaLabel=Label(drinksFrame,text='Maaza',font=('times new roman',15,'bold'),bg='gray20',fg='white')
maazaLabel.grid(row=4 ,column=0,pady=9,padx=14,sticky='w')
maazaEntry=Entry(drinksFrame,font=('arial',15),bd=5,width=14)
maazaEntry.grid(row=4,column=1,pady=9,padx=14)
maazaEntry.insert(0,0)
# 3.6
spriteLabel=Label(drinksFrame,text='Sprite',font=('times new roman',15,'bold'),bg='gray20',fg='white')
spriteLabel.grid(row=5 ,column=0,pady=9,padx=14,sticky='w')
spriteEntry=Entry(drinksFrame,font=('arial',15),bd=5,width=14)
spriteEntry.grid(row=5,column=1,pady=9,padx=14)
spriteEntry.insert(0,0)

# Bill Frame
billframe=Frame(productsFrame,bd=8,relief=GROOVE)
billframe.grid(row=0,column=3)
billareaLabel=Label(billframe,text='Bill Area', font=('times new roman',15,'bold'),bd=7,relief=GROOVE)
billareaLabel.pack(fill=X)
Scrollbar=Scrollbar(billframe,orient=VERTICAL)
Scrollbar.pack(side=RIGHT,fill=Y)
textarea=Text(billframe,height=18,width=55,yscrollcommand=Scrollbar.set)
textarea.pack()
Scrollbar.config(command=textarea.yview)

# BillMenu Frame
billmenuFrame=LabelFrame(root,text='Bill Menu',font=('times new roman',15,'bold'),fg='gold',bd=8,relief=GROOVE,bg='gray20')
billmenuFrame.pack(fill=X)
# 1
cosmeticpriceLabel=Label(billmenuFrame,text='Cosmetic Price',font=('times new roman',15,'bold'),bg='gray20',fg='white')
cosmeticpriceLabel.grid(row=0 ,column=0,pady=9,padx=15,sticky='w')
cosmeticpriceEntry=Entry(billmenuFrame,font=('arial',15),bd=5,width=15)
cosmeticpriceEntry.grid(row=0,column=1,pady=9,padx=15)
# 2
grocerypriceLabel=Label(billmenuFrame,text='Grocery Price',font=('times new roman',15,'bold'),bg='gray20',fg='white')
grocerypriceLabel.grid(row=1 ,column=0,pady=9,padx=15,sticky='w')
grocerypriceEntry=Entry(billmenuFrame,font=('arial',15),bd=5,width=15)
grocerypriceEntry.grid(row=1,column=1,pady=9,padx=15)
# 3
drinkpriceLabel=Label(billmenuFrame,text='Cold Drink Price',font=('times new roman',15,'bold'),bg='gray20',fg='white')
drinkpriceLabel.grid(row=2 ,column=0,pady=9,padx=15,sticky='w')
drinkpriceEntry=Entry(billmenuFrame,font=('arial',15),bd=5,width=15)
drinkpriceEntry.grid(row=2,column=1,pady=9,padx=15)
# 4
cosmetictaxLabel=Label(billmenuFrame,text='Cosmetic Tax',font=('times new roman',15,'bold'),bg='gray20',fg='white')
cosmetictaxLabel.grid(row=0 ,column=2,pady=9,padx=15,sticky='w')
cosmetictaxEntry=Entry(billmenuFrame,font=('arial',15),bd=5,width=15)
cosmetictaxEntry.grid(row=0,column=3,pady=9,padx=15)
# 5
grocerytaxLabel=Label(billmenuFrame,text='Grocery Tax',font=('times new roman',15,'bold'),bg='gray20',fg='white')
grocerytaxLabel.grid(row=1 ,column=2,pady=9,padx=15,sticky='w')
grocerytaxEntry=Entry(billmenuFrame,font=('arial',15),bd=5,width=15)
grocerytaxEntry.grid(row=1,column=3,pady=9,padx=15)
# 6
drinktaxLabel=Label(billmenuFrame,text='Cold Drink Tax',font=('times new roman',15,'bold'),bg='gray20',fg='white')
drinktaxLabel.grid(row=2 ,column=2,pady=9,padx=15,sticky='w')
drinktaxEntry=Entry(billmenuFrame,font=('arial',15),bd=5,width=15)
drinktaxEntry.grid(row=2,column=3,pady=9,padx=15)

# button frames
buttonFrame=Frame(billmenuFrame,bd=8,relief=GROOVE)
buttonFrame.grid(row=0,column=4,rowspan=3,padx=15)
# 1
totalButton=Button(buttonFrame,text='Total',font=('arial',16,'bold'),bg='gray20',fg='white',bd=5,width=8,pady=10, command=total)
totalButton.grid(row=0,column=0,pady=30,padx=12)
# 2
billButton=Button(buttonFrame,text='Bill',font=('arial',16,'bold'),bg='gray20',fg='white',bd=5,width=8,pady=10,command=bill_area)
billButton.grid(row=0,column=1,pady=30,padx=12)
# 3
emailButton=Button(buttonFrame,text='Email',font=('arial',16,'bold'),bg='gray20',fg='white',bd=5,width=8,pady=10,command=send_email)
emailButton.grid(row=0,column=2,pady=30,padx=12)
# 4
printButton=Button(buttonFrame,text='Print',font=('arial',16,'bold'),bg='gray20',fg='white',bd=5,width=8,pady=10,command=print_bill)
printButton.grid(row=0,column=3,pady=30,padx=12)
# 5
clearButton=Button(buttonFrame,text='Clear',font=('arial',16,'bold'),bg='gray20',fg='white',bd=5,width=8,pady=10,command=clear)
clearButton.grid(row=0,column=4,pady=30,padx=12)

root.mainloop()
