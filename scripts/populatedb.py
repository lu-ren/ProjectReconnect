import psycopg2
import names
from random import randint
import numpy
import csv
import pdb

def populate_db():
    conn = psycopg2.connect(database='projectreconnectdb',
            user='projectreconnect', host='0.0.0.0', port='5432')
    namelst = []
    emaillst = []
    agelst = []
    genomelst = []
    with open('father0.txt') as f:
        reader = csv.reader(f)
        namelst.append('James Potter')
        genome = [int(s) for s in next(reader)[0]]
        genome.insert(0,0)
        emaillst.append('jp3999@hogwarts.edu')
        agelst.append(58)
        genomelst.append(numpy.array(genome))
    with open('Genotypes_Only.txt') as f:
        reader = csv.reader(f)
        for elem in reader:
            strlist = list(elem[0])
            numlist = [int(s) for s in strlist]
            numlist.insert(0, 0)
            numlist = numpy.array(numlist)
            name = names.get_full_name()
            email = name.replace(" ", "") + "@email.com"
            namelst.append(name)
            emaillst.append(email)
            agelst.append(randint(20,100))
            genomelst.append(numpy.array(numlist))
    genomelst = genomelst
    cursor = conn.cursor()
    for x in range(len(namelst)):
        hashed_password = 'blahblahblahblahblahshit'
        cursor.execute("insert into \"user\" (full_name, age, email, hashed_password, genomic_obj) values (%s, %s, %s, %s, %s)", (namelst[x], agelst[x], emaillst[x], hashed_password, 
                    psycopg2.Binary(genomelst[x])))
        conn.commit()
    conn.close()

populate_db()
