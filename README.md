# Rule Compression
Class for compressing set of rules. For ranking rules, it uses confidence, that
estimates probability that LHS occurs given that RHS does. It is good metric
in our case because the number of rows where donor is old is similar to the number
of rows when he's not.

### Usage
```bash
python main.py
```
This command will run a simple script that performs the compression operations
and ensure that all the new rules have confidence = 1.0 and they are not
too complicated.

### Heuristics used for cleaning rules provided by RuleCompressor class:
- Remove rules that have confidence <= 0.5, as a random rule would have
  expected confidence of 0.5
- For two rules r1 and r2, if LHS of r1 includes LHS of r2, remove the one with
  smaller confidence. It makes sense in both cases because removing r1 means that
  it was too complicated and simplier sub-rule r2 performed better on our 
  dataset; removing r2 means that we can improve r2 by adding conditions from r1
- Merging rules - for every rule r, we iterate over all the other rules and we
  choose a rule r' for which combined LHS of r and r' has the highest confidence.
  If that confidence is greater than confidence of r, we remove r and add the new
  rule.

Let's see that the 2nd and 3rd operation have such property, that for every old
rule r_old we can find a new rule r_new such that the r_old is included in r_new.

In our case, we can perform the 2nd and 3rd operation merging pairs of rules and
removing the redundant ones as long as all the confidences don't equal 1 because 
this happens relatively fast.