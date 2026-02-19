# Report for assignment 3

## Project information

Name: PM4Py

URL: https://github.com/process-intelligence-solutions/pm4py

PM4Py is a python library that supports state-of-the-art process mining algorithms in Python. It is open source and intended to be used in both academia and industry projects.
## Onboarding experience
We had to install the two following additional tools to build the software:
- Python packages from requirements_complete.txt + pulp
- Graphviz

There were documentation of the Python packages but no mentions of Graphviz and pulp was only noticeable via debugging.

Once everything was installed the build concluded automatically without any errors. All tests run through.

## Complexity
#### Lizard's result:
~~~
apply_partial_order_projection: 16 CCN
comparison_symmetric.py: 27 CCN
ocel_consistency.py: 16 CCN
to_petri_net.py: 52 CCN
get_base_ocel.py: 24 CCN
~~~

#### Manually Calculated

Complexity calculated by 1 + Number of (if, else, for, while) (McCabe)
~~~
apply_partial_order_projection: 16
ocel_consistency.py: 16
get_base_ocel: 24
to_petri_net.py: 38
comparison.symmetric.py: 28
~~~

In our opinion, there are multiple branches that easily can be merged together to reduce complexity, for example, without the need to divide the functionality into subsequent functions. However, whether the reduction of branches always results in more readable code in this particular case remains a point of discussion. The only exception to this would be the function in to_petri_net.py where the high CC comes from the need to switch logic based on the specific type of BPMN element being processed.

Documentation: 
Function documentation only describes the purpose of it and of its parameters. I.e., lacks proper explanation of its internal behavior. However, a developer should not be expected to document such behavior for more auxiliary functions.

## Refactoring

### Refactoring plan performed on function [apply_partial_order_projection](https://github.com/gruendlich/pm4py-sef-course/blob/gruendlich/refactoring/pm4py/objects/conversion/wf_net/variants/to_powl.py):
1. Extract validation helper
- validate_unique_local_boundary(places, reference, subnet_transitions, kind)
- Responsibility: check all places are locally_identical to the first; raise with a clear message.
2. Extract boundary cloning helper
- clone_boundary_places(subnet_net, node_map, start_places, end_places, subnet_transitions)
- Responsibility: create new_start_place, decide whether end equals start, otherwise validate and clone end. Return (new_start_place, new_end_place, boundary_places_set).
3. Extract “get-or-clone node” helper with boundary skip
- get_or_clone_place(subnet_net, node_map, place, boundary_places) returns None if the place is a boundary place and should be skipped, else returns the mapped/cloned place.
4. Extract arc cloning loop
- clone_subnet_arcs(original_net, subnet_net, node_map, subnet_transitions, boundary_places)
- Responsibility: iterate arcs, apply “in subnet?” filter, resolve endpoints via helpers, add arcs.
5. Keep apply_partial_order_projection as a short orchestration function calling the helpers.

CC results after refactoring for apply_partial_order_projection: 2 CCN
___

### Refactoring plan performed on function 'apply' in [comparison_symmetric.py](https://github.com/gruendlich/pm4py-sef-course/blob/juozas/refactoring/pm4py/visualization/footprints/variants/comparison_symmetric.py):
Apply function delegating certain behavior to two new local functions:
One that merges activity (data) lists and returns merged, first and the second lists as a 3-tuple.
One that performs comparison on individual list items.

CC results after refractoring for apply in comparison.symmetric.py: 9 CCN

___

### Refactoring plan performed on function [get_base_ocel](https://github.com/gruendlich/pm4py-sef-course/blob/rayon/refactoring/pm4py/objects/ocel/importer/jsonocel/variants/classic.py):

High complexity is partly due to multiple responsibilities handled in one function as the function parses objects, events, relations, O2O links, object changes, and dataframe normalization all together. The complexity is structural rather than algorithmically necessary and can be split into smaller helper functions without changing behavior.


