import mysql.connector
import pandas as pd


table_name = ""
# Establish a connection to the database
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="india@123",
    database="split_bill"
)

# Create a cursor object
cursor = db.cursor()


def show_group_name():
  query = 'SHOW TABLES'

  cursor.execute(query)

  results = cursor.fetchall()

  print(results)

  return results

  # for index,group_name in enumerate(results,1):

  #   print(index,"--",group_name)

def createGroup(group_name,member_names):
  # group_name = input("Enter Your group name : ")
  print(group_name)
  print(member_names)
  print(type(member_names))
  number_of_member = len(member_names)
  # member_list = []
  # for i in range(number_of_member):
  #   # print("Enter ",i+1," member name")
  #   member_list.append(input(":->" ))
  query = 'CREATE TABLE '+ group_name + "(Trans_id INT PRIMARY KEY AUTO_INCREMENT,Expence_name VARCHAR(50), PaidBy VARCHAR(50), "
  for i in range(number_of_member-1):
    query = query + member_names[i] + " FLOAT, "
  query = query + member_names[-1] + " FLOAT);"
  # print(query)
  cursor.execute(query)
  # print("Group is Created !")


def show_column_name(table_name):
   # Execute a query to retrieve column names from the table
    query = "SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '" + table_name + "' ORDER BY ORDINAL_POSITION;"
    cursor = db.cursor()
    cursor.execute(query)
    results = cursor.fetchall()

    # Extract the column names from the results
    results =results[3:] 
    
    return results
    # return results



def show_all_gr_trans():
  show_group_name()
  choice = input("Enter the group name which transation history want : ")
  query = "SELECT * FROM "+choice+" ;"
  # print("---->All transaction history of "+choice+" <-----")
  cursor.execute(query)
  results = cursor.fetchall()
  for i in results:
    print(i)
  

def split_an_expense(group_name,amount,expence_name,paidby,choice):
  # show_group_name()
  # group_name = input("Enter the group name : ")
  # amount = float(input("Total  amount of expences: "))

  split_between_names = []

  # expence_name = input("Enter the expenxe name : ")

  query = "SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '" + group_name + "' ORDER BY ORDINAL_POSITION;"

  cursor.execute(query)
  results = cursor.fetchall()
  clean_lst = [x[0] for x in results[3:]]
  print(clean_lst)
  member_count = int(input("Enter number of people : "))
  member_amount = []
  for i in range(member_count):
    print("Enter ",i+1," member name")
    split_between_names.append(input(":-> "))  
  # paidby = input("Enter name of who paid Bill : ")
  # choice = int(input("Select 0 for equal split or 1 for customize split : "))
  if choice == 0:
    equal_split = round(amount/member_count,2)
    query = "INSERT INTO " + group_name + " ( Expence_name, PaidBy, "
    for i in range(member_count-1):
      query = query + split_between_names[i] + ","
    query = query + split_between_names[-1]+")"+ " VALUE("+"'"+expence_name+"'," +"'"+ paidby+"'" +","
    print(equal_split)
    print(query)
    for k in range(member_count-1):
      query = query + str(equal_split) + "," 
    query = query + str(equal_split) + ");"
    print(query)
  elif choice == 1:
    for member in split_between_names:
      print(member," : ",end="")
      amount=float(input())
      member_amount.append(amount)
    query = "INSERT INTO " + group_name + " ( PaidBy, "
    for i in range(member_count-1):
      query = query + split_between_names[i] + ","
    query = query + split_between_names[-1]+")"+ " VALUE(" +"'"+ paidby+"'" +","
    print(member_amount)
    print(query)
    for k in range(len(member_amount)-1):
      query = query + str(member_amount[k]) + ","
    query = query + str(member_amount[len(member_amount)-1]) + ");"
    print(query)
    
  cursor.execute(query)
  db.commit()
  print("value added !")



def add_new_member():
  show_group_name()
  choice = input("Enter the group name in which you want to add member : ")
  query = "SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '"+choice+"' ORDER BY ORDINAL_POSITION;"
  cursor.execute(query)
  results = cursor.fetchall()
  clean_lst = [x[0] for x in results[3:]]
  print(clean_lst)
  exit = 0
  while exit < 1 :
    new_member = input(" Enter the new member name : ")
    if new_member in clean_lst:
      print("Name of member is already present, Please enter new name of member : ")
      print("To exit press 1 or continue press 0 : ",end="")
      exit = int(input())
    else:
        query = "ALTER TABLE " + choice + " ADD COLUMN " + new_member + " FLOAT ;"
        cursor.execute(query)
        db.commit()
        print("new member add !")
        exit = 1


