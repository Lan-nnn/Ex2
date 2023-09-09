
import sqlite3

# 读取文件内容并将其存储到列表中
file_path = 'stephen_king_adaptations.txt'

with open(file_path, 'r') as file:
    stephen_king_adaptations_list = [line.strip() for line in file.readlines()]

# 创建一个新的SQLite数据库并在其中创建一个表
db_path = 'stephen_king_adaptations.db'

# 建立数据库连接
conn = sqlite3.connect(db_path)

# 创建一个新表来存储数据
c = conn.cursor()
c.execute('''
    CREATE TABLE IF NOT EXISTS stephen_king_adaptations_table (
        movieID TEXT,
        movieName TEXT,
        movieYear INTEGER,
        imdbRating REAL
    )
''')

# 提交数据库事务
conn.commit()

# 将列表中的数据插入到数据库表中
for line in stephen_king_adaptations_list:
    # 将每行数据分割为各个元素
    movieID, movieName, movieYear, imdbRating = line.split(',')
    
    # 插入数据到表中
    c.execute('''
        INSERT INTO stephen_king_adaptations_table (movieID, movieName, movieYear, imdbRating)
        VALUES (?, ?, ?, ?)
    ''', (movieID, movieName, int(movieYear), float(imdbRating)))

# 提交数据库事务
conn.commit()

def search_movies():
    while True:
        # 提示用户选择一个选项
        print("\nPlease choose an option:")
        print("1. Movie name")
        print("2. Movie year")
        print("3. Movie rating")
        print("4. STOP")
        
        choice = input("Your choice: ")
        
        # 根据用户的选择执行相应的操作
        if choice == "1":
            movie_name = input("Enter the movie name: ")
            
            # 在数据库中搜索电影
            c.execute("SELECT * FROM stephen_king_adaptations_table WHERE movieName LIKE ?", ('%' + movie_name + '%',))
            result = c.fetchall()
            
            # 显示结果
            if result:
                for row in result:
                    print(f"Movie ID: {row[0]}, Movie Name: {row[1]}, Movie Year: {row[2]}, IMDB Rating: {row[3]}")
            else:
                print("No such movie exists in our database.")
                
        elif choice == "2":
            movie_year = int(input("Enter the movie year: "))
            
            # 在数据库中搜索电影
            c.execute("SELECT * FROM stephen_king_adaptations_table WHERE movieYear = ?", (movie_year,))
            result = c.fetchall()
            
            # 显示结果
            if result:
                for row in result:
                    print(f"Movie ID: {row[0]}, Movie Name: {row[1]}, Movie Year: {row[2]}, IMDB Rating: {row[3]}")
            else:
                print("No movies were found for that year in our database.")
                
        elif choice == "3":
            movie_rating = float(input("Enter the minimum IMDB rating: "))
            
            # 在数据库中搜索电影
            c.execute("SELECT * FROM stephen_king_adaptations_table WHERE imdbRating >= ?", (movie_rating,))
            result = c.fetchall()
            
            # 显示结果
            if result:
                for row in result:
                    print(f"Movie ID: {row[0]}, Movie Name: {row[1]}, Movie Year: {row[2]}, IMDB Rating: {row[3]}")
            else:
                print("No movies at or above that rating were found in the database.")
                
        elif choice == "4":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

# 调用函数开始交互
search_movies()
