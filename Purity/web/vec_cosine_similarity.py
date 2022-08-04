from sklearn.feature_extraction.text import TfidfVectorizer #for vectorization of documents
from sklearn.metrics.pairwise import cosine_similarity # for checking text similarity btn jd and cvs
from nltk.stem.wordnet import WordNetLemmatizer # for getting root word through lemmatization
from nltk.corpus import stopwords as stp # to get stopwords for future removal from the docs
from web import vec_lemma as lemma #comes with lemmatization and vectorization
import re

def extract_emails(text):
    return re.findall(r"[\w.+-]+@[\w-]+\.[\w.-]+", text.replace("\s+","").replace("\n",""))



#fxn for cosine similarity btn the job description and resumes
def get_tf_idf_cosine_similarity(compare_doc,doc_corpus):
    tf_idf_vect = TfidfVectorizer(analyzer=lemma.stemmed_words)
    tf_idf_req_vector = tf_idf_vect.fit_transform([compare_doc]).todense()
    tf_idf_resume_vector = tf_idf_vect.transform(doc_corpus).todense()
    cosine_similarity_list = []
    
    for i in range(len(tf_idf_resume_vector)):
        res = []
        mails = extract_emails(doc_corpus[i])
        similarity = cosine_similarity(tf_idf_req_vector,tf_idf_resume_vector[i])[0][0]
        res.append(similarity)
        res.append(mails)
        cosine_similarity_list.append(res)
    
    return cosine_similarity_list