1. Extract object parsing into a helper that builds objects, types dictionary, and O2O relations


2. Extract event parsing into a helper that builds events and relations


3. Extract relation normalization and indexing into a helper


4. Extract object change processing into a helper


5. Keep get_base_ocel as an orchestration layer calling the helpers


This improves readability and maintainability.

___

### Refactoring plan performed on function 'apply' in [to_petri_net.py](https://github.com/gruendlich/pm4py-sef-course/blob/jintong/refactoring/pm4py/objects/conversion/bpmn/variants/to_petri_net.py):

This "God Function" handles initialization, traversal, logic mapping, and optimization all in one place.

Proposed New Structure:
We can extract 4 distinct helper functions to handle specific logical blocks:

1. _initialize_petri_net()

- Create the PetriNet object, source/sink places, and initial/final markings.

2. _process_bpmn_nodes(bpmn_graph, net, source_count, target_count, ...)
- Iterate through all BPMN nodes (Tasks, Gateways, Events) and create their corresponding Petri net transitions and places.

3. _connect_flows(bpmn_graph, net, nodes_entering, nodes_exiting, ...)
- Iterate through BPMN flows and add arcs between the Petri net elements created in the previous step.

4. _handle_inclusive_gateways(net, inclusive_gateway_exit, inclusive_gateway_entry)
- Execute the specific optimization logic for OR-gateways (calculating shortest paths and adding invisible transitions).

___

### Refactoring plan on function 'apply' in [ocel_consistency.py](https://github.com/gruendlich/pm4py-sef-course/blob/student-main/pm4py/objects/ocel/util/ocel_consistency.py) (not implemented):

The function is very clearly structured into different parts and most of them could all be put into their own separate functions. 

1. for-loop on lines 72-126 is moved to a separate function named process_dataframe(fields) which returns setattr(ocel, tab, df)

Just doing this would remove 4 for-loops and 6 if-statements from the apply function leaving us with a CC of 6.

2. Additionally, the uniqueness checks with 4 if statements could be moved to a separate function, leaving us with a CC of 2 (one if-statement + 1).



## Coverage

### Tools

We used coverage.py to calculate the coverage of our code and it was really straighforward with no issues as it is a well documented and tested tool.

~~~
### Your own coverage tool

Show a patch (or link to a branch) that shows the instrumented code to
gather coverage measurements.

The patch is probably too long to be copied here, so please add
the git command that is used to obtain the patch instead:

git diff ...

What kinds of constructs does your tool support, and how accurate is
its output?

### Evaluation

1. How detailed is your coverage measurement?

2. What are the limitations of your own tool?

3. Are the results of your tool consistent with existing coverage tools?

## Coverage improvement

Show the comments that describe the requirements for the coverage.

Report of old coverage: [link]

Report of new coverage: [link]

Test cases added:

git diff ...

Number of test cases added: two per team member (P) or at least four (P+).

## Self-assessment: Way of working

Current state according to the Essence standard: ...

Was the self-assessment unanimous? Any doubts about certain items?

How have you improved so far?

Where is potential for improvement?

## Overall experience

What are your main take-aways from this project? What did you learn?

Is there something special you want to mention here?

~~~

## Contributions:
**Adrian Grund** (Github: gruendlich): Worked with the to_powl.py file, manually instrumenting and analysing it and adding unittests. Also wrote our manual coverage check tool. 

**Juozas Skarbalius** (GitHub: terahidro2003): Worked with the comparison_symmetric.py file, manually instrumenting and analysing it and adding unittests.

**Alberto Rayon**  (GitHub: AlbertoRayon): Worked with the classic.py file, manually instrumenting and analysing it and adding unittests.

**Jintong Jang** (GitHub: kaffe1): Worked with the to_petri_net.py file, manually instrumenting and analysing it and adding unittests.

**Bahar Kimanos** (Github: baharkim): Worked with the ocel_consistency.py file, manually instrumenting and analysing it and adding unittests.