

"""
people = ['Dr. Christopher Brooks', 'Dr. Kevyn Collins-Thompson', 'Dr. VG Vinod Vydiswaran', 'Dr. Daniel Romero']
print len(people)
for item in people:
    print item
"""
"""
def split_title_and_name(person):
  return person.split(' ')[0] + ' ' + person.split(' ')[-1]

print list(map(split_title_and_name, people))

def times_tables():
    lst = []
    for i in range(10):
        for j in range (10):
            lst.append(i*j)
    return lst

print (times_tables())
#times_tables() == [???]

my_list = [i*j for j in range (10) for i in range(10)]
print (my_list)
"""

#example to have id as two letters and two digits, such as oh12
lowercase = 'abcdefghijklmnopqrstuvwxyz'
digits = '0123456789'

correct_answer = [a+b+c+d for a in lowercase for b in lowercase for c in digits for d in digits]
print (correct_answer[:50]) # Display first 50 ids






