# Fictional workflow policy v1

Synthetic training rule.

A review starts pending. A named human reviewer may mark it approved or rejected. The model may propose a review but may not approve it. Repeating a request ID with the same payload returns the existing review. A different payload with the same request ID is a conflict. Bulk changes are outside this lab.
