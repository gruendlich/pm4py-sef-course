# Part1： Cyclomatic Complexity 
measurement: 51 ($M = D + 1$)


```

For loops (8)
Line ~21: for obj_id in json_obj[OCEL_OBJECTS_KEY]: (+1)
Line ~27: for k, v in obj[OCEL_OVMAP_KEY].items(): (+1)
Line ~31: for newel in this_rel_objs: (+1)
Line ~45: for ev_id in json_obj[OCEL_EVENTS_KEY]: (+1)
Line ~52: for k, v in ev[OCEL_VMAP_KEY].items(): (+1)
Line ~55: for obj in ev[OCEL_OMAP_KEY]: (+1)
Line ~66: for element in ev[OCEL_TYPED_OMAP_KEY]: (+1)
Line ~74: for obj in this_rel: (+1)

If / elif (13)
Line ~29: if constants.OCEL_O2O_KEY in obj: (+1)
Line ~56: if obj in types_dict: (+1)
Line ~64: if constants.OCEL_TYPED_OMAP_KEY in ev: (+1)
Line ~67: if object_id in element: (+1)
Line ~69: if key1 in this_rel: (+1)
Line ~78: if constants.OCEL_OBJCHANGES_KEY in json_obj: (+1)
Line ~86: if len(relations) == 0: (+1)
Line ~100: if len(relations) > 0: (+1)
Line ~107: if len(relations) > 0: (+1)
Line ~111: if internal_index in relations.columns: (+1)
Line ~121: if object_changes is not None and len(object_changes) > 0: if : (+1) and : (+1)
Line ~118: o2o = ... if o2o else None  if : (+1) else : (+1)
Line ~119: object_changes = ... if object_changes else None  if : (+1) else : (+1)

**result: 24**

1. We analyzed the function get_base_ocel and all counted a CC of 24. This is exactly what the lizard tool got as well.

2. Usually there is a strong correlation between CC and NLOC. This function had 154 NLOC.

3. The get_base_ocel function takes an OCEL JSON object and converts it into an OCEL log object. The function achieves this by extracting and organizing the events, objects, and their relationships.

4. This function did not make any use of try/except exception handling despite it being available in the java language.

5. The documentation was not clear about this and I was able to understand it more just by reading the code.