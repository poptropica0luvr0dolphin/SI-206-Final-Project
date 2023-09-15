import sqlite3
import os
from collections import OrderedDict
import matplotlib.pyplot as plt
import numpy as np
import csv

'''
setup_database
takes in db_name ('imdb-data.db')
sets up cur and conn (cursor and connection)
returns cur and conn
'''
def setup_database(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn

'''
films_by_month
takes cur and conn
excludes months with values of 'NA'
selects count of number of movies from top 250 for each month
writes data to info.TXT
plots a bar graph comparing # of movies per month
returns none
'''

def films_by_month(cur, conn):
    cur.execute('''
    SELECT COUNT(*), date 
    FROM Wiki_data 
    GROUP BY date
    ''')
    conn.commit()
    data = cur.fetchall()
    months_dict={}

    base_path = os.path.abspath(os.path.dirname(__file__))
    full_path = os.path.join(base_path, 'info.TXT')

    first_row= ['Film Count by Month']

    for i in data:
        if i[1] != 'NA':
            months_dict[i[1]] = i[0]

    months = ['January','February','March','April','May','June','July','August','September','October','November','December']    
    months_ordered_dict = dict(OrderedDict(sorted(months_dict.items(),key =lambda x:months.index(x[0]))))

    with open(full_path, 'w', newline='') as f:
        output = csv.writer(f)
        output.writerow(first_row)
        for i in months_ordered_dict.items():
            output.writerow([i])

    
    plt.bar(list(months_ordered_dict.keys()),list(months_ordered_dict.values()), color = ['darkred', 'darkorchid', 'lightskyblue', 'white', 'green', 'plum', 'red', 'lightgreen', 'navy', 'deeppink', 'yellow', 'blue'], edgecolor = 'black')
    plt.xticks(rotation=70) 
    plt.xlabel('Month') 
    plt.ylabel('Number of Movies in Top 250') 
    plt.title('Top 250 Movies By Month') 
    plt.show()

'''
rank_and_budget
takes in cur and conn 
excludes budget values of zero
simply compares IMDB movie rank with budget
Plots a scatter plot to show correlation
returns none
'''

def rank_and_budget(cur, conn):
    cur.execute('''
    SELECT IMDB_data.Rank, Wiki_data.Budget, IMDB_data.Name 
    FROM Wiki_data 
    JOIN IMDB_data
    ON Wiki_data.Name = IMDB_data.Name
    ''')
    conn.commit()
    data = cur.fetchall()
    data_dict = {}

    for i in data:
        budget = int(i[1])
        if budget !=0:
            data_dict[budget]= i[0]

    x = np.array(list(data_dict.keys()))

    plt.scatter(list(data_dict.keys()), list(data_dict.values()), c = x, cmap = 'cividis', edgecolor = 'navy')
    plt.xticks(rotation=70) 
    plt.xlabel('Budget') 
    plt.ylabel('Rank') 
    plt.title('Top 250 Movies Rank Compared to Budget') 
    plt.show()

'''
budget_per_min_to_ratings
takes in cur and conn
excludes budget values of 0
Calculates the budget per minute of films and compares it to their rank 
writes data in info2.TXT
plots a scatter plot with a line of best fist to show correlation
returns none
'''

def budget_per_min_to_ratings(cur, conn):
    cur.execute('''
    SELECT IMDB_data.Rank, Wiki_data.Budget, Wiki_data.Length 
    FROM Wiki_data 
    JOIN IMDB_data
    ON Wiki_data.Name = IMDB_data.Name
    ''')
    conn.commit()
    data=cur.fetchall()
    rank_dict = {}

    base_path = os.path.abspath(os.path.dirname(__file__))
    full_path = os.path.join(base_path, 'info2.TXT')

    for i in data:
        budget = int(i[1])
        length = int(i[2])
        if budget != 0:
            budget_over_length = budget/length
            rank_dict[i[0]] = int(round(budget_over_length, 0))

    first_row = ['Rank of Films By Budget Per Minute']

    with open(full_path, 'w', newline='') as f:
        output = csv.writer(f)
        output.writerow(first_row)
        for i in rank_dict.items():
            output.writerow([i])

    x = np.array(list(rank_dict.keys()))
    y= np.array(list(rank_dict.values()))
  
    plt.scatter((rank_dict.keys()), rank_dict.values(), c = y, cmap = 'cividis')
    m, b = np.polyfit(x, y, 1) 
    plt.plot(x, m*x+b)
    plt.xticks(rotation=70) 
    plt.xlabel('Rank') 
    plt.ylabel('Budget Per Minute') 
    plt.title('Rank of Films By Budget Per Minute') 
    plt.grid()
    plt.show()

'''
budget_per_min_to_box
takes in cur and conn
excludes box office and budget values of 0
calculates budget per minute of film and compares that to box office success
graphed on a scatterplot with line of best fit to show correlation
returns none
'''

def budget_per_min_to_box(cur, conn):
    cur.execute('''
    SELECT Wiki_data.Box_office, Wiki_data.Budget, Wiki_data.Length 
    FROM Wiki_data 
    ''')
    conn.commit()
    data=cur.fetchall()
    box_dict ={}

    for i in data:
        budget = int(i[1])
        length = int(i[2])
        box = int(i[0])
        if (box != 0) and (budget != 0):
            budget_over_length = budget/length
            box_dict[box] = int(round(budget_over_length, 0))

    x = np.array(list(box_dict.values()))
    y= np.array(list(box_dict.keys()))

    plt.scatter((box_dict.values()), box_dict.keys(), c= x, cmap = 'coolwarm', edgecolor = 'black')
    m, b = np.polyfit(x, y, 1) 
    plt.plot(x, m*x+b)
    plt.xticks(rotation=70) 
    plt.xlabel('Budget Per Minute') 
    plt.ylabel('Box Office') 
    plt.title('Budget Per Minute of Films By Box Office') 
    #plt.grid()
    plt.show()

'''
rating_to_box
takes in cur and conn
excludes box office values of 0
takes each individual rating and plots all the points w/ the same rating on that line 
with the x axis value of budget
returns none
'''

def rating_to_box(cur, conn):
    cur.execute('''
    SELECT Wiki_data.Box_office, IMDB_data.Rating
    FROM Wiki_data 
    JOIN IMDB_data
    ON Wiki_data.Name = IMDB_data.Name
    ''')
    conn.commit()
    data=cur.fetchall()
    data_dict = {}

    for i in data:
        box = int(i[0])
        rating = i[1]
        if box != 0:
            data_dict[box] = rating

    x = np.array(list(data_dict.keys()))
    y= np.array(list(data_dict.values()))

    plt.scatter((data_dict.keys()), data_dict.values(), c=y)
    m, b = np.polyfit(x, y, 1) 
    plt.xticks(rotation=70) 
    plt.xlabel('Box Office') 
    plt.ylabel('Ratting') 
    plt.title('Box Office By Individual Rating')
    plt.grid(True) 
    plt.show()

def main():
    cur, conn = setup_database('IMDB-data.db')
    print(films_by_month(cur,conn))
    print(rank_and_budget(cur, conn))
    print(budget_per_min_to_ratings(cur,conn))
    print(budget_per_min_to_box(cur,conn))
    print(rating_to_box(cur, conn))

main()