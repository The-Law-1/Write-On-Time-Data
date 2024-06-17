import sys
import re

from time_expressions import time_regex
from realtime_from_clock import get_realtime_from_clock

# take a file as argument
argv = sys.argv

sentence_pattern = r'([^.!?"]*?[^.!?]*[.!?"])'

with open(argv[1], "r") as f:
  
    try:
      # argv could start with ".": "./books..."
      booknumber = argv[2]      
      
      text = f.read()
      
      splitInfo = text.split("*** START OF THE PROJECT GUTENBERG EBOOK")
      info = splitInfo[0]
      
      # match this info from info
      # Title: The Importance of Being Earnest: A Trivial Comedy for Serious People
      # Author: Oscar Wilde
      title = re.findall(r"Title: (.*)", info)[0]
      author = re.findall(r"Author: (.*)", info)[0]
      
      # discard any books that have the word bible
      if "bible" in title.lower():
        exit(0)

      print("Title: ", title)
      print("Author: ", author)
      
      text = splitInfo[1]
      
      # text = text.replace("\n", " ")

      sentences = re.findall(sentence_pattern, text, re.IGNORECASE)
      
      print("Booknumber: ", booknumber)
      
      for sentence in sentences:
        sentence = sentence.strip()
        sentence = sentence.replace("\n", " ")
        time_expressions = re.findall(time_regex, sentence)
        
        for time_exp in time_expressions:
          print(f"Sentence: {sentence}\n Time: {time_exp}\n\n")
 
          # worst case this will be empty string
          realtime = get_realtime_from_clock(time_exp)
 
          with open("times.csv", "a") as f:
            f.write(f"{realtime}|{sentence}|{booknumber}|{title}|{author}|{time_exp}\n")
    except Exception as e:
      # write to a log file
      with open("errors.log", "a") as f:
        f.write(f"Exception: while treating book {booknumber}: {e}\n")
      print(f"Exception: while treating book {booknumber}: {e}")
          