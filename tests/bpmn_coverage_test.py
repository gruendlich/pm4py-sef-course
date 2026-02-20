import unittest
from pm4py.objects.bpmn.obj import BPMN
from pm4py.objects.conversion.bpmn.variants import to_petri_net

class BPMNCoverageTest(unittest.TestCase):
    def setUp(self):
        # Create a simple valid BPMN graph for testing
        self.bpmn = BPMN()
        start = BPMN.StartEvent(name="start", isInterrupting=True)
        task = BPMN.Task(name="task")
        end = BPMN.EndEvent(name="end")
        self.bpmn.add_node(start)
        self.bpmn.add_node(task)
        self.bpmn.add_node(end)
        self.bpmn.add_flow(BPMN.SequenceFlow(start, task))
        self.bpmn.add_flow(BPMN.SequenceFlow(task, end))

    def test_apply_with_use_id(self):
        # Target branch_18: USE_ID = True
        to_petri_net.apply(self.bpmn, parameters={to_petri_net.Parameters.USE_ID: True})

    def test_apply_return_flow_trans_map(self):
        # Target branch_41: RETURN_FLOW_TRANS_MAP = True
        # Target branch_3: ... and enable_reduction = False (implied)
        res = to_petri_net.apply(self.bpmn, parameters={to_petri_net.Parameters.RETURN_FLOW_TRANS_MAP: True})
        self.assertTrue(len(res) == 5)  # net, im, fm, flow_place, trans_map

    def test_apply_parameters_none(self):
        # Target branch_1: parameters is None
        to_petri_net.apply(self.bpmn, parameters=None)


if __name__ == "__main__":
    unittest.main()
