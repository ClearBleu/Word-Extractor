import click
import requests #import request library
import re #Regular Expression (Regex) library module "re"
from bs4 import BeautifulSoup #bs4 module  to ignore HTML tags and metadata

#define function of getting the HTML source code of target
def get_html_of(url):
    resp = requests.get(url)
    #in case target IP was mistyped and an error occured
    if resp.status_code != 200:
        print(f'HTTP status code of {resp.status_code} returned, but 200 was expected. EXITING...')
        exit(1)

    return resp.content.decode()


def count_occurrences_in(word_list, min_length): #function to count all occurences of word
    word_count = {} #Empty dictionary; variable to store words counted in the target HTML

    for word in word_list:
        if len(word) < min_length:
            continue
        if word not in word_count:
            word_count[word] = 1
        else:
            current_count = word_count.get(word)
            word_count[word] = current_count + 1
    return word_count

def get_all_words_from(url):  #Gather all words
    
    html = get_html_of(url)
    soup = BeautifulSoup(html, 'html.parser')
    raw_text = soup.get_text()
    return re.findall(r'\w+', raw_text)


def get_top_words_from(all_words, min_length): #takes URL as parameter, then uses URL to call another function that gets the list needed
    occurrences = count_occurrences_in(all_words, min_length)
    return sorted(occurrences.items(), key= lambda item: item[1], reverse=True)

@click.command()
@click.option('--url', '-u', prompt='Web URL', help='URL of webpage to extract from.') #http://ip:port/ format
@click.option('--length', '-l', default=0, help='Minimum word length (default: 0, no limit).') #--length format # <-new minimum word length value #Tried -l and wouldn't produce words
def main(url, length):
    the_words = get_all_words_from(url) #variable storing target IP and Port
    top_words = get_top_words_from(the_words, length)


    for i in range(10): #arrange words in ranked 1-10 order according to occurrence in target HTML
        print(top_words[i][0])


if __name__ == '__main__':
    main()

    
