# Pokemon Dataset Analysis

This project analyzes a given Pokemon dataset and solves 12 specific problems related to data manipulation.

## Setup

1. Install the required dependencies:

pip install -r requirements.txt


2. Download the Pokemon dataset CSV file and place it in the same directory as the script, naming it `Pokemon.csv`.

## Usage

Run the analysis script:
```bash
python pokemon_analysis.py
```

## Problems Solved

1. **Find strongest and weakest Pokemon** based on Total stat
2. **Calculate average HP** of all Pokemon
3. **Replace spaces with underscores** and find single-type Pokemon with last names
4. **Top 10 function** to return top Pokemon based on any field
5. **ZeroIndexCount function** and find most common starting letter
6. **Standard deviation** of vowel letter counts
7. **Random Pokemon name generator** with specific formatting rules
8. **Normalize numeric fields** to (0-1) interval
9. **Add new Pokemon row** with calculated values
10. **Count Pokemon needing training** (moderate vs powerful)
11. **Sort dataset by name**
12. **Save results to new CSV file**

## Output

The script will:
- Print detailed results for each problem
- Generate a new CSV file (`pokemon_analysis_results.csv`) with all modifications
- Show statistics and analysis for each step
