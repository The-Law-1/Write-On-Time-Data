# Open the original file for reading
with open('approximate_google_times.csv', 'r') as original_file:
    # Open a new file for writing the processed lines
    with open('processed_approx_google_times.csv', 'w') as processed_file:
        # Iterate through each line in the original file
        for line in original_file:
          # Count the number of each type of quotation mark in the current line
          quote_counts = {
              '"': line.count('"'),
              '“': line.count('“'),
              '”': line.count('”'),
              "'": line.count("'"),
          }

          # Process the line to remove one of each type of quote if their count is odd
          for quote, count in quote_counts.items():
              if count % 2 != 0:
                  line = line.replace(quote, '', 1)

          # Write the processed line to the new file
          processed_file.write(line)
