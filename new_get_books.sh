#!/bin/bash

generate_url() {
    book_number=$1
    url="http://aleph.gutenberg.org"

    for (( i=0; i<${#book_number} - 1; i++ )); do
        url+="/${book_number:$i:1}"
    done

    url+="/$book_number/$book_number.zip"

    echo $url
}

for i in {16647..20000}
do
  # http://aleph.gutenberg.org/1/2/3/7/12370/12370.zip
  URL=$(generate_url $i)
  
  echo "Downloading book $i from $URL"

  wget -q -m -H -O ./new_books/$i.zip $URL

  unzip ./new_books/$i.zip -d ./new_books

  if [ $? -ne 0 ]; then
    echo "wget failed for $URL" >> wget_errors.log
  fi

  # running this will probably take at least a second 
  python3 ./parse_book.py ./new_books/$i.txt $i

  # delete the book(s) after by hand probably
  rm ./new_books/$i.txt

  sleep 1
done
