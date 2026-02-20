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
import json
from enum import Enum
from typing import Optional, Dict, Any

import pandas as pd

from pm4py.objects.ocel import constants
from pm4py.objects.ocel.obj import OCEL
from pm4py.objects.ocel.util import filtering_utils
from pm4py.objects.ocel.util import ocel_consistency
from pm4py.util import (
    exec_utils,
    dt_parsing,
    constants as pm4_constants,
    pandas_utils,
)
from pm4py.objects.log.util import dataframe_utils
from assignment_utilities.rayon_branch_cov import cov_hit



class Parameters(Enum):
    EVENT_ID = constants.PARAM_EVENT_ID
    EVENT_ACTIVITY = constants.PARAM_EVENT_ACTIVITY
    EVENT_TIMESTAMP = constants.PARAM_EVENT_TIMESTAMP
    OBJECT_ID = constants.PARAM_OBJECT_ID
    OBJECT_TYPE = constants.PARAM_OBJECT_TYPE
    INTERNAL_INDEX = constants.PARAM_INTERNAL_INDEX
    ENCODING = "encoding"

def _parse_objects(json_obj, object_id, object_type):
    objects = []
    o2o = []
    types_dict = {}

    for obj_id in json_obj[constants.OCEL_OBJECTS_KEY]:
        cov_hit(FN, 0)
        obj = json_obj[constants.OCEL_OBJECTS_KEY][obj_id]
        obj_type = obj[object_type]

        types_dict[obj_id] = obj_type
        dct = {object_id: obj_id, object_type: obj_type}

        # OVMap
        for k, v in obj[constants.OCEL_OVMAP_KEY].items():
            cov_hit(FN, 1)
            dct[k] = v

        # O2O
        if constants.OCEL_O2O_KEY in obj:
            for rel in obj[constants.OCEL_O2O_KEY]:
                o2o.append(
                    {
                        object_id: obj_id,
                        object_id + "_2": rel[object_id],
                        constants.DEFAULT_QUALIFIER: rel[constants.DEFAULT_QUALIFIER],
                    }
                )

        objects.append(dct)

    return objects, types_dict, o2o

def _parse_events(json_obj, types_dict, event_id, event_activity,
                  event_timestamp, object_id, object_type, parser):

    events = []
    relations = []

    for ev_id in json_obj[constants.OCEL_EVENTS_KEY]:
        cov_hit(FN, 5)
        ev = json_obj[constants.OCEL_EVENTS_KEY][ev_id]

        dct = {
            event_id: ev_id,
            event_timestamp: parser.apply(ev[event_timestamp]),
            event_activity: ev[event_activity],
        }

        # VMAP
        for k, v in ev[constants.OCEL_VMAP_KEY].items():
            cov_hit(FN, 6)
            dct[k] = v

        this_rel = {}

        # OMAP
        for obj in ev[constants.OCEL_OMAP_KEY]:
            cov_hit(FN, 7)
            if obj in types_dict:
                cov_hit(FN, 8)
                this_rel[obj] = {
                    event_id: ev_id,
                    event_activity: ev[event_activity],
                    event_timestamp: parser.apply(ev[event_timestamp]),
                    object_id: obj,
                    object_type: types_dict[obj],
                }


        if constants.OCEL_TYPED_OMAP_KEY in ev:
            cov_hit(FN, 10)
            for element in ev[constants.OCEL_TYPED_OMAP_KEY]:
                cov_hit(FN, 12)
                if object_id in element:
                    cov_hit(FN, 13)
                    key1 = element[object_id]
                    if key1 in this_rel:
                        cov_hit(FN, 15)
                        this_rel[key1][constants.DEFAULT_QUALIFIER] = element[
                            constants.DEFAULT_QUALIFIER
                        ]

        relations.extend(this_rel.values())
        events.append(dct)

    return events, relations

def _normalize_dataframes(events, objects, relations,
                          event_id, event_activity,
                          event_timestamp, object_id,
                          object_type, internal_index):

    events = pandas_utils.instantiate_dataframe(events)
    objects = pandas_utils.instantiate_dataframe(objects)
    relations = pandas_utils.instantiate_dataframe(relations)

    if len(relations) == 0:
        cov_hit(FN, 20)
        relations = pandas_utils.instantiate_dataframe(
            {
                event_id: [],
                event_activity: [],
                event_timestamp: [],
                object_id: [],
                object_type: [],
            }
        )
    else: cov_hit(FN, 21)

    events = pandas_utils.insert_index(
        events, internal_index, reset_index=False, copy_dataframe=False
    )

    if len(relations) > 0:
        cov_hit(FN, 22)
        relations = pandas_utils.insert_index(
            relations, internal_index, reset_index=False, copy_dataframe=False
        )
    cov_hit(FN, 23)

    events = events.sort_values([event_timestamp, internal_index])

    if len(relations) > 0:
        cov_hit(FN, 24)
        relations = relations.sort_values([event_timestamp, internal_index])
    else: cov_hit(FN, 25)

    del events[internal_index]

    if internal_index in relations.columns:
        cov_hit(FN, 26)
        del relations[internal_index]
    else: cov_hit(FN, 27)

    return events, objects, relations

