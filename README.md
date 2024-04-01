# StringPairFinder

StringPairFinder is a Python package designed to simplify the process of finding similarities between strings.

<p align="center">
  <img src="https://github.com/AntoinePinto/string-pair-finder/blob/master/img/problematic.png?raw=true" alt="drawing" width="400"/>
</p>

## Evaluation

Evaluation on a dataset of 1000 observations (see `notebooks/1_evaluation.ipynb`) :
* [FuzzyWuzzy](https://github.com/seatgeek/thefuzz) algorithm : 85.2 % of success rate
* StringPairFinder algorithm : 94.0 % of success rate

## Installation

```python
pip install stringpairfinder
```

## Usage

### Computing String Similarity

```python
import stringpairfinder as spf

spf.get_similarity("Munich", "Munchen")
```

```python
>> 0.23809523809523808
```

### Finding the Nearest String

```python
spf.get_nearest_string(
    string="Naples",
    string_list=["Munchen", "Napoli", "Warszawa"]
    )
```

```python
>> 'Napoli'
```

### Mapping Strings to Their Nearest Counterparts

```python
spf.match_strings(
    source_strings=["Naples", "Munich", "Warsaw"],
    target_strings=["Munchen", "Napoli", "Warszawa"]
    )
```

```python
>> {'Naples': 'Napoli',
    'Munich': 'Munchen',
    'Warsaw': 'Warszawa'}
```

## What is the algorithm ?

The similarity search between two strings consists of a matrix comparison of each character in those strings. Let"s assume we want to compare the strings "Munich" and "Bayern Munich". 

1. The first step is to construct a table $T$ containing the first string in the column and the second in the row. The value of a cell is 1 if the character in the row is the same as the one in the column, and 0 otherwise.

<p align="center">
  <img src="https://github.com/AntoinePinto/string-pair-finder/blob/master/img/step1.png?raw=true" alt="drawing" width="300"/>
</p>

2. The second step aims at highlighting the fact that several characters correspond consecutively. Thus, for each row $i$ and column $j$, if cell $T[i-1, j-1] > 0$, then $T[i, j]$ is twice the value of $T[i-1, j-1]$.

<p align="center">
  <img src="https://github.com/AntoinePinto/string-pair-finder/blob/master/img/step2.png?raw=true" alt="drawing" width="300"/>
</p>

3. The third step is simply to calculate the similarity score, equal to the sum of all the cells in the $T$ divided by the size of the table.

$$ Score = \frac{\sum_{i=1}^{n_{row}}\sum_{j=1}^{n_{col}} T_{i,j}}{n_{row} * n_{col}}  = \frac{1+1+2+4+8+16+32}{78} \approx 0.82 $$

In this example, we obtain a similarity score of 64.

To connect the peers two by two, StringPairFinder calculates the similarity score of all (list1, list2) combinations and returns the association between each character string in list 1 with the character string in list 2 with the highest similarity score.