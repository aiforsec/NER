import os
import sys
import polyglot
import logging
from polyglot.text import Text
from flair.models import SequenceTagger

logging.basicConfig(
    level=logging.WARNING,
    format=('[%(asctime)s] %(levelname)-8s %(message)s'),
    handlers=[
        logging.FileHandler('debug.log'),
        logging.StreamHandler(sys.stdout),
    ]
)

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
            if filename.lower() != "readme.txt" and os.path.splitext(filename)[1] == ".txt" and not filename.startswith("flair4class_") and not filename.startswith("flair12class_") and not filename.startswith("polyglot_"):
                with open(os.path.join(root, filename), "r", encoding="windows_1252") as file:
                    try:
                        text = file.read()
                    except Exception as err:
                        logging.error("Unable to read file '" + os.path.join(root, filename) + "': " + str(err))
                        continue
                        
                if os.path.basename(os.path.normpath(root)) != os.path.splitext(filename)[0]:
                    tmp = os.path.join(root, os.path.splitext(filename)[0])
                    os.mkdir(tmp)
                    os.rename(os.path.join(root, filename), os.path.join(tmp, filename))
                    root = tmp

                print("Running flair4class algorithm on '" + filename + "'...")
                try:
                    with open(os.path.join(root, "flair4class_" + filename), 'w') as file:
                        file.writelines("%s\n" % str(entity) for entity in flair_ner(text, flair_4class))
                    print("Completed!")
                except Exception as err:
                    logging.error("flair4class failed on '" + os.path.join(root, filename) + "': " + str(err))
                
                print("Running flair12class algorithm on '" + filename + "'...")
                try:
                    with open(os.path.join(root, "flair12class_" + filename), 'w') as file:
                        file.writelines("%s\n" % str(entity) for entity in flair_ner(text, flair_12class))
                    print("Completed!")
                except Exception as err:
                    logging.error("flair12class failed on '" + os.path.join(root, filename) + "': " + str(err))

                print("Running polyglot algorithm on '" + filename + "'...")
                try:
                    with open(os.path.join(root, "polyglot_" + filename), 'w') as file:
                        file.writelines("%s\n" % str(entity) for entity in polyglot_ner(text))
                    print("Completed!")
                except Exception as err:
                    logging.error("polyglot failed on '" + os.path.join(root, filename) + "': " + str(err))
                print()

if __name__ == "__main__":
    main()
