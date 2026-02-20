'''
    PM4Py – A Process Mining Library for Python
Copyright (C) 2024 Process Intelligence Solutions UG (haftungsbeschränkt)

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as
published by the Free Software Foundation, either version 3 of the
License, or any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see this software project's root or
visit <https://www.gnu.org/licenses/>.

Website: https://processintelligence.solutions
Contact: info@processintelligence.solutions
'''
import uuid
from enum import Enum

from pm4py.objects.petri_net.utils import reduction
import json
import atexit

# Coverage storage
coverage_data = {}

def dump_coverage():
    print("\n--- Manual Branch Coverage Report ---")
    print(json.dumps(coverage_data, indent=2))
    print("-------------------------------------")

atexit.register(dump_coverage)

def mark_branch(branch_id):
    coverage_data[branch_id] = True
from pm4py.objects.petri_net.obj import PetriNet, Marking
from pm4py.objects.bpmn.obj import BPMN
from pm4py.objects.petri_net.utils.petri_utils import remove_place
from pm4py.objects.petri_net.utils.petri_utils import add_arc_from_to
from pm4py.util import exec_utils, nx_utils


class Parameters(Enum):
    USE_ID = "use_id"
    ENABLE_REDUCTION = "enable_reduction"
    RETURN_FLOW_TRANS_MAP = "return_flow_trans_map"


def build_digraph_from_petri_net(net):
    """
    Builds a directed graph from a Petri net
        (for the purpose to add invisibles between inclusive gateways)

    Parameters
    -------------
    net
        Petri net

    Returns
    -------------
    digraph
        Digraph
    """
    graph = nx_utils.DiGraph()
    for place in net.places:
        graph.add_node(place.name)
    for trans in net.transitions:
        in_places = [x.source for x in list(trans.in_arcs)]
        out_places = [x.target for x in list(trans.out_arcs)]
        for pl1 in in_places:
            for pl2 in out_places:
                graph.add_edge(pl1.name, pl2.name)
    return graph


