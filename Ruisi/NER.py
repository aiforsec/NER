import os
import shutil
import unicodedata

from polyglot.text import Text
from flair.models import SequenceTagger
flair_12class = SequenceTagger.load('ner-ontonotes-fast')
flair_4class = SequenceTagger.load('ner')

def flair_ner(document, model):
    from flair.data import Sentence
    s = Sentence(document)
    model.predict(s)
    entities = s.to_dict(tag_type='ner')
    return [(entity["text"], entity["labels"]) for entity in entities["entities"]]

def polyglot_ner(document):
    return {(' '.join(entity),entity.tag.split('-')[-1]) for entity in Text(document).entities}

directory = r'C:\Users\Jianr\Desktop\2020'
for filename in os.listdir(directory):
    print(os.path.join(directory, filename))
    f = open (os.path.join(directory, filename), 'r', encoding='ISO-8859-1')
    text = f.read()
    text = ''.join([l for l in text if unicodedata.category(l)[0] not in ('S', 'M', 'C')])
    f.close()
    subdirectory = r'C:\Users\Jianr\Desktop\2020pro\%s' % filename.replace(".txt", "").strip(" ")
    try:
        os.mkdir(r'C:\Users\Jianr\Desktop\2020pro\%s' % filename.replace(".txt", "").strip(" "))
        if len(os.path.join(subdirectory, filename)) >= 260:
            new_file = filename[:10] + ".txt"
        else:
            new_file = filename        
        original = os.path.join(directory, filename)
        target = os.path.join(subdirectory, new_file)
        shutil.copyfile(original, target)  
    except:
        print("already")
    if len(os.path.join(subdirectory, filename.replace(".txt", "_flair4.txt"))) >= 260:
        new_file = filename[:10] + ".txt"
    else:
        new_file = filename
    if not os.path.exists(os.path.join(subdirectory, new_file.replace(".txt", "_flair4.txt"))):
        txt1 = flair_ner(text, flair_4class)
        print(1)
        if len(os.path.join(subdirectory, filename.replace(".txt", "_flair4.txt"))) >= 260:
            new_file = filename[:10] + ".txt"
        else:
            new_file = filename
        with open(os.path.join(subdirectory, new_file.replace(".txt", "_flair4.txt")), 'w', encoding='ISO-8859-1') as filehandle:
            for listitem in txt1:
                filehandle.write('%s\n' % str(listitem))
    if len(os.path.join(subdirectory, filename.replace(".txt", "_flair12.txt"))) >= 260:
        new_file = filename[:10] + ".txt"
    else:
        new_file = filename
    if not os.path.exists(os.path.join(subdirectory, new_file.replace(".txt", "_flair12.txt"))):
        txt2 = flair_ner(text, flair_12class)
        print(2)
        if len(os.path.join(subdirectory, filename.replace(".txt", "_flair12.txt"))) >= 260:
            new_file = filename[:10] + ".txt"
        else:
            new_file = filename
        with open(os.path.join(subdirectory, new_file.replace(".txt", "_flair12.txt")), 'w', encoding='ISO-8859-1') as filehandle:
            for listitem in txt2:
                filehandle.write('%s\n' % str(listitem))
    if len(os.path.join(subdirectory, filename.replace(".txt", "_polyglot.txt"))) >= 260:
        new_file = filename[:10] + ".txt"
    else:
        new_file = filename
    if not os.path.exists(os.path.join(subdirectory, new_file.replace(".txt", "_polyglot.txt"))):
        txt3 = polyglot_ner(text)
        print(3)
        if len(os.path.join(subdirectory, filename.replace(".txt", "_polyglot.txt"))) >= 260:
            new_file = filename[:10] + ".txt"
        else:
            new_file = filename
        with open(os.path.join(subdirectory, new_file.replace(".txt", "_polyglot.txt")), 'w', encoding='ISO-8859-1') as filehandle:
            for listitem in txt3:
                filehandle.write('%s\n' % str(listitem))