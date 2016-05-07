#ReconnectMatching
''' PARAMETERS
MINMATCH = Mnimum Number Homozygote Matches
MAXMATCH = Maximum Number Homozygote Mismatches
Het = heterozygote
Ref = Reference Allele Homozygote
Non = Nonreference Alllel Homozygote
num_SNP_Pos = number of SNP Positions
pMATCHRAND = probability of allele match by chance
pMATCHREAL = probability of homozygote match by parent
'''
import decimal
import decimal as dec
import numpy
import numpy as np
from numpy import *
import pdb

MINMATCH = 1
MAXMATCH = 500
Het = 1
Ref = 0
Non = 2
NA = 9

max_Parents = 100

'''
Parents is a numpy two dimensional array with
SNP positions across and inidividual genotypes down
Child is a numpy one dimensional array
returns list of parents along with Homozygote matches,
number of homozygous sites on child
'''

def ReconnectMatch(Parents, Child):

    num_SNP_Pos = len(Child)
    num_Parents = Parents.shape[0]
    match_List = [0] * num_Parents
    parent_Num_SNP_Pos = [0] * num_Parents

    for child_Allele in range(1,num_SNP_Pos):
        for parent_gen in range(0, num_Parents):
            if Child[child_Allele] != NA and Parents[parent_gen, child_Allele] != NA:
                parent_Num_SNP_Pos[parent_gen] += 1
                if Child[child_Allele] == Het:
                    match_List[parent_gen] += 1
                elif Child[child_Allele] != Het:
                    if Child[child_Allele] == Parents[parent_gen, child_Allele]:
                        match_List[parent_gen] += 1
                    elif Parents[parent_gen, child_Allele] == Het:
                        match_List[parent_gen] += 1


    return match_List, parent_Num_SNP_Pos, num_SNP_Pos

def find_Most_Likely(Parents, match_List, parent_Num_SNP_Pos, max_Parents):

    parent_Match_List = []
    top_Matches = np.argsort(match_List)[-max_Parents:]
    for x in range(max_Parents-1, -1, -1):
        parent_Match_List.append((Parents[top_Matches[x],0], match_List[top_Matches[x]], parent_Num_SNP_Pos[top_Matches[x]]))

    return parent_Match_List

def get_P_Values(Parents, Child, match_List, num_SNP_Pos, allele_Frequencies, max_Parents):

    parent_Match_PVal_List = []

    top_Matches = np.argsort(match_List)[-max_Parents:]

    for x in range(max_Parents-1, -1, -1):
        p_Val = dec.Decimal(1)
        for child_Allele in range(1,num_SNP_Pos):
            if Child[child_Allele] != NA and Parents[top_Matches[x], child_Allele] != NA:
                if Child[child_Allele] == Het:
                    p_Val = p_Val * dec.Decimal(1 - allele_Frequencies[child_Allele] ** 2 - (1 - allele_Frequencies[child_Allele]) ** 2)
                elif Child[child_Allele] != Het:
                    if Child[child_Allele] == Parents[top_Matches[x], child_Allele]:
                        p_Val = p_Val * dec.Decimal(1 - allele_Frequencies[child_Allele] ** 2 - (1 - allele_Frequencies[child_Allele]) ** 2)
                    elif Parents[top_Matches[x], child_Allele] == Het:
                        p_Val = p_Val * dec.Decimal(1 - allele_Frequencies[child_Allele] ** 2 - (1 - allele_Frequencies[child_Allele]) ** 2)
        parent_Match_PVal_List.append((Parents[top_Matches[x],0], match_List[top_Matches[x]], dec.Decimal(p_Val)))

    return parent_Match_PVal_List

def get_matches(Parents, Child, allele_Frequencies):
    match_List, parent_Num_SNP_Pos, num_SNP_Pos = ReconnectMatch(Parents, Child)
    parent_Match_List = find_Most_Likely(Parents, match_List, parent_Num_SNP_Pos, max_Parents)
    parent_Match_PVal_List = get_P_Values(Parents, Child, match_List, num_SNP_Pos, allele_Frequencies, max_Parents)

    parent_Percent_List = []

    for match in parent_Match_List:
        tmp1 = float(match[1])
        tmp2 = float(match[2])
        parent_Percent_List.append((match[0], "{0:.0f}%".format((tmp1/tmp2)*100)))

    # for absolute p_Values

    # print parent_Match_PVal_List

    # uncomment statement above


    return parent_Percent_List[:10]

if __name__ == "__main__":
    Parents = numpy.random.randint(3, size=(501, 1000))
    Child = numpy.random.randint(3, size=501)
    allele_Frequencies = numpy.random.random(size = 501)
    get_matches(Parents, Child, allele_Frequencies)