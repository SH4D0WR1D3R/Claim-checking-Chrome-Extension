# Module to handle retrieving evidence based on a claim or set of claims

# needs to do a google search essentially - can use the google-search module - python module
# 2 options for searching
    # - search for the exact claim
    # - search for the topics broken down from the claim
# probably better to search for exact claim but need to figure out about results - will need to break claim into topics anyways
# once the search has been executed, a topic check should be done against article headlines
# if topics match (unsure how to go about this since how many topics do we want matching?), that can be given to the user as a piece of evidence
# claims will need to be extracted from each article found and compared with the original claim