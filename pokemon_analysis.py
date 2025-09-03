import pandas as pd
import numpy as np
import random
import string
import re
from statistics import median, stdev

class PokemonAnalyzer:
    def __init__(self, csv_file):
        """Initialize the analyzer with the Pokemon dataset."""
        self.df = pd.read_csv(csv_file)
        self.original_df = self.df.copy()
    
    def reset(self):
        """Reset the dataframe to its original state."""
        self.df = self.original_df.copy()
        
    def problem1_strongest_weakest(self):
        """Problem 1: Find the strongest and weakest pokemon based on Total stat."""
        strongest = self.df.loc[self.df['Total'].idxmax()]
        weakest = self.df.loc[self.df['Total'].idxmin()]
        
        print(f"Strongest Pokemon: {strongest['Name']} (Total: {strongest['Total']})")
        print(f"Weakest Pokemon: {weakest['Name']} (Total: {weakest['Total']})")
        
        return strongest, weakest
    
    def problem2_averagehp(self):
        """Problem 2: Find the average hit points (HP) of pokemons."""
        avg_hp = self.df['HP'].dropna().mean()
        
        print(f"Average HP: {avg_hp:.2f}")
        
        return avg_hp
    
    def problem3_rename(self):
        """Problem 3: Replace spaces with underscores and find single-type pokemons with last names."""
        
        # replace spaces with underscores
        self.df['Name'] = self.df['Name'].str.replace(' ', '_')
        
        # find pokemons with last names and only one type
        original_names = self.original_df['Name']
        names_with_spaces = original_names.str.contains(' ')
        single_type = self.df['Type 2'].isna() | (self.df['Type 2'] == '')
        
        # filter 
        filtered = self.df[names_with_spaces & single_type].copy()
        
        # extract last names
        original_filtered = self.original_df[names_with_spaces & single_type].copy()
        filtered['Last_Name'] = original_filtered['Name'].str.split(' ').str[-1]
        
        # remove duplicates
        filtered = filtered.drop_duplicates(subset=['#', 'Last_Name'])
        
        print("ID | Last Name")
        print("-" * 20)
        for _, row in filtered.iterrows():
            print(f"{row['#']} | {row['Last_Name']}")
        
        return filtered[['#', 'Last_Name']]
    
    def problem4_topten(self, field):
        """Problem 4: Function to return top ten pokemons based on a field."""
        top_ten = self.df.nlargest(10, field)
        return top_ten
    
    def problem5_lettercount(self, words, letter):
        """Problem 5: Function to return zeroIndexCount of a letter given a list of words."""
        count = sum(1 for word in words if word.lower().startswith(letter.lower()))
        return count
    
    def problem5_common_letter(self):
        """Problem 5: Find the letter with highest zeroIndexCount among pokemon names."""
        names = self.df['Name'].tolist()
        letters = string.ascii_lowercase
        
        letter_counts = {}
        for letter in letters:
            letter_counts[letter] = self.problem5_lettercount(names, letter)
        
        most_common_letter = max(letter_counts, key=letter_counts.get)
        max_count = letter_counts[most_common_letter]
        
        print(f"Most common starting letter: '{most_common_letter}' ({max_count} pokemon)")
        
        return most_common_letter, letter_counts
    
    def problem6_vowel_std_dev(self, letter_counts):
        """Problem 6: Calculate standard deviation of zeroIndexCounts for vowel letters."""
        vowels = ['a', 'e', 'i', 'o', 'u']
        vowel_counts = [letter_counts[vowel] for vowel in vowels]
        
        std_dev = stdev(vowel_counts)
        
        print(f"Vowel counts: {vowel_counts}")
        print(f"Standard deviation: {std_dev:.2f}")
        
        return std_dev
    
    def problem7_random_name(self):
        """Problem 7: Generate a random pokemon name (max 50 chars)."""
        # define possible name parts
        prefixes = ['char', 'pika','blast', 'fire', 'ice', 'water', 'earth', 'wind', 'shadow', 'light', 
                   'storm', 'flame', 'frost', 'volt', 'rock', 'steel', 'dark', 'psychic', 'ghost', 'dragon']
        suffixes = ['mon', 'izard', 'chu', 'saur', 'tle', 'gon', 'ite', 'eon', 'achu', 'mander', 
                   'puff', 'lord', 'master', 'wing', 'claw', 'fang', 'tail', 'eye', 'bug']
        
        # generate name parts 
        num_parts = random.randint(1, 4)
        name_parts = []
        
        for i in range(num_parts):
            if i == 0:
                # first part prefix
                name_parts.append(random.choice(prefixes))
            else:
                # can be prefixes or suffixes
                if random.choice([True, False]):
                    name_parts.append(random.choice(prefixes))
                else:
                    name_parts.append(random.choice(suffixes))
        
        # join with underscores
        name = '_'.join(name_parts)
        
        # split by underscores and capitalize
        parts = name.split('_')
        capitalized_parts = []
        
        for i, part in enumerate(parts):
            if part:  # part is not empty
                if i == 0:
                    # only first character capitalized for first part
                    capitalized_parts.append(part.capitalize())
                else:
                    # fully capitalized after underscores
                    capitalized_parts.append(part.upper())
        
        # join with underscores
        name = '_'.join(capitalized_parts)
        
        #  only letters and underscores 
        name = re.sub(r'[^a-zA-Z_]', '', name)
        
        #  name doesn't start with underscore
        if name.startswith('_'):
            name = name[1:]
            if name:  
                name = name[0].upper() + name[1:]
        
        # truncate if too long
        if len(name) > 50:
            truncated = name[:50]
            last_underscore = truncated.rfind('_')
            if last_underscore > 35:  
                name = truncated[:last_underscore]
            else:
                name = truncated
        
        # final valid name option 
        if not name or name.startswith('_'):
            name = random.choice(prefixes).capitalize()
        
        return name
    
    def problem8_normalize(self):
        """Problem 8: Normalize all numeric fields to (0-1) interval using min-max scaling."""
        num_columns = ['Total', 'HP', 'Attack', 'Defense', 'Sp. Atk', 'Sp. Def', 'Speed']
        
        for col in num_columns:
            if col in self.df.columns:
                min_val = self.df[col].min()
                max_val = self.df[col].max()
                if max_val > min_val:
                    self.df[col] = (self.df[col] - min_val) / (max_val - min_val)
                else:
                    self.df[col] = 0.0
        
        print("All numeric fields have been normalized to (0-1) interval")
    
    def problem9_new_row(self, strongest, weakest, avg_hp, letter_counts):
        """Problem 9: Add a new row with specified values."""
        # get the last ID
        last_id = self.df['#'].max()
        new_id = last_id + 1
        
        # generate random name
        new_name = self.problem7_random_name()
        
        # get most popular pokemon types (using Pikachu)
        pikachu = self.df[self.df['Name'].str.contains('Pikachu', case=False, na=False)]
        if not pikachu.empty:
            type1 = pikachu.iloc[0]['Type 1']
            type2 = pikachu.iloc[0]['Type 2']
        else:
            # fallback to first pokemon
            type1 = self.df.iloc[0]['Type 1']
            type2 = self.df.iloc[0]['Type 2']
        
        # get fastest pokemon's attack
        fastest = self.df.loc[self.df['Speed'].idxmax()]
        attack = fastest['Attack']
        
        # get strongest pokemon's defense
        defense = strongest['Defense']
        
        # get highest Sp.Atk among Fire and Dragon types
        fire_dragon = self.df[
            (self.df['Type 1'].isin(['Fire', 'Dragon'])) | 
            (self.df['Type 2'].isin(['Fire', 'Dragon']))
        ]
        if not fire_dragon.empty:
            sp_atk = fire_dragon['Sp. Atk'].max()
        else:
            sp_atk = self.df['Sp. Atk'].max()
        
        # get median Sp.Def of top 10 
        top_10_sp_def = self.problem4_topten('Sp. Def')
        sp_def = top_10_sp_def['Sp. Def'].median()
        
        # get median speed of top 10
        top_10_speed = self.problem4_topten('Speed')
        speed = top_10_speed['Speed'].median()
        
        # calculate total
        total = avg_hp + attack + defense + sp_atk + sp_def + speed
        
        # create new row
        new_row = {
            '#': new_id,
            'Name': new_name,
            'Type 1': type1,
            'Type 2': type2,
            'Total': total,
            'HP': avg_hp,
            'Attack': attack,
            'Defense': defense,
            'Sp. Atk': sp_atk,
            'Sp. Def': sp_def,
            'Speed': speed
        }
        
        # add to dataframe
        self.df = pd.concat([self.df, pd.DataFrame([new_row])], ignore_index=True)
        
        print(f"New Pokemon: {new_name} (ID: {new_id})")
        print(f"Total: {total:.2f}")
    
    def problem10_training_count(self, avg_hp):
        """Problem 10: Count pokemons that need training (moderate vs powerful)."""
        moderate_count = len(self.df[self.df['HP'] <= avg_hp])
        powerful_count = len(self.df[self.df['HP'] > avg_hp])
        
        print(f"Pokemon needing training (moderate): {moderate_count}")
        print(f"Powerful Pokemon: {powerful_count}")
        
        return moderate_count, powerful_count
    
    def problem11_sort(self):
        """Problem 11: Sort dataset by name."""
        self.df = self.df.sort_values('Name').reset_index(drop=True)
    
    def problem12_save(self, filename='pokemon_analysis_results.csv'):
        """Problem 12: Save manipulated dataset to new CSV file."""
        self.df.to_csv(filename, index=False)
    
    def run_analysis(self):
        """Run all problems in sequence."""
        print("Starting Pokemon Dataset Analysis...")
        print("=" * 50)
        
        strongest, weakest = self.problem1_strongest_weakest()
        
        avg_hp = self.problem2_averagehp()
        
        self.problem3_rename()
        
        self.problem4_topten('Speed')
        
        most_common_letter, letter_counts = self.problem5_common_letter()
        
        self.problem6_vowel_std_dev(letter_counts)
        
        self.problem7_random_name()
        
        self.problem9_new_row(strongest, weakest, avg_hp, letter_counts)
        
        self.problem10_training_count(avg_hp)

        self.problem8_normalize()
        
        self.problem11_sort()
        
        self.problem12_save()
        
        print("\n" + "=" * 50)
        print("Analysis complete!")

def main():
    """Main function to run the analysis."""
    # need to download the Pokemon dataset CSV file
    # and place it in the same directory as this script
    csv_file = 'pokemon.csv'  # update path as needed
    
    try:
        analyzer = PokemonAnalyzer(csv_file)
        analyzer.run_analysis()
    except FileNotFoundError:
        print(f"Error: Could not find {csv_file}")
        print("Please download the Pokemon dataset and place it in the same directory.")

if __name__ == "__main__":
    main()
