import sys

def readParents():
        f = open('data/all_parents')
        annot_hash={}
        for line in f:
                line.strip()
                tmp = line.split()
                if len(tmp) > 1:
                        protein = tmp.pop(0)
                        goterm = tmp
                        annot_hash[protein] = goterm
        return annot_hash

if __name__ == '__main__':

        parent_hash = readParents()

        input_file = sys.argv[1]
        output_file = sys.argv[2]

        f = open(input_file,'r')
        w = open(output_file,'w')

        for row in f:
                r = row.strip()
                tmp = r.split()
                prot_name = tmp[0]
                w.write(prot_name)
                w.write(' ')
                goterms = tmp[1].split(',')

                all_terms = set()
            
                for term in goterms:
                        if term in parent_hash:
                                all_terms.add(term)
                                parent_terms = parent_hash[term][0].split(',')
                                for t in parent_terms:
                                        all_terms.add(t)
                        else:
                                all_terms.add(term)



                all_terms = list(all_terms)
                w.write(','.join(all_terms))
                w.write('\n')

        print("GO term propogated file created \n")

w.close()