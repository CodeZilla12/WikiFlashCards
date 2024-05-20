# WikiFlashCards

Flashcard practice software with auto-generated flashcard sets from Wikipedia

## Overview

You can create new flashcard files from the homepage, as well as edit them in the toplevel widget - where you can scroll through, delete and add new flashcards.

The wiki-generated flashcards are still in alpha. The goal being to supply the program with a wikipedia link, it will crawl through that link with to grab exponentially more links up to a specified search depth, gather the words from the link, and automatically translate them, auto-generating a flashcard file. So you could supply a link such as "https://lt.wikipedia.org/wiki/%C5%A0altibar%C5%A1%C4%8Diai" with a relatively short search-depth to get food-related flashcards etc. Currently the links are limited to lt.wikipedia, the search depth is locked at zero (due to link numbers growing unnaturally large), and the translation API is rather buggy. Hence the warning that this feature is still in alpha. This will be the next feature to be developed.

When reviewing flashcards, a group of X words (defined in the config) are chosen from the flashcard file selected on the home page. The likelihood of the word showing up is based on the score given to that flashcard. A score of -5 would mean you will almost always see that flashcard, and a score of +5 will mean that you will almost never see that flashcard (unseen flashcards begin at 0). The score is increased or decreased based on your answer from fail -> easy, giving -1 -> +1 points each time. The maximum and minimum scores can be modified in the config.


Note: you will need the alpha version of googletrans to run the wiki flashcard generation:
```
pip install googletrans==3.1.0a0
```

## Screenshots

![HomePage](https://github.com/Sam-Gledhill/WikiFlashCards/assets/69915380/b75d4344-2155-4c29-85d2-ef7b57b9ef26)


![EditFlashcardPage](https://github.com/Sam-Gledhill/WikiFlashCards/assets/69915380/c0a7be2f-3898-4b1b-b65e-5873cfdc51f8)


![ShowWordPage](https://github.com/Sam-Gledhill/WikiFlashCards/assets/69915380/c798e8d8-7351-4ddc-8b93-debda673b646)


![AnswerPage](https://github.com/Sam-Gledhill/WikiFlashCards/assets/69915380/1f8d3ce8-d458-445b-9533-59bc74940818)


![GraphPage](https://github.com/Sam-Gledhill/WikiFlashCards/assets/69915380/46d1ca06-fea6-4d16-ab75-caa8df154c99)
