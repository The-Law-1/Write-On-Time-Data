#!/bin/bash

for i in {1001..2000}
do
   wget -H -P ./books https://www.gutenberg.org/ebooks/$i.txt.utf-8 --referer="http://www.google.com" \
      --user-agent="Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.6) Gecko/20070725 Firefox/2.0.0.6" \
      --header="Accept: text/xml,text/html;q=0.9,text/plain;" \
      --header="Accept-Language: en-us,en;q=0.5" \
      --header="Accept-Charset: ISO-8859-1,utf-8;q=0.7,*;q=0.7" \
      --header="Keep-Alive: 300"

   if [ $? -ne 0 ]; then
      echo "wget failed for https://www.gutenberg.org/ebooks/$i.txt.utf-8" >> wget_errors.log
   fi

   # running this will probably take at least a second 
   python3 ./parse_book.py ./books/$i.txt.utf-8 $i

   # delete the book(s) after by hand probably

   sleep 1
done
