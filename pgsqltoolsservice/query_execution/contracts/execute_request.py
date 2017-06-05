# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from pgsqltoolsservice.hosting import IncomingMessageConfiguration
import pgsqltoolsservice.query_execution.contracts.common as common
import pgsqltoolsservice.utils as utils


class ExecuteRequestParamsBase:
    def __init__(self):
        self.owner_uri: str = None
        self.execution_plan_options = None      # TODO: Define/wire up ExecutionPlanOptions class


class ExecuteStringParams(ExecuteRequestParamsBase):
    @classmethod
    def from_dict(cls, dictionary: dict):
        return utils.deserialize_from_dict(cls, dictionary)

    def __init__(self):
        super().__init__()
        self.query: str = None

EXECUTE_STRING_REQUEST = IncomingMessageConfiguration(
    'query/executeString',
    ExecuteStringParams
)


class ExecuteDocumentSelectionParams(ExecuteRequestParamsBase):
    @classmethod
    def from_dict(cls, dictionary: dict):
        return utils.deserialize_from_dict(cls, dictionary,
                                           query_selection=common.QuerySelection)

    def __init__(self):
        super().__init__()
        self.query_selection: common.QuerySelection = None

EXECUTE_DOCUMENT_SELECTION_REQUEST = IncomingMessageConfiguration(
    'query/executeSelection',
    ExecuteDocumentSelectionParams
)


class ExecuteResult:
    """
    Parameters for the query execute result. Reserved for future use
    """
    def __init__(self):
        pass
