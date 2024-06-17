import re

hours = list(range(1, 13))
minutes = list(range(1, 60))

time_expressions = []

hours_words = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "eleven", "twelve"]
minutes_words = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "eleven", "twelve", 
                 "thirteen", "fourteen", "fifteen", "sixteen", "seventeen", "eighteen", "nineteen", "twenty", 
                 "twenty-one", "twenty-two", "twenty-three", "twenty-four", "twenty-five", "twenty-six", 
                 "twenty-seven", "twenty-eight", "twenty-nine", "thirty", "thirty-one", "thirty-two", "thirty-three", 
                 "thirty-four", "thirty-five", "thirty-six", "thirty-seven", "thirty-eight", "thirty-nine", "forty", 
                 "forty-one", "forty-two", "forty-three", "forty-four", "forty-five", "forty-six", "forty-seven", 
                 "forty-eight", "forty-nine", "fifty", "fifty-one", "fifty-two", "fifty-three", "fifty-four", 
                 "fifty-five", "fifty-six", "fifty-seven", "fifty-eight", "fifty-nine"]


# Generate "x o'clock" expressions
time_expressions.extend([f'{h} o\'clock' for h in hours_words])
time_expressions.extend([f'{h} o’clock' for h in hours_words])

time_expressions.extend([f'{h}-o\'clock' for h in hours_words])
time_expressions.extend([f'{h}-o’clock' for h in hours_words])

# Generate "xx:yy" expressions
time_expressions.extend([f'{h:02d}:{m:02d}' for h in range(24) for m in range(60)])

# Generate "1 minute past 10" and "2 minutes past 5" expressions
time_expressions.extend([f'{m} minute{"s" if m != "one" else ""} past {h}' for h in hours_words for m in minutes_words])

time_expressions.extend([f'{m} minute{"s" if m != "one" else ""} before {h}' for h in hours_words for m in minutes_words])


# Generate "quarter past y", "half past y", and "quarter to y" expressions
time_expressions.extend([f'quarter past {h}' for h in hours_words])
time_expressions.extend([f'half past {h}' for h in hours_words])
time_expressions.extend([f'quarter to {h}' for h in hours_words])

# extend to find noon and midnight
time_expressions.extend(["noon", "midnight"])

# print(time_expressions)

# example = "It was 10 o'clock when the clock struck 10. Then 10:31, then it was five minutes past eleven. Then 45 minutes before twelve."

# Join all time expressions into a single regular expression pattern
time_pattern = '|'.join(r'\b' + re.escape(expr) + r'\b' for expr in time_expressions)

# Compile the regular expression pattern
time_regex = re.compile(time_pattern, re.IGNORECASE)
# matches = time_regex.findall(example)

# print(matches)