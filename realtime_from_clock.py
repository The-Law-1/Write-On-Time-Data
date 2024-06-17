import sys

# get real time from strings like "midnight", "noon", "3:30pm", "3:30", "3pm", "3"

time_correspondance = {
  "noon": "12:00",
  "midnight": "00:00",
}

hours_words = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "eleven", "twelve"]
minutes_words = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "eleven", "twelve", 
                 "thirteen", "fourteen", "fifteen", "sixteen", "seventeen", "eighteen", "nineteen", "twenty", 
                 "twenty-one", "twenty-two", "twenty-three", "twenty-four", "twenty-five", "twenty-six", 
                 "twenty-seven", "twenty-eight", "twenty-nine", "thirty", "thirty-one", "thirty-two", "thirty-three", 
                 "thirty-four", "thirty-five", "thirty-six", "thirty-seven", "thirty-eight", "thirty-nine", "forty", 
                 "forty-one", "forty-two", "forty-three", "forty-four", "forty-five", "forty-six", "forty-seven", 
                 "forty-eight", "forty-nine", "fifty", "fifty-one", "fifty-two", "fifty-three", "fifty-four", 
                 "fifty-five", "fifty-six", "fifty-seven", "fifty-eight", "fifty-nine"]

word_hour_to_number = {word: str(i+1) for i, word in enumerate(hours_words)}
word_minute_to_number = {word: str(i+1) for i, word in enumerate(minutes_words)}

# generate all possible times
for hour in range(24):
  for minute in range(60):
    time = f"{hour:02}:{minute:02}"
    time_correspondance[time] = time
    
for hour_word in hours_words:
  for minute_word in minutes_words:
    time_correspondance[f"{minute_word} minute{'s' if minute_word != 'one' else ''} past {hour_word}"] = f"{word_hour_to_number[hour_word]}:{word_minute_to_number[minute_word]}"
    time_correspondance[f"{minute_word} minute{'s' if minute_word != 'one' else ''} before {hour_word}"] = f"{word_hour_to_number[hour_word]}:{word_minute_to_number[minute_word]}"

  time_correspondance[hour_word + " o'clock"] = f"{word_hour_to_number[hour_word]}:00"
  time_correspondance[hour_word + " o’clock"] = f"{word_hour_to_number[hour_word]}:00"
  
  time_correspondance[hour_word + "-o'clock"] = f"{word_hour_to_number[hour_word]}:00"
  time_correspondance[hour_word + "-o’clock"] = f"{word_hour_to_number[hour_word]}:00"
  

  time_correspondance["quarter past " + hour_word] = f"{word_hour_to_number[hour_word]}:15"
  time_correspondance["half past " + hour_word] = f"{word_hour_to_number[hour_word]}:30"
  time_correspondance["quarter to " + hour_word] = f"{int(word_hour_to_number[hour_word]) - 1}:45"

def get_realtime_from_clock(clocktime):
  if (clocktime in time_correspondance):
    return time_correspondance[clocktime]
  return ""

# if (len(sys.argv) > 0):
#   # open the csv file
#   with open(sys.argv[1], "r") as f:
#     with open("updated.csv", "w") as f2:
      
#       # read the file
#       text = f.read()
#       # split the file by lines
#       lines = text.split("\n")
#       # iterate over the lines
#       for line in lines:
#         # split the line by commas
#         parts = line.split(",")
#         print("Parts: ", parts)
#         # if the line has at least 2 parts
#         if len(parts) > 1:
#           # get the clock time
#           clocktime = parts[5]
#           print("Clocktime: ", clocktime)
#           # add the mapping to the time_correspondance dictionary
#           realtime = get_realtime_from_clock(clocktime)
#           print("Realtime: ", realtime)
          
#           f2.write(f"{realtime}{line}\n")