def _process_object_changes(json_obj, objects,
                            event_timestamp, object_id, object_type):

    if constants.OCEL_OBJCHANGES_KEY not in json_obj:
        return None

    object_changes = pandas_utils.instantiate_dataframe(
        json_obj[constants.OCEL_OBJCHANGES_KEY]
    )

    if len(object_changes) == 0:
        return None

    object_changes = dataframe_utils.convert_timestamp_columns_in_df(
        object_changes,
        timest_format=pm4_constants.DEFAULT_XES_TIMESTAMP_PARSE_FORMAT,
        timest_columns=[event_timestamp],
    )

    obj_id_map = objects[[object_id, object_type]].to_dict("records")
    obj_id_map = {x[object_id]: x[object_type] for x in obj_id_map}

    object_changes[object_type] = object_changes[object_id].map(obj_id_map)

    return object_changes


def get_base_ocel(json_obj: Any, parameters: Optional[Dict[Any, Any]] = None):

    event_id = exec_utils.get_param_value(
        Parameters.EVENT_ID, parameters, constants.DEFAULT_EVENT_ID
    )
    event_activity = exec_utils.get_param_value(
        Parameters.EVENT_ACTIVITY, parameters, constants.DEFAULT_EVENT_ACTIVITY
    )
    event_timestamp = exec_utils.get_param_value(
        Parameters.EVENT_TIMESTAMP, parameters,
        constants.DEFAULT_EVENT_TIMESTAMP,
    )
    object_id = exec_utils.get_param_value(
        Parameters.OBJECT_ID, parameters, constants.DEFAULT_OBJECT_ID
    )
    object_type = exec_utils.get_param_value(
        Parameters.OBJECT_TYPE, parameters, constants.DEFAULT_OBJECT_TYPE
    )
    internal_index = exec_utils.get_param_value(
        Parameters.INTERNAL_INDEX, parameters, constants.DEFAULT_INTERNAL_INDEX
    )

    parser = dt_parsing.parser.get()

    objects_list, types_dict, o2o_list = _parse_objects(
        json_obj, object_id, object_type
    )

    events_list, relations_list = _parse_events(
        json_obj, types_dict,
        event_id, event_activity, event_timestamp,
        object_id, object_type, parser
    )

    events, objects, relations = _normalize_dataframes(
        events_list, objects_list, relations_list,
        event_id, event_activity, event_timestamp,
        object_id, object_type, internal_index
    )

    o2o = pandas_utils.instantiate_dataframe(o2o_list) if o2o_list else None

    object_changes = _process_object_changes(
        json_obj, objects, event_timestamp, object_id, object_type
    )

    globals_dict = {
        constants.OCEL_GLOBAL_LOG: json_obj[constants.OCEL_GLOBAL_LOG],
        constants.OCEL_GLOBAL_EVENT: json_obj[constants.OCEL_GLOBAL_EVENT],
        constants.OCEL_GLOBAL_OBJECT: json_obj[constants.OCEL_GLOBAL_OBJECT],
    }

    return OCEL(
        events=events,
        objects=objects,
        relations=relations,
        o2o=o2o,
        object_changes=object_changes,
        globals=globals_dict,
        parameters=parameters,
    )

def apply(file_path: str, parameters: Optional[Dict[Any, Any]] = None) -> OCEL:
    """
    Imports an object-centric event log from a JSON-OCEL file, using the default JSON backend of Python

    Parameters
    -----------------
    file_path
        Path to the JSON-OCEL file
    parameters
        Parameters of the algorithm, including:
        - Parameters.EVENT_ID
        - Parameters.EVENT_ACTIVITY
        - Parameters.EVENT_TIMESTAMP
        - Parameters.OBJECT_ID
        - Parameters.OBJECT_TYPE
        - Parameters.INTERNAL_INDEX

    Returns
    ------------------
    ocel
        Object-centric event log
    """
    if parameters is None:
        parameters = {}

    encoding = exec_utils.get_param_value(
        Parameters.ENCODING, parameters, pm4_constants.DEFAULT_ENCODING
    )

    F = open(file_path, "r", encoding=encoding)
    json_obj = json.load(F)
    F.close()

    log = get_base_ocel(json_obj, parameters=parameters)

    log = ocel_consistency.apply(log, parameters=parameters)
    log = filtering_utils.propagate_relations_filtering(
        log, parameters=parameters
    )

    return log
