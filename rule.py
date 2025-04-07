import pandas as pd

class Rule:
    def __init__(self, biomarkers: set, negated_biomarkers: set, conclusion: str, data: pd.DataFrame):
        self.biomarkers = biomarkers
        self.negated_biomarkers = negated_biomarkers
        self.conclusion = conclusion
        self.confidence = self.calculate_confidence(data)

    def __eq__(self, other: object) -> bool:
        return (self.biomarkers == other.biomarkers and
                self.negated_biomarkers == other.negated_biomarkers and
                self.conclusion == other.conclusion)
    
    def __hash__(self) -> int:
        return hash((frozenset(self.biomarkers), frozenset(self.negated_biomarkers), self.conclusion))
    
    def __str__(self) -> str:
        return self.rule_to_expression()
    
    def __repr__(self) -> str:
        return self.__str__()
        
    def calculate_confidence(self, data: pd.DataFrame) -> float:
        valid_data = data[data[self.conclusion].notna() & 
                          data[list(self.biomarkers.union(self.negated_biomarkers))].notna().all(axis=1)]
        lhs_mask = valid_data[list(self.biomarkers)].all(axis=1) & ~valid_data[list(self.negated_biomarkers)].any(axis=1)
        rhs_mask = valid_data[self.conclusion]
        support_lhs_rhs = valid_data[lhs_mask & rhs_mask].shape[0]
        support_lhs = valid_data[lhs_mask].shape[0]
        return support_lhs_rhs / support_lhs if support_lhs > 0 else 0.0
    
    def rule_to_expression(self) -> str:
        result = ' AND '.join([f'{biomarker}' for biomarker in self.biomarkers] +
                              [f'NOT {biomarker}' for biomarker in self.negated_biomarkers])
        result += f' => {self.conclusion}'
        return result
        
    @staticmethod
    def expression_to_rule(expression: str, data: pd.DataFrame):
        parts = expression.split('=>')[0].strip().split('AND')
        biomarkers = set([part.strip() for part in parts if 'NOT' not in part])
        negated_biomarkers = set([part.replace('NOT', '').strip() for part in parts if 'NOT' in part])
        conclusion = expression.split('=>')[1].strip()
        return Rule(biomarkers, negated_biomarkers, conclusion, data)
    