def remove_member():
  show_group_name()
  choice = input("Enter the group name in which you want to delete member : ")
  query = "SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '"+choice+"' ORDER BY ORDINAL_POSITION;"
  cursor.execute(query)
  results = cursor.fetchall()
  clean_lst = [x[0] for x in results[3:]]
  print(clean_lst)
  delete_member = input(" Enter the member name want to delete : ")
  query = "ALTER TABLE " + choice + " DROP COLUMN " + delete_member + " ;"
  cursor.execute(query)
  db.commit()
  print("member deleted !")

def remove_transaction():
  show_group_name()
  choice = input("Enter the group name whose transaction want to delete : ")
  df = pd.read_sql('SELECT * FROM '+choice, con=db )
  print(df)
  trans_no = input("Enter the transaction id you want to delete : ")
  query = "DELETE FROM "+choice+" WHERE Trans_id="+trans_no+" ;"
  print(query)
  cursor.execute(query)
  db.commit()
  print("Transaction successfully removed")



def bill_settlement():
  show_group_name()
  choice = input("Enter the group name that Bill you want to genrate : ")
  df = pd.read_sql('SELECT * FROM '+choice, con=db)
  df = df.drop(['Trans_id','Expence_name'],axis=1)
  column_names = df.columns.tolist()
  column_names.sort(key=lambda x: x[0])
  first_column_values = column_names[1:]
  data = {column_names[0]: first_column_values}
  df_calculation = pd.DataFrame(data)
  for i in column_names[1:]:
    df_calculation[i] = pd.Series(dtype=float)
  count=1
  for i in range(1,len(column_names)):
    df_member = df.groupby('PaidBy')[column_names[i]].sum()
    for j in range(len(column_names)-1):
      df_calculation.iloc[j,count]=df_member[j]
    count+=1
  for i in range(len(column_names)-1):
    df_calculation.iloc[i,i+1]=0
  for i in range(len(column_names)-1):
    for j in range(1,len(column_names)-1):
      if df_calculation.iloc[j,i+1] == df_calculation.iloc[i,j+1]:
        df_calculation.iloc[j,i+1]= 0
        df_calculation.iloc[i,j+1] = 0
      elif df_calculation.iloc[j,i+1] > df_calculation.iloc[i,j+1]:
        df_calculation.iloc[j,i+1] = df_calculation.iloc[j,i+1] - df_calculation.iloc[i,j+1]
        df_calculation.iloc[i,j+1] = 0
      else:
        df_calculation.iloc[i,j+1] = df_calculation.iloc[i,j+1] - df_calculation.iloc[j,i+1]
        df_calculation.iloc[j,i+1] = 0
  stacked_df = df_calculation.set_index('PaidBy').stack().reset_index()
  filtered_df = stacked_df.loc[stacked_df[0] != 0]
  filtered_df.columns = ['Payee', 'Payer', 'Amount']
  print("Press 0 to show all split expences or 1 for see indivisual member result : ",end="")
  split_member_choice = int(input())
  if split_member_choice == 0:
    print(filtered_df)
  else:
    query = "SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '"+choice+"' ORDER BY ORDINAL_POSITION;"
    cursor.execute(query)
    results = cursor.fetchall()
    clean_lst = [x[0] for x in results[3:]]
    print(clean_lst)
    member = input("Enter the member name whose expence want to see : ")
    print(" Owe to you :-")
    filtered_payee_df = filtered_df[filtered_df['Payee'] == member]
    if filtered_payee_df.empty:
      print("No transcation to show")
    else:
      print(filtered_payee_df)
    print()
    print(" Owe by you :-")
    filtered_payer_df = filtered_df[filtered_df['Payer'] == member]
    if filtered_payer_df.empty:
      print("No transcation to show")
    else:
      print(filtered_payer_df)

  

if __name__ == "__main__":
  # show_group_name()
  # create_group()
  #split_an_expense()
  #add_new_member()
  #remove_member()
  #remove_transaction()
  #bill_settlement()
  #show_all_gr_trans()
  cursor.close()