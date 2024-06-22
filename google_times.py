#! /usr/bin/python3

import requests
import html
import time as TIME

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
    time_to_past_expression[time] = f"{minutes_words[minute - 1]}+minute{'s' if minute != 1 else ''}+past+{hours_words[hour]}"
    
    if hour + 1 < 13 and hour > 0 and minute > 30:
      time_to_before_expression[time] = f"{minutes_words[60 - minute - 1]}+minute{'s' if minute != 1 else ''}+before+{hours_words[hour + 1]}"


#  https://www.googleapis.com/books/v1/volumes?q="three+minutes+past+midnight"+subject:"fiction"&filter=free-ebooks
def search_google_books(time_str):

    url = f'https://www.googleapis.com/books/v1/volumes?q="{time_str}"&subject:fiction&filter=free-ebooks'
    response = requests.get(url)
    books = response.json()
    results = []

    for item in books.get('items', []):
        title = item['volumeInfo'].get('title', 'No Title')
        authors = item['volumeInfo'].get('authors', ['No Author'])
        snippet = item.get('searchInfo', {}).get('textSnippet', 'No Snippet')
        preview_link = item['volumeInfo'].get('previewLink', 'No Preview Link')
        
        # remove html tags from snippet
        snippet = snippet.replace("<b>", "").replace("</b>", "")
        snippet = html.unescape(snippet)
        
        time_str = time_str.replace("+", " ")
        
        # if the snippet doesn't contain the time, discard it
        if (time_str not in snippet.lower()):
          print("Discarding", title, snippet, preview_link, authors[0], time_str)
          continue
 
        results.append({'title': title, 'snippet': snippet, 'preview_link': preview_link, "author": authors[0], "expression": time_str.replace("+", " ")})

    TIME.sleep(1)
    return results


# results = search_google_books("three+minutes+past+midnight")
# print(results)

with open("missing_times.txt") as f:
    for line in f:
      # split at :
      split_line = line.split("Missing:")
      if (len(split_line) != 2):
        continue
      time = split_line[1]
      time = time.strip()
      time_past_expression = time_to_past_expression[time]
      
      book_clocks = []
      book_clocks_past = search_google_books(time_past_expression)
      
      if time in time_to_before_expression:
        time_before_expression = time_to_before_expression[time]
        book_clocks_before = search_google_books(time_before_expression)
        book_clocks.extend(book_clocks_before)
      
      book_clocks.extend(book_clocks_past)
      
      with open("google_times.csv", "a") as f2:
        for book in book_clocks:

          result_str = f"{time}|{book['snippet']}|{book['title']}|{book['preview_link']}|{book['author']}|{book['expression']}\n"
          print(result_str)
          f2.write(result_str)