#open times.csv 
with open("times.csv", "r") as f:
  #open updated.csv
  with open("updated.csv", "w") as f2:
    #read the file
    text = f.read()
    #split the file by lines
    lines = text.split("\n")
    #iterate over the lines
    for (i, line) in enumerate(lines):
      parts = line.split("|")

      if (i % 1000 == 0):
        print("Line: ", i)

      #if the line has at least 2 parts
      if len(parts) > 1:
        numbers = parts[0].split(":")
        try:
          hour = numbers[0]
          minute = numbers[1]
          if (len(hour) == 1):
            hour = "0" + hour
            print("Fixed hour: ", hour)
          if (len(minute) == 1):
            minute = "0" + minute
            print("Fixed minute: ", minute)
          parts[0] = f"{hour}:{minute}"
          f2.write(f"{'|'.join(parts)}\n")  
        except Exception as e:
          f2.write(f"{line}\n")  

          print("Could not fix line: ", line)
          print("Exception: ", e)

        # 5:5|Precisely at five minutes before five o'clock, winter or summer, Lampe, Kant's servant, who had formerly served in the army, marched into his master's room with the air of a sentinel on duty, and cried aloud in a military tone,--'Mr.|6148|Narrative and Miscellaneous Papers|Thomas De Quincey|five minutes before five