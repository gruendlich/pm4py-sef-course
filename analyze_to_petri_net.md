# Part1： Cyclomatic Complexity 
measurement: 51 ($M = D + 1$)

```
Line 93: if parameters is None: (+1)
Line 106: if return_flow_trans_map: (+1)
Line 126: for flow in bpmn_graph.get_flows(): (+1)
Line 127: if isinstance(flow, BPMN.SequenceFlow): (+1)
Line 133: if source not in source_count: (+1)
Line 135: if target not in target_count: (+1)
Line 140: for flow in bpmn_graph.get_flows(): (+1)
Line 141: if isinstance(flow, BPMN.SequenceFlow): (+1)
Line 145-147: if (isinstance(...) and source_count[...] > 1): if : (+1) and : (+1)
Line 150-152: elif (isinstance(...) and target_count[...] > 1): elif: (+1) and : (+1)
Line 172: for node in bpmn_graph.get_nodes(): (+1)
Line 173-180: if : (+1) or (StartEvent): (+1) or (EndEvent): (+1) or (ExclusiveGateway): (+1) or (ParallelGateway): (+1) or (InclusiveGateway): (+1)
Line 181: if node not in source_count: (+1)
Line 183: if node not in target_count: (+1)
Line 190: if use_id: (+1)
Line 193/195: if isinstance(node, BPMN.Task) else None if : (+1)
Line 198: if not label: (+1)
Line 208-209: if isinstance(...) or isinstance(...): if : (+1) or : (+1)
Line 211: if source_count[node] > 1: (+1)
Line 221: if target_count[node] > 1: (+1)
Line 236: if isinstance(node, BPMN.StartEvent): (+1)
Line 242: elif isinstance(node, BPMN.EndEvent): (+1)
Line 249: for flow in bpmn_graph.get_flows(): (+1)
Line 250: if isinstance(flow, BPMN.SequenceFlow): (+1)
Line 251-253: if (flow.get_source() ... and flow.get_target() ...): if : (+1) and : (+1)
Line 258: if isinstance(source_object, PetriNet.Place): (+1)
Line 265: if isinstance(target_object, PetriNet.Place): (+1)
Line 275: if inclusive_gateway_exit and inclusive_gateway_entry: if : (+1) and : (+1)
Line 285: for pl1 in inclusive_gateway_exit: (+1)
Line 286: if pl1 in keys: (+1)
Line 288-292: List comprehension [... for x, y in ... if x in ...] for: (+1) if : (+1)
Line 295: if output_places: (+1)
Line 303: if enable_reduction: (+1)
Line 306: for place in list(net.places): (+1)
Line 307-311: if (len... and len... and place... and place...): if : (+1) and : (+1) and : (+1) and : (+1)
Line 315: if return_flow_trans_map: (+1)
```

**result: 51**
- We analyzed the apply function in to_petri_net.py
- Our manual CC count was consistently around 50-51. There were minor discrepancies initially regarding how to count list comprehensions (e.g., line 288) and complex boolean conditions (e.g., lines 173-180 with multiple or operators). We resolved this by agreeing to count each boolean operator (and, or) as an additional decision point (+1), which aligns with the standard definition. The automated tool lizard reported a CC of 52. This is extremely close to our manual count (51). 

**CC and LOC:**
- CC: 51
- NLOC: 196
- usually there is a strong correlation here

**purpose of the function and CC:**
- The function apply is a core conversion algorithm that translates a BPMN model (Business Process Model and Notation) into a Petri Net.
- The high CC comes from the need to switch logic based on the specific type of BPMN element being processed and the state of the graph (e.g. checking count of incoming/outgoing edges)

**exceptions:**
- lizard generally does not count try/except blocks as increasing cyclomatic complexity
- The "apply" function we analyzed does not use try/except blocks; it relies on standard conditional checks
- CC will go up if we think of an exception as another possible branch

**documentation of the function:**
It explains what the function does ("Converts a BPMN graph to an accepting Petri net") and explains the parameters, however it does not explain the different possible outcomes induced by different branches taken, the internal logic will be understood by reading the code

