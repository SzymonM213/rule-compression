from rule_compressor import RuleCompressor
from rule import Rule
import pandas as pd

def main():
    compressor = RuleCompressor()
    compressor.remove_rules_worse_than_random()
    # while any(r.confidence != 1 for r in compressor.rules):
    #     compressor.merge_rules()
    #     compressor.remove_inclusive_rules()
            
    compressor.save_rules('data/new_rules.txt')

if __name__ == "__main__":
    main()