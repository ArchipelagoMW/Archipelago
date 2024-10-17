'''
- Assignments are built by randomly associating slots with items
- After an assignment is made, a list of branches is made:
    eg.  twinharp? dmist pan
         hook? kingqueen rubicant underground
         magmakey? underground
         (items with ? are checks for qualifications, others are received qualifications)
- The checker gets the list of branches
- The checker is then queried to make sure various assertions are true
    eg.  exists path to pan
         exists path to earth crystal without Zeromus

- How does this work?
  - first the accessible paths are evaluated
    - follow each path as far as it can go
      - every time we hit a "get", make a note of this branch up to the get, keyed by the thing gotten
    - repeat until we make no progress on any branch
  - when queried,
    - check each noted path to this terminus according to constraints
    - recursive check for each gated item on the path
'''



class DepChecker:
    def __init__(self):
        self._branches = []
        self._paths = {}

    def add_branch(self, *tokens):
        self._branches.append(tokens)

    def resolve(self):
        self._paths = {}
        indices = [0] * len(self._branches)
        progressed = True
        while progressed:
            progressed = False
            for i,branch in enumerate(self._branches):
                if indices[i] is None:
                    continue

                while indices[i] < len(branch):
                    if branch[indices[i]].endswith('?'):
                        qualification = branch[indices[i]][:-1]
                        if qualification not in self._paths:
                            # currently blocked at this position
                            break
                        else:
                            indices[i] += 1
                            progressed = True
                    else:
                        qualification = branch[indices[i]]
                        self._paths.setdefault(qualification, []).append(branch[:indices[i]])
                        indices[i] += 1
                        progressed = True

    def check(self, qualification, without=[], known_subqualifications=None, force=None):
        if qualification not in self._paths:
            return False, None

        for path in self._paths[qualification]:
            path_failed = False
            path_details = []
            if known_subqualifications is None:
                known_subqualifications = []
            for step in path:
                if step.endswith('?'):
                    subqualification = step[:-1]
                    if subqualification in without:
                        path_failed = True
                        break

                    if subqualification in known_subqualifications:
                        continue

                    subqualification_check, subpath = self.check(
                        subqualification, 
                        without=(without + [qualification]),
                        known_subqualifications=known_subqualifications
                        )
                    if not subqualification_check:
                        path_failed = True
                        break
                    path_details.extend(subpath)
                    path_details.append(subqualification)

                    known_subqualifications.append(subqualification)
                else:
                    if step in without:
                        path_failed = True
                        break
                    path_details.append(step)
                    
            if force and not force in path_details:
                path_failed = True
            if not path_failed:
                return True, path_details

        # found no path
        return False, None
