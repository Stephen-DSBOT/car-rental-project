import csv                                          #Importing needed modules
import sys
from datetime import datetime, timedelta
def main():
    print("You may select one of the following:\n"
          "1) List available cars\n2) Rent a car\n"
          "3) Return a car\n4) Count the money\n0) Exit")                   
    try:
        c=int(input("What is your selection?\n"))    #Tries input until integer is given
    except ValueError:
        print("Please choose an option from the list") #ValueError when str is given, gives menu
        print()
        main()    
    if c==1:                            #Inputs and their respective functions, print() for better readability in program
        listofcars()
        print()
        main()
    elif c==2:
        rentacar()
        print()
    elif c==3:
        returnacar()
        print()
    elif c==4:
        countthemoney()
        print()
    elif c==0:
        print("\nEnd of program")    #Sysexit when 0 is given in the menu. exit() would ask to kill the running program
        sys.exit()
        print()  
    else:
        print("Please choose an option from the list") #If inputted integer is not in the options, gives menu
        print()
        main()

#'temporary' lists that contain rented and available. Outside of function to access in other functions
#out of function so you dont have to call listofcars() before renting or returning
with open("Vehicles.txt",'r',encoding='utf-8') as vehiclesfile, open("rentedVehicles.txt",'r',encoding='utf-8') as rentedfile:
    csvreader=csv.reader(vehiclesfile)   #converts files to csv files to access indexes
    csvreader2=csv.reader(rentedfile)
    rentedtemp=[]      
    available=[]       
    for roww in csvreader2:          #comparing rented file to all vehicles to find available
        rentedtemp.append(roww[0])
    for row in csvreader:
            if row[0] in rentedtemp:
                continue
            else:             #prints the lines to available (from all vehicles) that dont contain rented vehicles
                properties=(row[3::])
                properties=", ".join(properties)
                available.append(row[0])
                available.append(row[1])
                available.append(row[2])
                available.append(properties)
    

            
def listofcars():
    print()
    with open("Vehicles.txt",'r',encoding='utf-8') as vehiclesfile, open("rentedVehicles.txt",'r',encoding='utf-8') as rentedfile:
        csvreader=csv.reader(vehiclesfile)
        csvreader2=csv.reader(rentedfile)
        print("The following cars are available:")
        for row in csvreader:
            if row[0] in rentedtemp:       #Skips rented lines, prints available (calling from 'temporary' lists)
                continue
            else:
                #updates available cars list by checking rented list
                properties=(row[3::])
                properties=", ".join(properties)
                print("* Reg. nr: ",row[0],", Model: ",row[1],", Price per day: ",row[2],sep='')
                print("Properties:",properties)
                print("-------------------------------------------------------------------------")
        print()
        main() #back to menu

def rentacar():
    print()
    
    rented=input("Please input the register number:\n")
    if rented in available:
        print("This car is available.\n") #Checks wether input is in 'temporary' rented or available or incorrect input
    elif rented in rentedtemp:
        print("This car is rented.\n")
        rentacar()
    else:
        print("Incorrect input.\n")
        rentacar()
    dob(rented) #returns rented input when available register number is inputted
    main()      #menu after dob(rented) has run

    
