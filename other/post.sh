#!/bin/bash

echo -n "Author : "
read author
echo -n "Quote : "
read quote
curl -d "author=$author;quote=$quote" http://quotes.matael.org 
