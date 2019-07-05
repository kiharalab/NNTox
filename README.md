# NNTox
NNTox (Neural Network based protein Toxin prediction) is a method to predict toxicity of any protein seqeunce based on protein's Gene Ontology (functional information) using machine leanring.  
Further, it can provide insight into proteins toxicity by prediction the mode of action of the toxicity. The mode of action is described by the 11 sub-categories of toxicity as defined in UniProtKB Keyword Toxin (https://www.uniprot.org/keywords/KW-0800) 

The input given to the method are the Gene Onotology (GO) terms of a protein. The are two networks. The first network will predict the probability of the protein to be toxin. The second network will predict the mode of action of a toxin protein.

Copyright (C) 2019 Aashish Jain, Daisuke Kihara, and Purdue University.

License: GPL v3 for academic use. (For commercial use, please contact us for different licensing)

Contact: Daisuke Kihara (dkihara@purdue.edu)

Reference: Jain A., Kihara D. Gene Ontology based Protein Toxicity Prediciton Using Neural Network. Submitted (2019).

#

### Pre-required software

Python 3 : https://www.python.org/downloads/  
tensorflow : pip/conda install tensorflow

### Running the method

Input File: Contains protein name and GO terms. Sample input file "example" is provided.  
Running: python nntox.py {input_file} {mode}  
There are two modes:  
a)'toxin' : Default mode will predict is a input protein is toxin or non toxin  
b)'mode_of_action': Will predict the mode of action of a toxin protein  

Example input and output files are found in sampleIO

Example runs:   
python nntox.py sampleIO/example1 toxin  
Output:
SIX2_LEIQH Toxin
SCX4_CENSU Toxin
..

python nntox.py sampleIO/example1 mode_of_action
Output:
SIX2_LEIQH Neurotoxin,Ion channel impairing toxin
SCX4_CENSU Neurotoxin,Ion channel impairing toxin
...

### Propogate GO terms  
The GO terms should be propogated ,i.e. ,parent GO terms should be added. We provide the code to do parental propogation.  
Running: python propogate_goterms.py {input_file} {output_file}  
An output file will be genarated with the name propogated_{input_filen} containing propogated GO terms.  
This output file can be used to run NNTox.

Example runs:
python propogate_goterms.py sampleIO/example2 sampleIO/example2_propogated  
Output file: sampleIO/example2_propogated    

Additional Data:
Toxin and Non toxin proteins and their GOterms are provided in the data/uniprot_data.

### Funding  
This study was sponsored by the Office of the Director of National Intel-ligence (ODNI), Intelligence Advanced Research Projects Activity (IARPA), via the Army Research Office (ARO) under cooperative Agree-ment Number W911NF-17-2-0105. DK also acknowledges support from the National Institute of General Medical Sciences of the NIH (R01GM123055) and the National Science Foundation (DMS1614777, CMMI1825941).  