def dob(rented):

        from datetime import date
        birthdate=input("Please enter your birth date in the format DD/MM/YYYY:\n")
    
        try:
            birth = datetime.strptime(birthdate, '%d/%m/%Y')#validates birthdate input with try, except calls dob()  
            today=date.today()                              #current date from datetime date
            age=today.year-birth.year - ((today.month, today.day) < (birth.month, birth.day)) 
                                #calculates current age for eligibility, ends program if over 100 or under 18
            if age>100:
                print("You must be under 100 to rent a car, end of program.")
                sys.exit()
            elif age<18:
                print("You must be over 18 to rent a car, end of program.")
                sys.exit()
            else:
                with open("Customers.txt","r+",encoding='utf-8') as customersfile: #if acceptable age, program continues
                    csvreader3=csv.reader(customersfile)
                    now=datetime.now()
                    now1=now.strftime('%d/%m/%Y %H:%M')  #string for current date/time
                    var1=False
                    
                    for lines in csvreader3:
                #checks if customer on file, updates temp lists, updates rentedVehicles file, doesnt append Customer.txt
                        if birthdate == lines[0]: 
                            print("Customer already on file.")
                            print("Hello",lines[1],"\nYou rented the car",rented)
                            print()
                            with open("rentedVehicles.txt",'a',encoding='utf-8') as rentedfile:
                                rentedinfo=f'{rented},{birthdate},{now1}\n'
                                rentedfile.write(rentedinfo)
                            #updates temp files
                            available.remove(rented)
                            rentedtemp.append(rented)
                            var1=True #if customer is on file, it won't ask for further info var1=(True)
                                                  
                    if var1==False: #if customer not on file
                        firstname=input("Enter your first name:\n")
                        lastname=input("Enter your last name:\n")
                        email=input("Enter your email address:\n")
                        var=True
                        while var==True:
                            if '.' in email and '@' in email: #validates email address until correct input
                                print("Valid email address.")
                                var=False
                            else:
                                print("Invalid email address.")
                                email=input("Enter your email address:\n")
                        #in new customer loop, appends customer info to Customers.txt
                        customersfile=open("Customers.txt","a",encoding='utf-8') 
                        customerinfo=f'{birthdate},{firstname},{lastname},{email}\n'
                        customersfile.write(customerinfo)
                        customersfile.close()
                        print("Hello",firstname,"\nYou rented the car",rented)
                        print()
                        #appends rented info to rentedVehicles.txt
                        with open("rentedVehicles.txt",'a',encoding='utf-8') as rentedfile:
                            rentedinfo=f'{rented},{birthdate},{now1}\n'
                            rentedfile.write(rentedinfo)
                        available.remove(rented) #updates temp files
                        rentedtemp.append(rented)
                
        except ValueError: #goes back to birthdate input validation (try, except)
            print("Incorrect date format")
            print()
            dob(rented)
    

def returnacar():
    print()
    returnreg=input("Enter the register number of the car you would like to return:\n")
    with open("rentedVehicles.txt",'r',encoding='utf-8') as rentedfile:
        csvreader4=csv.reader(rentedfile)
        #checks if returnreg (return register) is in rented file, until correct rented car is inputted
        for rowww in csvreader4:
            if returnreg==rowww[0]:
                print("In rented")
                returnacarcont(returnreg) #breaks loop and goes to continued returnacar with (returnreg) input
                return(returnreg)    
            else:
                pass
                
        print("Not in rented")
        returnacar()
        
        
def returnacarcont(returnreg):
    
    with open("Vehicles.txt","r",encoding='utf-8') as vehiclesfile:
        csvreader5=csv.reader(vehiclesfile)
        for i in csvreader5:
            if returnreg==i[0]:#checks price of given (already validated) car
                price=i[2]
                
        now=datetime.now()
        now=now.strftime('%d/%m/%Y %H:%M')
        
        
        with open("rentedVehicles.txt",'r+',encoding='utf-8') as rentedfile:
            csvreader4=csv.reader(rentedfile)
            
            for rowww in csvreader4:
                if returnreg==rowww[0]:  #finds and defines the rented cars values in rentedfile 
                    rentedbirth=rowww[1]
                    start=rowww[2]
                    rentedline=rowww[0::]
                    rentedline=','.join(rentedline) #comma seperated to compare strings in next lines
                    
        with open("rentedVehicles.txt",'r',encoding='utf-8') as rentedfile: 
            linis=rentedfile.readlines()
        with open("rentedVehicles.txt",'w',encoding='utf-8') as rentedfile: 
            for lini in linis:              #rewrites rentedfile and removes the returned car line
                if lini.strip('\n')!=rentedline:
                    rentedfile.write(lini)
        #finds dif. of start date and return date    
        startdate=datetime.strptime(start[:10],'%d/%m/%Y')
        returndate=datetime.strptime(now[:10],'%d/%m/%Y')
        length=returndate-startdate
        pricelength=int(length.days)+1
        #calculates price for number of days started days relative to start date
        dueamount=(pricelength)*int(price)
        print("The rent lasted ",pricelength," days and the cost is ",dueamount,".00 euros.",sep='')
        #appends transaction info to file, updates temp files   
        with open("transActions.txt",'a',encoding='utf-8') as transactionsfile:
            traninfo=f'{returnreg},{rentedbirth},{start},{now},{pricelength},{dueamount}.00\n'
            transactionsfile.write(traninfo)
        rentedtemp.remove(returnreg)
        available.append(returnreg)
    print()
    main()


def countthemoney():
    with open("transActions.txt",'r',encoding='utf-8') as transactionsfile:
        csvreadertran=csv.reader(transactionsfile)
        revenue=0
        for trains in csvreadertran:
            try:
                number=trains[5] #iterates through file and adds sum of each transaction to revenue
                revenue+=int(float(number))
            except IndexError:
                print()
        
        print("\nThe total amount of money is ",revenue,".00 euros\n",sep='')
        main()
        
            
        
main() #Main function starts program


        