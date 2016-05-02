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
Het = 0
Ref = 1
Non = 2

#pMATCHREAL = 0.999999
pMATCHRAND = 1 - 2 * 0.16 * 0.36

max_Parents_PVal = 10
max_Parents_Likelihood = 100

'''
Parents is a numpy two dimensional array with 
SNP positions across and inidividual genotypes down
Child is a numpy one dimensional array
returns list of parents along with Homozygote matches,
number of homozygous sites on child
'''

def ReconnectMatch(Parents, Child):
    
    num_SNP_Pos = len(Child)
    num_Parents = Parents.shape[1]
    match_List = [0] * num_Parents

    for child_Allele in range(1,num_SNP_Pos):
        for parent_gen in range(0, num_Parents):
            if Child[child_Allele] == Het:
                match_List[parent_gen] += 1
            elif Child[child_Allele] == Parents[child_Allele, parent_gen]:
                match_List[parent_gen] += 1


    return match_List, num_SNP_Pos

def Calculate_Likelihood_Ratios(match_List, num_SNP_Pos, pMATCHRAND):
    likelihood_List = [0] * len(match_List)

    for parent_Idx in range(0, len(match_List)):
        if match_List[parent_Idx] >= MINMATCH and num_SNP_Pos - match_List[parent_Idx] <= MAXMATCH:
            likelihood_List[parent_Idx] = dec.Decimal(pMATCHRAND **  match_List[parent_Idx])

    return likelihood_List

def find_Most_Likely(Parents, likelihood_List, match_List, max_Parents):

    parent_Match_Likelihood_List = []
    top_Matches = np.argsort(match_List)[-max_Parents:]
    for x in range(max_Parents-1, -1, -1):
        parent_Match_Likelihood_List.append((Parents[0, top_Matches[x]], match_List[top_Matches[x]], dec.Decimal(likelihood_List[top_Matches[x]])))

    return parent_Match_Likelihood_List

def get_P_Values(Parents, Child, match_List, num_SNP_Pos, allele_Frequencies, max_Parents):
    
    parent_Match_PVal_List = []
    top_Matches = np.argsort(match_List)[-max_Parents:]

    for x in range(max_Parents-1, -1, -1):
        p_Val = dec.Decimal(1)
        for child_Allele in range(1,num_SNP_Pos):
            if Child[child_Allele] != Het:
                if Child[child_Allele] == Parents[child_Allele, top_Matches[x]]:
                    p_Val = p_Val * dec.Decimal(1 - allele_Frequencies[child_Allele] ** 2 - (1 - allele_Frequencies[child_Allele]) ** 2)
                if Child[child_Allele] == Het:
                    if Parents[child_Allele, top_Matches[x]] == Het:
                        p_Val = p_Val * dec.Decimal(1 - allele_Frequencies[child_Allele] ** 2 - (1 - allele_Frequencies[child_Allele]) ** 2)
        parent_Match_PVal_List.append((Parents[0, top_Matches[x]], match_List[top_Matches[x]], dec.Decimal(p_Val)))

    return parent_Match_PVal_List

def main(Parents, Child, allele_Frequencies):
    match_List, num_SNP_Pos = ReconnectMatch(Parents, Child)
    likelihood_List = Calculate_Likelihood_Ratios(match_List, num_SNP_Pos, pMATCHRAND)
    parent_Match_Likelihood_List = find_Most_Likely(Parents, likelihood_List, match_List, max_Parents_Likelihood)
    parent_Match_PVal_List = get_P_Values(Parents, Child, match_List, num_SNP_Pos, allele_Frequencies, max_Parents_PVal)

    '''for match in parent_Match_Likelihood_List:
        print(match)
    print ("\n")
    for match in  parent_Match_PVal_List:
        print(match)'''

    parent_Percent_List = []

    for match in parent_Match_Likelihood_List:
        parent_Percent_List.append((match[0], "{0:.0f}%".format(match[1]/num_SNP_Pos))

    for match in parent_Percent_List:
        print(match)


if __name__ == "__main__":
    pdb.set_trace()
    Parents = numpy.random.randint(3, size=(501, 1000))
    Child = numpy.random.randint(3, size=501)
    allele_Frequencies = numpy.random.random(size = 501)
    main(Parents, Child, allele_Frequencies)
