import pandas as pd
from rule import Rule
from typing import List

class RuleCompressor:
    def __init__(self, data_path: str='data/dataset.tsv', rules_path: str='data/rules.txt'):
        self.data = pd.read_csv(data_path, sep='\t')
        self.rules = self.load_rules(rules_path)

    def load_rules(self, rules_path: str) -> List[Rule]:
        with open(rules_path, 'r') as file:
            rules = [Rule.expression_to_rule(line, self.data) for line in file] 
        return rules
    
    def remove_rules_worse_than_random(self):
        rhs_support = self.data['donor_is_old'].mean()
        # self.rules = [r for r in self.rules if r.confidence > rhs_support]
        self.rules = [r for r in self.rules if r.calculate_p_value(self.data) < 0.01]
    
    def remove_inclusive_rules(self):
        """
        If rule r1 is included in rule r2, remove the one with smaller confidence
        (in case of a tie, remove more complicated rule).
        """
        rules_to_remove = set()
        for i, r1 in enumerate(self.rules):
            for j, r2 in enumerate(self.rules):
                if i != j and r1.biomarkers.issubset(r2.biomarkers) and \
                              r1.negated_biomarkers.issubset(r2.negated_biomarkers):
                    if r1.confidence >= r2.confidence:
                        rules_to_remove.add(r2)
                    else:
                        rules_to_remove.add(r1)
        self.rules = list(set(self.rules) - rules_to_remove)
    
    def merge_rules(self):
        """
        For every rule r, find the rule r' for which merged rule r'' = r + r' has the highest confidence
        and replace r with r''.
        """
        rules_to_remove = set()
        rules_to_add = set()
        for i, r1 in enumerate(self.rules):
            best_merged_rule = r1
            for j, r2 in enumerate(self.rules):
                if i != j and r1.conclusion == r2.conclusion: # redundant in our testcase
                    merged_rule = Rule(r1.biomarkers.union(r2.biomarkers), 
                                       r1.negated_biomarkers.union(r2.negated_biomarkers), 
                                       r1.conclusion, self.data)
                    best_merged_rule = max(best_merged_rule, merged_rule, key=lambda r: r.confidence)
            if best_merged_rule != r1:
                rules_to_add.add(best_merged_rule)
                rules_to_remove.add(r1)
        self.rules = list((set(self.rules).union(rules_to_add)) - rules_to_remove)
    
    def save_rules(self, path: str):
        with open(path, 'w') as file:
            for rule in self.rules:
                file.write(str(rule) + '\n')
