import os
from web import doc_to_vec as doc # to get the documents
from web import vec_cosine_similarity as vec 




def process_files(req_document,resume_docs):
    # print(f"Req is  {req_document}\n")#
    # print(f"Req is  {resume_docs}\n")
    req_doc_text = doc.get_content_as_string(req_document)
    resume_doc_text = []
    for doct in resume_docs:
        resume_doc_text.append(doc.get_content_as_string(doct))

    cos_sim_list = vec.get_tf_idf_cosine_similarity(req_doc_text,resume_doc_text)
    final_doc_rating_list = []
    zipped_docs = zip(cos_sim_list,resume_docs)
    sorted_doc_list = sorted(zipped_docs, key = lambda x: x[0], reverse=True)
    for element in sorted_doc_list:
        print(element)
        doc_rating_list = []
        doc_rating_list.append(os.path.basename(element[1]))
        doc_rating_list.append('{:.0%}'.format(element[0][0]))

        mails = element[0][1]
        if len(mails)==0:
            mails.append("")
        doc_rating_list.append(" ".join(mails[0]))
        final_doc_rating_list.append(doc_rating_list)
    return final_doc_rating_list
    
    