#call write() function

import csv , sqlite3 
import os


DB_FNAME = 'db.sqlite3'
CSV_FNAME = 'data.csv'
DESTINATION = 'forum/data.csv'

fields = ['id', 'title', 'category', 'subcategory','answers' , 'combined']

conn = sqlite3.connect(DB_FNAME)
#conn.row_factory = sqlite3.Row


posts = conn.execute("SELECT * FROM forum_post")


#print(posts.fetchone().keys())
'''['id', 'title', 'slug', 'solved', 'posted_on', 'views', 'category_id', 'posted_by_id', 'subcategory_id' ]'''



def max_upvoted(ans):
     
    max_index = 0
    index = 0
    
    max_up = ans[index][5]
    for i in ans:
        if i[5] > max_up:
            max_up = i[5]
            max_index = index
            
        index += 1
    
    return max_index
    




def write():
    print('\n')
    global posts
    with open(CSV_FNAME, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(fields)
        rec_no = 0
        for i in posts:
            
            category = conn.execute("SELECT * FROM forum_category where id = {}".format(i[6]))
            subcategory = conn.execute("SELECT * FROM forum_subcategory where id = {}".format(i[8]))
            answers = conn.execute("SELECT * FROM forum_answer where post_id = {}".format(i[0]))
            answers = answers.fetchall()
            
            try:
                if len(answers) == 0:
                    fin = [i[0],i[1],category.fetchone()[1],subcategory.fetchone()[1],' ']
                else:
                    fin = [i[0],i[1],category.fetchone()[1],subcategory.fetchone()[1],answers[max_upvoted(answers)][1]]
                fin.append(' '.join(fin[1:]))
                writer.writerow(fin)
                print("writing {}th record".format(rec_no))
            except:
                writer.writerow([i[0],i[1],category.fetchone()[1],subcategory.fetchone()[1],"Null"])
            rec_no+=1
        print("\ndone writing {} records into {} file".format(rec_no,CSV_FNAME))
            

'''
def find(): #function just for debugging
    for i in posts:
        print(i[1])
        category = conn.execute("SELECT * FROM forum_category where id = {}".format(i[6]))
        subcategory = conn.execute("SELECT * FROM forum_subcategory where id = {}".format(i[8]))

        answers = conn.execute("SELECT * FROM forum_answer where post_id = {}".format(i[0]))
        answers = answers.fetchall()
        
        print(answers[max_upvoted(answers)][1])
        

        print('----')
        print(category.fetchone()[1])
        print(subcategory.fetchone()[1])
        print('\n')
'''

if __name__ == '__main__':
    write()
    #os.system('cp {} {}'.format(CSV_FNAME,DESTINATION))
    #find()