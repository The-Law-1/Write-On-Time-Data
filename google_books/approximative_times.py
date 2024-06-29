#! /usr/bin/python3

import requests
import html
import time as TIME
import re

approx_expressions = {}

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
  for minute in range(0, 60):
    time = f"{hour:02d}:{minute:02d}"
    
    approx_expressions[time] = []

    if (minute == 0):

      if (hour != 0):
        approx_expressions[time].append({'expression': f"almost+{hours_words[hour]}+o'clock", 'approximation': 'any'})
        approx_expressions[time].append({'expression': f"around+{hours_words[hour]}+o'clock", 'approximation': 'any'})
      else:
        approx_expressions[time].append({'expression': f"almost+{hours_words[hour]}", 'approximation': 'any'})
        approx_expressions[time].append({'expression': f"around+{hours_words[hour]}", 'approximation': 'any'})

      approx_expressions[time].append({'expression': f"just+after+{hours_words[hour]}", 'approximation': 'after'})
      approx_expressions[time].append({'expression': f"just+before+{hours_words[hour]}", 'approximation': 'before'})

      approx_expressions[time].append({'expression': f"shortly+after+{hours_words[hour]}", 'approximation': 'after'})
      approx_expressions[time].append({'expression': f"shortly+before+{hours_words[hour]}", 'approximation': 'before'})

      approx_expressions[time].append({'expression': f"a+few+minutes+after+{hours_words[hour]}", 'approximation': 'after'})
      approx_expressions[time].append({'expression': f"a+few+minutes+before+{hours_words[hour]}", 'approximation': 'before'})

    if (minute == 15):
        approx_expressions[time].append({'expression': f"almost+quarter+past+{hours_words[hour]}", 'approximation': 'any'})
        approx_expressions[time].append({'expression': f"around+quarter+past+{hours_words[hour]}", 'approximation': 'any'})
    if (minute == 30):
        approx_expressions[time].append({'expression': f"almost+half+past+{hours_words[hour]}", 'approximation': 'any'})
        approx_expressions[time].append({'expression': f"around+half+past+{hours_words[hour]}", 'approximation': 'any'})
    if (minute == 45 and hour < 12):
        approx_expressions[time].append({'expression': f"almost+quarter+to+{hours_words[hour + 1]}", 'approximation': 'any'})
        approx_expressions[time].append({'expression': f"around+quarter+to+{hours_words[hour + 1]}", 'approximation': 'any'})
    
    


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
def search_google_books(time_str, approximation, startIdx=0, maxResults=40):

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
 
        results.append({'title': title,
                        'snippet': sentence,
                        'preview_link': preview_link,
                        "author": authors[0],
                        "expression": time_str.replace("+", " "),
                        "approximation": approximation})

    TIME.sleep(1)
    return results
  
# results = search_google_books("around+half+past+midnight", "any")
# print(results)

with open("approximate_times.txt") as f:
    for line in f:
      time = line
      time = time.strip()
      
      if time not in approx_expressions:
        continue
  
      # since hyphens/non-hyphens, multiple expressions can be under one time format
      approx_time_expression_arr = approx_expressions[time]
      
      book_clocks = []
      for approx_time_expression in approx_time_expression_arr:
        book_clocks_approx = search_google_books(approx_time_expression['expression'], approx_time_expression['approximation'])
        book_clocks.extend(book_clocks_approx)
      
      with open("approximate_google_times.csv", "a") as f2:
        for book in book_clocks:

          result_str = f"{time}|{book['snippet']}|{book['title']}|{book['preview_link']}|{book['author']}|{book['expression']}|{book['approximation']}\n"
          print(result_str)
          f2.write(result_str)