from pm4py.objects.ocel.importer.jsonocel.variants.classic import get_base_ocel
from pm4py.objects.ocel.constants import (
    OCEL_OBJECTS_KEY,
    OCEL_EVENTS_KEY,
    OCEL_OVMAP_KEY,
    OCEL_VMAP_KEY,
    OCEL_OMAP_KEY,
    OCEL_OBJCHANGES_KEY,
    OCEL_O2O_KEY,
    OCEL_GLOBAL_LOG,
    OCEL_GLOBAL_EVENT,
    OCEL_GLOBAL_OBJECT,
)
from pm4py.objects.ocel import constants

import unittest



class TestGetBaseOcel(unittest.TestCase):

    def build_globals(self):
        return {
            OCEL_GLOBAL_LOG: {},
            OCEL_GLOBAL_EVENT: {},
            OCEL_GLOBAL_OBJECT: {},
            OCEL_OBJECTS_KEY: {},
            OCEL_EVENTS_KEY: {},
        }


    def test_empty_relations(self):
        json_obj = self.build_globals()

        json_obj[OCEL_OBJECTS_KEY] = {
            "o1": {
                constants.DEFAULT_OBJECT_TYPE: "typeA",
                OCEL_OVMAP_KEY: {},
            }
        }

        json_obj[OCEL_EVENTS_KEY] = {
            "e1": {
                constants.DEFAULT_EVENT_ACTIVITY: "act",
                constants.DEFAULT_EVENT_TIMESTAMP: "2020-01-01T00:00:00",
                OCEL_VMAP_KEY: {},
                OCEL_OMAP_KEY: [],
            }
        }

        log = get_base_ocel(json_obj)

        self.assertEqual(len(log.events), 1)
        self.assertEqual(len(log.relations), 0)


    def test_missing_object_reference(self):
        json_obj = self.build_globals()

        json_obj[OCEL_OBJECTS_KEY] = {
            "o1": {
                constants.DEFAULT_OBJECT_TYPE: "typeA",
                OCEL_OVMAP_KEY: {},
            }
        }

        json_obj[OCEL_EVENTS_KEY] = {
            "e1": {
                constants.DEFAULT_EVENT_ACTIVITY: "act",
                constants.DEFAULT_EVENT_TIMESTAMP: "2020-01-01T00:00:00",
                OCEL_VMAP_KEY: {},
                OCEL_OMAP_KEY: ["o2"], 
            }
        }

        log = get_base_ocel(json_obj)

        self.assertEqual(len(log.events), 1)

        self.assertEqual(len(log.relations), 0)

    def test_single_valid_relation(self):
        json_obj = self.build_globals()

        json_obj[OCEL_OBJECTS_KEY] = {
            "o1": {
                constants.DEFAULT_OBJECT_TYPE: "typeA",
                OCEL_OVMAP_KEY: {},
            }
        }

        json_obj[OCEL_EVENTS_KEY] = {
            "e1": {
                constants.DEFAULT_EVENT_ACTIVITY: "act",
                constants.DEFAULT_EVENT_TIMESTAMP: "2020-01-01T00:00:00",
                OCEL_VMAP_KEY: {},
                OCEL_OMAP_KEY: ["o1"],
            }
        }

        log = get_base_ocel(json_obj)

        self.assertEqual(len(log.relations), 1)

    def test_object_changes_present(self):
        json_obj = self.build_globals()

        json_obj[OCEL_OBJECTS_KEY] = {
            "o1": {
                constants.DEFAULT_OBJECT_TYPE: "typeA",
                OCEL_OVMAP_KEY: {},
            }
        }

        json_obj[OCEL_EVENTS_KEY] = {}

        json_obj[OCEL_OBJCHANGES_KEY] = [
            {
                constants.DEFAULT_OBJECT_ID: "o1",
                constants.DEFAULT_EVENT_TIMESTAMP: "2020-01-01T00:00:00",
            }
        ]

        log = get_base_ocel(json_obj)

        self.assertIsNotNone(log.object_changes)
        self.assertEqual(len(log.object_changes), 1)
