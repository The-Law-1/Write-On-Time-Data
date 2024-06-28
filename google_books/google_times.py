#! /usr/bin/python3

import requests
import html
import time as TIME
import re

time_to_past_expression = {}
time_to_before_expression = {}

hours_words = ["midnight", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "eleven", "twelve"]

minutes_words = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "eleven", "twelve", 
                 "thirteen", "fourteen", "fifteen", "sixteen", "seventeen", "eighteen", "nineteen", "twenty", 
                 "twenty-one", "twenty-two", "twenty-three", "twenty-four", "twenty-five", "twenty-six", 
                 "twenty-seven", "twenty-eight", "twenty-nine", "thirty", "thirty-one", "thirty-two", "thirty-three", 
                 "thirty-four", "thirty-five", "thirty-six", "thirty-seven", "thirty-eight", "thirty-nine", "forty", 
                 "forty-one", "forty-two", "forty-three", "forty-four", "forty-five", "forty-six", "forty-seven", 
                 "forty-eight", "forty-nine", "fifty", "fifty-one", "fifty-two", "fifty-three", "fifty-four", 
                 "fifty-five", "fifty-six", "fifty-seven", "fifty-eight", "fifty-nine"]

for hour in range(0, 13):
  for minute in range(1, 60):
    time = f"{hour:02d}:{minute:02d}"
    
    time_to_past_expression[time] = []
    
    no_hyphen_minutes = ""
    if ("-" in minutes_words[minute - 1]):
      no_hyphen_minutes = minutes_words[minute - 1].replace("-", " ")

    time_to_past_expression[time].append(f"{minutes_words[minute - 1]}+minute{'s' if minute != 1 else ''}+past+{hours_words[hour]}")

    if (no_hyphen_minutes != ""):
      # time_to_past_expression[time] = f"{no_hyphen_minutes}+minutes+past+{hours_words[hour]}"
      time_to_past_expression[time].append(f"{no_hyphen_minutes}+minutes+past+{hours_words[hour]}")
      if minute > 30:
        if (hour == 12):
          time_to_past_expression[time].append(f"{no_hyphen_minutes}+minutes+before+{hours_words[1]}")
          # time_to_past_expression[time] = f"{no_hyphen_minutes}+minutes+before+{hours_words[1]}"
        else:
          time_to_past_expression[time].append(f"{no_hyphen_minutes}+minutes+before+{hours_words[hour + 1]}")
          # time_to_past_expression[time] = f"{no_hyphen_minutes}+minutes+before+{hours_words[hour + 1]}"
    
    if hour < 13 and minute > 30:
      time_to_before_expression[time] = []
      if (hour == 12):
        time_to_before_expression[time].append(f"{minutes_words[60 - minute - 1]}+minute{'s' if minute != 59 else ''}+before+{hours_words[1]}")
        # time_to_before_expression[time] = f"{minutes_words[60 - minute - 1]}+minute{'s' if minute != 59 else ''}+before+{hours_words[1]}"
      else:
        time_to_before_expression[time].append(f"{minutes_words[60 - minute - 1]}+minute{'s' if minute != 59 else ''}+before+{hours_words[hour + 1]}")
        # time_to_before_expression[time] = f"{minutes_words[60 - minute - 1]}+minute{'s' if minute != 59 else ''}+before+{hours_words[hour + 1]}"


max_depth = 10

def clean_snippet(snippet):
  snippet = snippet.replace("<b>", "").replace("</b>", "")
  snippet = html.unescape(snippet)
  
  snippet = snippet.replace("...", "")
  
  snippet = snippet.replace(" - ", "-")
  snippet = snippet.replace("- ", "-")
  snippet = snippet.replace(" -", "-")
  
  snippet = snippet.replace(" .", ".")
  snippet = snippet.replace(" ?", "?")
  snippet = snippet.replace(" !", "!")
  
  return snippet

