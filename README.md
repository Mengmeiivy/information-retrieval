# An Information Retrieval task 
In this task, I did an information retrieval using TFIDF weights and cosine similarity scores. 

I used the Cranfield collection, which can be downloaded at http://ir.dcs.gla.ac.uk/resources/test_collections/cran/.
- cran.qry contains a set of 225 queries. 
- cran.all.1400 contains a set of 1400 abstracts of aerodynamics journal articles. 
- cranqrel is the answer key, with query ID as the first number and abstract ID as the second number. 

To run the program: python TFIDF.py 

To evaluate the result: python cranfield_score.py output.txt

The evaluation includes a Mean Average Precision based on the precision of the system at each 10% recall level from 10% to 100%. 
The evaluation also includes an Average Recall based on the number of abstracts associated with the query according to the answer key.

