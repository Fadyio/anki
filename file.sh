#To handle lines that start with "Question" followed by a number, a colon, a space, and then the rest of the text, you can use the following Perl command:
perl -pe 's/Question (\d+): /sprintf("Question %d: ", ++$i)/e' exams.txt > newfile.txt

#To count the number of occurrences of the word "question" (case-insensitive) in a file, you can use the following command:
grep -i -c 'Question' exams.txt

#To insert a blank line after the end of each line that starts with "Explanation", "CORRECT", or "INCORRECT", you can use the following Perl one-liner:
perl -pe 's/^(Explanation|CORRECT|INCORRECT).*/$&\n/' exams.txt > newfile.txt