def get_sentence_from_snippet(snippet, title, time_str, curr_depth=0):
  
  if (curr_depth > max_depth):
    print("discarding", title, snippet, time_str)
    return ""

  snippet = clean_snippet(snippet)

  snippet = snippet.replace(" ", "+")

  title = title.replace(" ", "+")
  
  url = f'https://www.googleapis.com/books/v1/volumes?q=".*+{snippet}"+subject:fiction+intitle:{title}&filter=partial&maxResults=1&printType=books'
  response = requests.get(url)
  books = response.json()
  
  
  for item in books.get('items', []):
    
    extendedSnippet = item.get('searchInfo', {}).get('textSnippet', 'No Snippet')
    
    extendedSnippet = clean_snippet(extendedSnippet)
    
    if extendedSnippet == "No Snippet":
      return ""

    # match this regex (?<=\.\s)[^.]*your_pattern_here[^.]*\.(?=\s)
    print("Searching for snippet \n'" + time_str + "' in \n" + extendedSnippet)
    # (?<=[.?!])[^.?!]*twenty four minutes past midnight.*?[.?!]
    match = re.search(rf'(?<=[.?!])[^.?!]*{time_str}.*?[.?!]', extendedSnippet, re.IGNORECASE)
    if match != None:
      sentence = match.group(0)
      print("Found: ", sentence)
      return sentence
    else:
      print("Snippet didn't match regex: ", extendedSnippet)
      TIME.sleep(0.1)
      return get_sentence_from_snippet(extendedSnippet, title, time_str, curr_depth + 1)


#  https://www.googleapis.com/books/v1/volumes?q="three+minutes+past+midnight"+subject:fiction&filter=partial&maxResults=40&printType=books
def search_google_books(time_str, startIdx=0, maxResults=40):

    print("Searching for time: ", time_str)
    # maximum results is 40, after that, you need to paginate with startIndex
    url = f'https://www.googleapis.com/books/v1/volumes?q=".*+{time_str}"+subject:fiction&filter=partial&maxResults={maxResults}&printType=books'
    response = requests.get(url)
    books = response.json()
    results = []
    
    starting_snippets = []

    for item in books.get('items', []):
      
        # make sure the 'categories': ['Fiction']
        categories = item['volumeInfo'].get('categories', [])

        title = item['volumeInfo'].get('title', 'No Title')
        authors = item['volumeInfo'].get('authors', ['No Author'])
        snippet = item.get('searchInfo', {}).get('textSnippet', 'No Snippet')
        preview_link = item['volumeInfo'].get('previewLink', 'No Preview Link')
        
        time_str = time_str.replace("+", " ")
        
        snippet = clean_snippet(snippet)
        
        if (snippet in starting_snippets):
          print("Skipping snippet because I've seen it")
          continue
        
        # we've already seen this snippet, don't duplicate it, or waste time on it
        starting_snippets.append(snippet)
        
        # if the snippet doesn't contain the time, discard it
        # ! shouldn't really happen because it means google made a mistake
        if (time_str not in snippet.lower()):
          print("discarding", title, snippet, preview_link, authors[0], time_str)
          continue
        
        sentence = get_sentence_from_snippet(snippet, title, time_str)
        if (sentence == None or len(sentence) == 0):
          continue
        print("Found sentence: ", sentence)
 
        results.append({'title': title, 'snippet': sentence, 'preview_link': preview_link, "author": authors[0], "expression": time_str.replace("+", " ")})

    TIME.sleep(1)
    return results


# resultsA = search_google_books("twenty-one+minutes+past+midnight")
# print(resultsA)
# resultsB = search_google_books("twenty+one+minutes+past+midnight")
# print(resultsB)

# get_sentence_from_snippet("one minute past midnight", "Without Fail", "one minute past midnight", 0)

# print("Before expressions ", time_to_before_expression)


with open("missing_times.txt") as f:
    for line in f:
      # split at :
      split_line = line.split("Missing:")
      if (len(split_line) != 2):
        continue
      time = split_line[1]
      time = time.strip()
      
      # if the hours are over 12, skip. There are no lines for 13:00, 14:00, etc.
      if time not in time_to_past_expression:
        continue
  
      # since hyphens/non-hyphens, multiple expressions can be under one time format
      time_past_expression_arr = time_to_past_expression[time]
      
      book_clocks = []
      for time_past_expression in time_past_expression_arr:
        book_clocks_past = search_google_books(time_past_expression)
        book_clocks.extend(book_clocks_past)
      
      if time in time_to_before_expression:
        time_before_expression_arr = time_to_before_expression[time]
        for time_before_expression in time_before_expression_arr:
          book_clocks_before = search_google_books(time_before_expression)
          book_clocks.extend(book_clocks_before)
      
      
      with open("new_google_times.csv", "a") as f2:
        for book in book_clocks:

          result_str = f"{time}|{book['snippet']}|{book['title']}|{book['preview_link']}|{book['author']}|{book['expression']}\n"
          print(result_str)
          f2.write(result_str)