def apply(bpmn_graph, parameters=None):
    """
    Converts a BPMN graph to an accepting Petri net

    Parameters
    --------------
    bpmn_graph
        BPMN graph
    parameters
        Parameters of the algorithm:
        - Parameters.USE_ID => (default: False) uses the IDs of the objects instead of their labels in the conversion
        - Parameters.ENABLE_REDUCTION => reduces the invisible transitions
        - Parameters.RETURN_FLOW_TRANS_MAP => returns additional information on the conversion:
                                                (iv) the places of the obtained Petri net that are corresponding to each
                                                    BPMN flow.
                                                (v) the transitions of the Petri net related to the nodes of the BPMN
                                                    diagram.

    Returns
    --------------
    net
        Petri net
    im
        Initial marking
    fm
        Final marking
    """
    if parameters is None:
        mark_branch("branch_1_parameters_none")
        parameters = {}
    else:
        mark_branch("branch_2_parameters_not_none")

    from pm4py.objects.bpmn.obj import BPMN

    use_id = exec_utils.get_param_value(Parameters.USE_ID, parameters, False)
    return_flow_trans_map = exec_utils.get_param_value(
        Parameters.RETURN_FLOW_TRANS_MAP, parameters, False
    )
    enable_reduction = exec_utils.get_param_value(
        Parameters.ENABLE_REDUCTION, parameters, True
    )

    if return_flow_trans_map:
        mark_branch("branch_3_return_flow_trans_map_true")
        enable_reduction = False
    else:
        mark_branch("branch_4_return_flow_trans_map_false")

    net = PetriNet("")
    source_place = PetriNet.Place("source")
    net.places.add(source_place)
    sink_place = PetriNet.Place("sink")
    net.places.add(sink_place)
    im = Marking()
    fm = Marking()
    im[source_place] = 1
    fm[sink_place] = 1

    # keep this correspondence for adding invisible transitions for OR-gateways
    inclusive_gateway_exit = set()
    inclusive_gateway_entry = set()

    flow_place = {}
    source_count = {}
    target_count = {}
    for flow in bpmn_graph.get_flows():
        mark_branch("branch_5_loop_flows")
        if isinstance(flow, BPMN.SequenceFlow):
            mark_branch("branch_6_is_sequence_flow")
            source = flow.get_source()
            target = flow.get_target()
            place = PetriNet.Place(str(flow.get_id()))
            net.places.add(place)
            flow_place[flow] = place
            if source not in source_count:
                mark_branch("branch_7_source_not_in_count")
                source_count[source] = 0
            if target not in target_count:
                mark_branch("branch_8_target_not_in_count")
                target_count[target] = 0
            source_count[source] = source_count[source] + 1
            target_count[target] = target_count[target] + 1

    for flow in bpmn_graph.get_flows():
        mark_branch("branch_9_loop_flows_2")
        if isinstance(flow, BPMN.SequenceFlow):
            mark_branch("branch_10_is_sequence_flow_2")
            source = flow.get_source()
            target = flow.get_target()
            place = PetriNet.Place(str(flow.get_id()))
            if (
                isinstance(source, BPMN.InclusiveGateway)
                and source_count[source] > 1
            ):
                mark_branch("branch_11_inclusive_gateway_exit")
                inclusive_gateway_exit.add(place.name)
            elif (
                isinstance(target, BPMN.InclusiveGateway)
                and target_count[target] > 1
            ):
                mark_branch("branch_12_inclusive_gateway_entry")
                inclusive_gateway_entry.add(place.name)
            else:
                mark_branch("branch_13_no_inclusive_gateway")

    # remove possible places that are both in inclusive_gateway_exit and inclusive_gateway_entry,
    # because we do not need to add invisibles in this situation
    incl_gat_set_inters = inclusive_gateway_entry.intersection(
        inclusive_gateway_exit
    )
    inclusive_gateway_exit = inclusive_gateway_exit.difference(
        incl_gat_set_inters
    )
    inclusive_gateway_entry = inclusive_gateway_entry.difference(
        incl_gat_set_inters
    )

    nodes_entering = {}
    nodes_exiting = {}
    trans_map = {}

    for node in bpmn_graph.get_nodes():
        mark_branch("branch_14_loop_nodes")
        if (
            isinstance(node, BPMN.Task)
            or isinstance(node, BPMN.StartEvent)
            or isinstance(node, BPMN.EndEvent)
            or isinstance(node, BPMN.ExclusiveGateway)
            or isinstance(node, BPMN.ParallelGateway)
            or isinstance(node, BPMN.InclusiveGateway)
        ):
            mark_branch("branch_15_supported_node_type")
            if node not in source_count:
                mark_branch("branch_16_node_not_in_source_count")
                source_count[node] = 0
            if node not in target_count:
                mark_branch("branch_17_node_not_in_target_count")
                target_count[node] = 0

            entry_place = PetriNet.Place("ent_" + str(node.get_id()))
            net.places.add(entry_place)
            exiting_place = PetriNet.Place("exi_" + str(node.get_id()))
            net.places.add(exiting_place)
            if use_id:
                mark_branch("branch_18_use_id_true")
                label = str(node.get_id())
            else:
                mark_branch("branch_19_use_id_false")
                label = (
                    str(node.get_name())
                    if isinstance(node, BPMN.Task)
                    else None
                )
                if not label:
                    mark_branch("branch_20_label_is_none")
                    label = None
            transition = PetriNet.Transition(
                name=str(node.get_id()), label=label
            )
            net.transitions.add(transition)
            trans_map[node] = [transition]
            add_arc_from_to(entry_place, transition, net)
            add_arc_from_to(transition, exiting_place, net)

            if isinstance(node, BPMN.ParallelGateway) or isinstance(
                node, BPMN.InclusiveGateway
            ):
                mark_branch("branch_21_is_parallel_or_inclusive_gateway")
                if source_count[node] > 1:
                    mark_branch("branch_22_gateway_source_count_gt_1")
                    exiting_object = PetriNet.Transition(
                        str(uuid.uuid4()), None
                    )
                    net.transitions.add(exiting_object)
                    add_arc_from_to(exiting_place, exiting_object, net)
                    trans_map[node].append(exiting_object)
                else:
                    mark_branch("branch_23_gateway_source_count_le_1")
                    exiting_object = exiting_place

                if target_count[node] > 1:
                    mark_branch("branch_24_gateway_target_count_gt_1")
                    entering_object = PetriNet.Transition(
                        str(uuid.uuid4()), None
                    )
                    net.transitions.add(entering_object)
                    add_arc_from_to(entering_object, entry_place, net)
                    trans_map[node].append(entering_object)
                else:
                    mark_branch("branch_25_gateway_target_count_le_1")
                    entering_object = entry_place
                nodes_entering[node] = entering_object
                nodes_exiting[node] = exiting_object
            else:
                mark_branch("branch_26_not_gateway")
                nodes_entering[node] = entry_place
                nodes_exiting[node] = exiting_place

            if isinstance(node, BPMN.StartEvent):
                mark_branch("branch_27_is_start_event")
                start_transition = PetriNet.Transition(str(uuid.uuid4()), None)
                net.transitions.add(start_transition)
                add_arc_from_to(source_place, start_transition, net)
                add_arc_from_to(start_transition, entry_place, net)
                trans_map[node].append(start_transition)
            elif isinstance(node, BPMN.EndEvent):
                mark_branch("branch_28_is_end_event")
                end_transition = PetriNet.Transition(str(uuid.uuid4()), None)
                net.transitions.add(end_transition)
                add_arc_from_to(exiting_place, end_transition, net)
                add_arc_from_to(end_transition, sink_place, net)
                trans_map[node].append(end_transition)

    for flow in bpmn_graph.get_flows():
        mark_branch("branch_29_loop_flows_3")
        if isinstance(flow, BPMN.SequenceFlow):
            mark_branch("branch_30_is_sequence_flow_3")
            if (
                flow.get_source() in nodes_exiting
                and flow.get_target() in nodes_entering
            ):
                mark_branch("branch_31_flow_source_target_valid")
                source_object = nodes_exiting[flow.get_source()]
                target_object = nodes_entering[flow.get_target()]

                if isinstance(source_object, PetriNet.Place):
                    mark_branch("branch_32_source_is_place")
                    inv1 = PetriNet.Transition(f"sfl_{flow.get_id()}", None)
                    net.transitions.add(inv1)
                    add_arc_from_to(source_object, inv1, net)
                    source_object = inv1
                    trans_map[flow.source].append(inv1)

                if isinstance(target_object, PetriNet.Place):
                    mark_branch("branch_33_target_is_place")
                    inv2 = PetriNet.Transition(f"tfl_{flow.get_id()}", None)
                    net.transitions.add(inv2)
                    add_arc_from_to(inv2, target_object, net)
                    target_object = inv2
                    trans_map[flow.target].append(inv2)

                add_arc_from_to(source_object, flow_place[flow], net)
                add_arc_from_to(flow_place[flow], target_object, net)

    if inclusive_gateway_exit and inclusive_gateway_entry:
        mark_branch("branch_34_inclusive_gateway_optimization")
        # do the following steps if there are inclusive gateways:
        # - calculate the shortest paths
        # - add an invisible transition between couples of corresponding places
        # this ensures soundness and the correct translation of the BPMN
        inv_places = {x.name: x for x in net.places}
        digraph = build_digraph_from_petri_net(net)
        all_shortest_paths = dict(nx_utils.all_pairs_dijkstra(digraph))
        keys = list(all_shortest_paths.keys())

        for pl1 in inclusive_gateway_exit:
            mark_branch("branch_35_loop_inclusive_exit")
            if pl1 in keys:
                mark_branch("branch_36_pl1_in_keys")
                output_places = sorted(
                    [
                        (x, len(y))
                        for x, y in all_shortest_paths[pl1][1].items()
                        if x in inclusive_gateway_entry
                    ],
                    key=lambda x: x[1],
                )
                if output_places:
                    mark_branch("branch_37_output_places_exist")
                    inv_trans = PetriNet.Transition(str(uuid.uuid4()), None)
                    net.transitions.add(inv_trans)
                    add_arc_from_to(inv_places[pl1], inv_trans, net)
                    add_arc_from_to(
                        inv_trans, inv_places[output_places[0][0]], net
                    )

    if enable_reduction:
        mark_branch("branch_38_enable_reduction_true")
        reduction.apply_simple_reduction(net)

    for place in list(net.places):
        mark_branch("branch_39_loop_cleanup_places")
        if (
            len(place.in_arcs) == 0
            and len(place.out_arcs) == 0
            and place not in im
            and place not in fm
        ):
            mark_branch("branch_40_remove_unconnected_place")
            remove_place(net, place)

    if return_flow_trans_map:
        mark_branch("branch_41_return_flow_trans_map")
        return net, im, fm, flow_place, trans_map

    mark_branch("branch_42_return_standard")
    return net, im, fm
