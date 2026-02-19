import unittest

from pandas import Series

from pm4py.util import exec_utils, pandas_utils
from enum import Enum
from pm4py.objects.ocel import constants
from pm4py.objects.ocel.util import ocel_consistency as induct_consistency, ocel_consistency
from assignment_utilities import manual_coverage_helper

class Parameters(Enum):
    EVENT_ID = constants.PARAM_EVENT_ID
    EVENT_ACTIVITY = constants.PARAM_EVENT_ACTIVITY
    EVENT_TIMESTAMP = constants.PARAM_EVENT_TIMESTAMP
    OBJECT_ID = constants.PARAM_OBJECT_ID
    OBJECT_TYPE = constants.PARAM_OBJECT_TYPE
    QUALIFIER = constants.PARAM_QUALIFIER
    CHANGED_FIELD = constants.PARAM_CHNGD_FIELD


class OCEL(object):
    def __init__(
        self,
        events=None,
        objects=None,
        relations=None,
        globals=None,
        parameters=None,
        o2o=None,
        e3e=None,
        object_changes=None,
    ):
        if parameters is None:
            parameters = {}

        self.event_id_column = exec_utils.get_param_value(
            Parameters.EVENT_ID, parameters, constants.DEFAULT_EVENT_ID
        )
        self.object_id_column = exec_utils.get_param_value(
            Parameters.OBJECT_ID, parameters, constants.DEFAULT_OBJECT_ID
        )
        self.object_type_column = exec_utils.get_param_value(
            Parameters.OBJECT_TYPE, parameters, constants.DEFAULT_OBJECT_TYPE
        )

        self.event_activity = exec_utils.get_param_value(
            Parameters.EVENT_ACTIVITY,
            parameters,
            constants.DEFAULT_EVENT_ACTIVITY,
        )
        self.event_timestamp = exec_utils.get_param_value(
            Parameters.EVENT_TIMESTAMP,
            parameters,
            constants.DEFAULT_EVENT_TIMESTAMP,
        )
        self.qualifier = exec_utils.get_param_value(
            Parameters.QUALIFIER, parameters, constants.DEFAULT_QUALIFIER
        )
        self.changed_field = exec_utils.get_param_value(
            Parameters.CHANGED_FIELD, parameters, constants.DEFAULT_CHNGD_FIELD
        )

        if events is None:
            events = pandas_utils.instantiate_dataframe(
                {
                    self.event_id_column: [],
                    self.event_activity: [],
                    self.event_timestamp: [],
                }
            )
        if objects is None:
            objects = pandas_utils.instantiate_dataframe(
                {self.object_id_column: [], self.object_type_column: []}
            )
        if relations is None:
            relations = pandas_utils.instantiate_dataframe(
                {
                    self.event_id_column: [],
                    self.event_activity: [],
                    self.event_timestamp: [],
                    self.object_id_column: [],
                    self.object_type_column: [],
                }
            )
        if globals is None:
            globals = {}
        if o2o is None:
            o2o = pandas_utils.instantiate_dataframe(
                {
                    self.object_id_column: [],
                    self.object_id_column + "_2": [],
                    self.qualifier: [],
                }
            )
        if e3e is None:
            e3e = pandas_utils.instantiate_dataframe(
                {
                    self.event_id_column: [],
                    self.event_id_column + "_2": [],
                    self.qualifier: [],
                }
            )
        if object_changes is None:
            object_changes = pandas_utils.instantiate_dataframe(
                {
                    self.object_id_column: [],
                    self.object_type_column: [],
                    self.event_timestamp: [],
                    self.changed_field: [],
                }
            )
        if self.qualifier not in relations:
            relations[self.qualifier] = [None] * len(relations)

        self.events = events
        self.objects = objects
        self.relations = relations
        self.globals = globals
        self.o2o = o2o
        self.e3e = e3e
        self.object_changes = object_changes

        self.parameters = parameters

class AlignmentTest(unittest.TestCase):
    def test_apply(self):
        self.fields = {
        }
        self.dummy_ocel = OCEL()
        self.dummy_ocel.events[self.dummy_ocel.event_id_column] = [1,2,3]


        induct_consistency.apply(self.dummy_ocel, None)

if __name__ == "__main__":
    unittest.main()

