# Part1： Cyclomatic Complexity 
measurement: 38 ($M = D + 1$)

```
Line 93: if parameters is None: (+1)
Line 106: if return_flow_trans_map: (+1)
Line 126: for flow in bpmn_graph.get_flows(): (+1)
Line 127: if isinstance(flow, BPMN.SequenceFlow): (+1)
Line 133: if source not in source_count: (+1)
Line 135: if target not in target_count: (+1)
Line 140: for flow in bpmn_graph.get_flows(): (+1)
Line 141: if isinstance(flow, BPMN.SequenceFlow): (+1)
Line 145-147: if (isinstance(...) and source_count[...] > 1): if : (+1)
Line 150-152: elif (isinstance(...) and target_count[...] > 1): elif: (+1)
Line 172: for node in bpmn_graph.get_nodes(): (+1)
Line 173-180: if : (+1)
Line 181: if node not in source_count: (+1)
Line 183: if node not in target_count: (+1)
Line 190: if use_id: (+1)
Line 193/195: if isinstance(node, BPMN.Task) else None if : (+1)
Line 198: if not label: (+1)
Line 208-209: if isinstance(...) or isinstance(...): if : (+1)
Line 211: if source_count[node] > 1: (+1)
Line 221: if target_count[node] > 1: (+1)
Line 236: if isinstance(node, BPMN.StartEvent): (+1)
Line 242: elif isinstance(node, BPMN.EndEvent): (+1)
Line 249: for flow in bpmn_graph.get_flows(): (+1)
Line 250: if isinstance(flow, BPMN.SequenceFlow): (+1)
Line 251-253: if (flow.get_source() ... and flow.get_target() ...): if : (+1)
Line 258: if isinstance(source_object, PetriNet.Place): (+1)
Line 265: if isinstance(target_object, PetriNet.Place): (+1)
Line 275: if inclusive_gateway_exit and inclusive_gateway_entry: if : (+1)
Line 285: for pl1 in inclusive_gateway_exit: (+1)
Line 286: if pl1 in keys: (+1)
Line 288-292: List comprehension [... for x, y in ... if x in ...] for: (+1) if : (+1)
Line 295: if output_places: (+1)
Line 303: if enable_reduction: (+1)
Line 306: for place in list(net.places): (+1)
Line 307-311: if (len... and len... and place... and place...): if : (+1)

**result: 38**
- We analyzed the apply function in to_petri_net.py
- Our manual CC count was consistently around 38. There were minor discrepancies initially regarding how to count list comprehensions (e.g., line 288) and complex boolean conditions (e.g., lines 173-180 with multiple or operators). **We resolved this by agreeing not to count each boolean operator (and, or) as an additional decision point (+1) **. The automated tool lizard reported a CC of 52. The differences exists because it includes boolean operators as decision points, while we do not. 

**CC and LOC:**
- CC: 38
- NLOC: 196
- usually there is a strong correlation here

**purpose of the function and CC:**
- The function apply is a core conversion algorithm that translates a BPMN model (Business Process Model and Notation) into a Petri Net.
- The high CC comes from the need to switch logic based on the specific type of BPMN element being processed.

**exceptions:**
- lizard generally does not count try/except blocks as increasing cyclomatic complexity
- The "apply" function we analyzed does not use try/except blocks; it relies on standard conditional checks
- CC will go up if we think of an exception as another possible branch

**documentation of the function:**
It explains what the function does ("Converts a BPMN graph to an accepting Petri net") and explains the parameters, however it does not explain the different possible outcomes induced by different branches taken, the internal logic will be understood by reading the code

# Part 2: Coverage measurement & improvement
## Task 1: DIY Coverage Measurement
We implemented manual instrumentation for the `apply` function in `to_petri_net.py` by injecting `mark_branch(id)` calls at decision points.

### Results
Running `tests/bpmn_tests.py` (specifically `test_bpmn_to_petri_net`) produced the following coverage:

**Covered Branches (31/42 = ~74%):**
```
--- Manual Branch Coverage Report ---

  "branch_2_parameters_not_none": true,
  "branch_4_return_flow_trans_map_false": true,
  "branch_5_loop_flows": true,
  "branch_6_is_sequence_flow": true,
  "branch_7_source_not_in_count": true,
  "branch_8_target_not_in_count": true,
  "branch_9_loop_flows_2": true,
  "branch_10_is_sequence_flow_2": true,
  "branch_13_no_inclusive_gateway": true,
  "branch_14_loop_nodes": true,
  "branch_15_supported_node_type": true,
  "branch_19_use_id_false": true,
  "branch_20_label_is_none": true,
  "branch_26_not_gateway": true,
  "branch_21_is_parallel_or_inclusive_gateway": true,
  "branch_22_gateway_source_count_gt_1": true,
  "branch_25_gateway_target_count_le_1": true,
  "branch_23_gateway_source_count_le_1": true,
  "branch_24_gateway_target_count_gt_1": true,
  "branch_17_node_not_in_target_count": true,
  "branch_27_is_start_event": true,
  "branch_16_node_not_in_source_count": true,
  "branch_28_is_end_event": true,
  "branch_29_loop_flows_3": true,
  "branch_30_is_sequence_flow_3": true,
  "branch_31_flow_source_target_valid": true,
  "branch_32_source_is_place": true,
  "branch_33_target_is_place": true,
  "branch_38_enable_reduction_true": true,
  "branch_39_loop_cleanup_places": true,
  "branch_42_return_standard": true
}
-------------------------------------
```
**Missing Branches (11/42):**
- `branch_1_parameters_none`: **Handle implicit parameters.** Triggered when the function is called without providing a `parameters` dictionary (defaulting to None).
- `branch_3_return_flow_trans_map_true`: **Extended Return Mode.** Triggered when `RETURN_FLOW_TRANS_MAP` is set to True, disabling reduction and preparing to return extra mapping data.
- `branch_11_inclusive_gateway_exit`: **Inclusive Split Detection.** Triggered when an `InclusiveGateway` node is found to have multiple outgoing sequence flows (OR-split).
- `branch_12_inclusive_gateway_entry`: **Inclusive Join Detection.** Triggered when an `InclusiveGateway` node is found to have multiple incoming sequence flows (OR-join).
- `branch_18_use_id_true`: **ID-based Naming.** Triggered when `USE_ID` is set to True, forcing the Petri net transitions to use IDs as labels/names instead of node names.
- `branch_34_inclusive_gateway_optimization`: **OR-Gateway Optimization Logic.** The entry point for a complex block that adds invisible transitions between OR-splits and OR-joins to ensure model soundness.
- `branch_35_loop_inclusive_exit`: **Optimization Loop.** Part of the optimization logic that iterates through all identified OR-splits.
- `branch_36_pl1_in_keys`: **Reachability Check.** specific check within the optimization to ensure the OR-split is part of the calculated reachability graph.
- `branch_37_output_places_exist`: **Link Creation.** Triggered when a path is found between an OR-split and OR-join, prompting the creation of a synchronizing invisible transition.
- `branch_40_remove_unconnected_place`: **Cleanup Logic.** Triggered if the conversion results in isolated places (no arcs in/out), removing them from the final net.
- `branch_41_return_flow_trans_map`: **Extended Return Statement.** The specific return statement executing when extended return values (mappings) are requested.

### Quality and Limitations
- **Quality:** The manual instrumentation is robust for block coverage. It accounts for `elif` chains and specific boolean conditions implicitly by where we placed the markers.
- **Limitations:** It requires intrusive code changes. It cannot easily track "condition coverage" (e.g., if `A and B` is false because A is false or B is false) without breaking up compound statements. 
- **Comparison:** We don't have an automated tool setup for comparison, but the results align with expectations

## Task 2: Coverage Improvement

We created `tests/bpmn_coverage_test.py` which specifically targets the parameter-driven branches.
Running this new test suite successfully covered:
- `branch_1_parameters_none` (Tested by calling `apply(bpmn, parameters=None)`)
- `branch_18_use_id_true` (Tested by calling `apply(..., parameters={USE_ID: True})`)
- `branch_3_return_flow_trans_map_true` & `branch_41_return_flow_trans_map` (Tested by enabling the return map parameter)

**Impact:**
- Before: 31 branches covered.
- After (Union of both test suites): 31 + 4 (new unique branches) = **35/42** branches covered.
- Improvement: Coverage increased from ~74% to ~83%.

**Remaining Weak Spots:**
- The complex logic for **Inclusive Gateway Optimization** (`branch_11`, `branch_12`, `branch_34`, etc.) remains uncovered. This logic requires specific graph structures (multiple flows entering/exiting inclusive gateways) to trigger. Achieving coverage here would require constructing a specific BPMN graph with these patterns.


