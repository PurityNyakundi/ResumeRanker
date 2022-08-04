import textract
import re



def clean_text(words):
    """
    Text cleaning
    Returns a cleaned text
    """
    words = str(words).lower()
    
    # new line removal#
    words = re.sub("\n" , " " , words)
    words = re.sub(u"\xa0" , " " , words)
    words = re.sub('[^A-Za-z0-9]+\s+', ' ', words)
    words = re.sub('\!', ' ', words)
    words = re.sub('\,', ' ', words)
    # remove distracting single quotes
    words = re.sub("\'", "", words)
    words = "".join(words)
    return words

def get_content_as_string(filename):
    # print(f"The file name is   {filename}")
    text = textract.process(filename)
    lower_case_string =  str(text.decode('utf-8')).lower()
    #final_string = re.sub('[^a-zA-Z0-9 \n]', '', lower_case_string)
    return clean_text(lower_case_string)


# print(get_content_as_string("./web/files/Manager_JD.docx"))