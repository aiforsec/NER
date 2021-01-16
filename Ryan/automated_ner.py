import os
import sys
import polyglot
from polyglot.text import Text
from flair.models import SequenceTagger

flair_12class = SequenceTagger.load('ner-ontonotes-fast')
flair_4class = SequenceTagger.load('ner')

def polyglot_ner(document):
  return {(' '.join(entity),entity.tag.split('-')[-1]) for entity in Text(document).entities}

def flair_ner(document, model):
  from flair.data import Sentence
  s = Sentence(document)
  model.predict(s)
  entities = s.to_dict(tag_type='ner')
  return [(entity["text"], entity["labels"]) for entity in entities["entities"]]

def main():
    if len(sys.argv) != 2:
        print("Usage:", sys.argv[0], "<input directory>")
        exit()

    for root, _, files in os.walk(sys.argv[1]):
        for filename in files:
            if filename.lower() != "readme.txt" and os.path.splitext(filename)[1] == ".txt":
                path = os.path.join(root, filename)
                text = "" #Still need to figure out a way to get text
                '''
                with open(os.path.join(root, name), "r", encoding='ANSI') as file:
                    print(os.path.join(root, name))
                    try:
                        print(file.read())
                        print("BLAH")
                        input()
                    except Exception as err:
                        print(err)
                print(os.path.join(root, name))
                '''
                output = flair_ner(text, flair_4class)
                with open(os.path.join(root, "flair4class_" + filename), 'w') as file:
                    file.writelines("%s\n" % entity for entity in output)
                    
                output = flair_ner(text, flair_12class)
                with open(os.path.join(root, "flair12class_" + filename), 'w') as file:
                    file.writelines("%s\n" % entity for entity in output)

                output = polyglot_ner(text)
                with open(os.path.join(root, "polyglot_" + filename), 'w') as file:
                    file.writelines("%s\n" % entity for entity in output)
                input()

if __name__ == "__main__":
    main()
