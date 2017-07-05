# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

# ScanKeyword function for PostgreSQL 9.5rc1

import enum
from typing import List

from pgsqltoolsservice.language.contracts import CompletionItem, CompletionItemKind, TextEdit
from pgsqltoolsservice.workspace.contracts.common import Range


class KeywordType(enum.Enum):
    """Type of keyword in Postgres"""
    UNRESERVED_KEYWORD = 0
    COL_NAME_KEYWORD = 1
    TYPE_FUNC_NAME_KEYWORD = 2
    RESERVED_KEYWORD = 3


class DefaultCompletionHelper():
    """
    Manages the default completion list
    """
    KEYWORDS = {
        "abort": 0, "absolute": 0, "access": 0, "action": 0, "add": 0, "admin": 0, "after": 0, "aggregate": 0, "all": 3,
        "also": 0, "alter": 0, "always": 0, "analyze": 3, "and": 3, "any": 3, "array": 3, "as": 3, "asc": 3,
        "assertion": 0, "assignment": 0, "asymmetric": 3, "at": 0, "attribute": 0, "authorization": 2, "backward": 0,
        "before": 0, "begin": 0, "between": 1, "bigint": 1, "binary": 2, "bit": 1, "boolean": 1, "both": 3, "by": 0,
        "cache": 0, "called": 0, "cascade": 0, "cascaded": 0, "case": 3, "cast": 3, "catalog": 0, "chain": 0, "char": 1,
        "character": 1, "characteristics": 0, "check": 3, "checkpoint": 0, "class": 0, "close": 0, "cluster": 0,
        "coalesce": 1, "collate": 3, "collation": 2, "column": 3, "comment": 0, "comments": 0, "commit": 0,
        "committed": 0, "concurrently": 2, "configuration": 0, "conflict": 0, "connection": 0, "constraint": 3,
        "constraints": 0, "content": 0, "continue": 0, "conversion": 0, "copy": 0, "cost": 0, "create": 3, "cross": 2,
        "csv": 0, "cube": 0, "current": 0, "current_catalog": 3, "current_date": 3, "current_role": 3,
        "current_schema": 2, "current_time": 3, "current_timestamp": 3, "current_user": 3, "cursor": 0, "cycle": 0,
        "data": 0, "database": 0, "day": 0, "deallocate": 0, "dec": 1, "decimal": 1, "declare": 0, "default": 3,
        "defaults": 0, "deferrable": 3, "deferred": 0, "definer": 0, "delete": 0, "delimiter": 0, "delimiters": 0,
        "desc": 3, "dictionary": 0, "disable": 0, "discard": 0, "distinct": 3, "do": 3, "document": 0, "domain": 0,
        "double": 0, "drop": 0, "each": 0, "else": 3, "enable": 0, "encoding": 0, "encrypted": 0, "end": 3, "enum": 0,
        "escape": 0, "event": 0, "except": 3, "exclude": 0, "excluding": 0, "exclusive": 0, "execute": 0, "exists": 1,
        "explain": 0, "extension": 0, "external": 0, "extract": 1, "false": 3, "family": 0, "fetch": 3, "filter": 0,
        "first": 0, "float": 1, "following": 0, "for": 3, "force": 0, "foreign": 3, "forward": 0, "freeze": 2,
        "from": 3, "full": 2, "function": 0, "functions": 0, "global": 0, "grant": 3, "granted": 0, "greatest": 1,
        "group": 3, "grouping": 1, "handler": 0, "having": 3, "header": 0, "hold": 0, "hour": 0, "identity": 0, "if": 0,
        "ilike": 2, "immediate": 0, "immutable": 0, "implicit": 0, "import": 0, "in": 3, "including": 0, "increment": 0,
        "index": 0, "indexes": 0, "inherit": 0, "inherits": 0, "initially": 3, "inline": 0, "inner": 2, "inout": 1,
        "input": 0, "insensitive": 0, "insert": 0, "instead": 0, "int": 1, "integer": 1, "intersect": 3, "interval": 1,
        "into": 3, "invoker": 0, "is": 2, "isnull": 2, "isolation": 0, "join": 2, "key": 0, "label": 0, "language": 0,
        "large": 0, "last": 0, "lateral": 3, "leading": 3, "leakproof": 0, "least": 1, "left": 2, "level": 0, "like": 2,
        "limit": 3, "listen": 0, "load": 0, "local": 0, "localtime": 3, "localtimestamp": 3, "location": 0, "lock": 0,
        "locked": 0, "logged": 0, "mapping": 0, "match": 0, "materialized": 0, "maxvalue": 0, "minute": 0,
        "minvalue": 0, "mode": 0, "month": 0, "move": 0, "name": 0, "names": 0, "national": 1, "natural": 2, "nchar": 1,
        "next": 0, "no": 0, "none": 1, "not": 3, "nothing": 0, "notify": 0, "notnull": 2, "nowait": 0, "null": 3,
        "nullif": 1, "nulls": 0, "numeric": 1, "object": 0, "of": 0, "off": 0, "offset": 3, "oids": 0, "on": 3,
        "only": 3, "operator": 0, "option": 0, "options": 0, "or": 3, "order": 3, "ordinality": 0, "out": 1, "outer": 2,
        "over": 0, "overlaps": 2, "overlay": 1, "owned": 0, "owner": 0, "parser": 0, "partial": 0, "partition": 0,
        "passing": 0, "password": 0, "placing": 3, "plans": 0, "policy": 0, "position": 1, "preceding": 0,
        "precision": 1, "prepare": 0, "prepared": 0, "preserve": 0, "primary": 3, "prior": 0, "privileges": 0,
        "procedural": 0, "procedure": 0, "program": 0, "quote": 0, "range": 0, "read": 0, "real": 1, "reassign": 0,
        "recheck": 0, "recursive": 0, "ref": 0, "references": 3, "refresh": 0, "reindex": 0, "relative": 0,
        "release": 0, "rename": 0, "repeatable": 0, "replace": 0, "replica": 0, "reset": 0, "restart": 0, "restrict": 0,
        "returning": 3, "returns": 0, "revoke": 0, "right": 2, "role": 0, "rollback": 0, "rollup": 0, "row": 1,
        "rows": 0, "rule": 0, "savepoint": 0, "schema": 0, "scroll": 0, "search": 0, "second": 0, "security": 0,
        "select": 3, "sequence": 0, "sequences": 0, "serializable": 0, "server": 0, "session": 0, "session_user": 3,
        "set": 0, "setof": 1, "sets": 0, "share": 0, "show": 0, "similar": 2, "simple": 0, "skip": 0, "smallint": 1,
        "snapshot": 0, "some": 3, "sql": 0, "stable": 0, "standalone": 0, "start": 0, "statement": 0, "statistics": 0,
        "stdin": 0, "stdout": 0, "storage": 0, "strict": 0, "strip": 0, "substring": 1, "symmetric": 3, "sysid": 0,
        "system": 0, "table": 3, "tables": 0, "tablesample": 2, "tablespace": 0, "temp": 0, "template": 0,
        "temporary": 0, "text": 0, "then": 3, "time": 1, "timestamp": 1, "to": 3, "trailing": 3, "transaction": 0,
        "transform": 0, "treat": 1, "trigger": 0, "trim": 1, "true": 3, "truncate": 0, "trusted": 0, "type": 0,
        "types": 0, "unbounded": 0, "uncommitted": 0, "unencrypted": 0, "union": 3, "unique": 3, "unknown": 0,
        "unlisten": 0, "unlogged": 0, "until": 0, "update": 0, "user": 3, "using": 3, "vacuum": 0, "valid": 0,
        "validate": 0, "validator": 0, "value": 0, "values": 1, "varchar": 1, "variadic": 3, "varying": 0, "verbose": 2,
        "version": 0, "view": 0, "views": 0, "volatile": 0, "when": 3, "where": 3, "whitespace": 0, "window": 3,
        "with": 3, "within": 0, "without": 0, "work": 0, "wrapper": 0, "write": 0, "xml": 0, "xmlattributes": 1,
        "xmlconcat": 1, "xmlelement": 1, "xmlexists": 1, "xmlforest": 1, "xmlparse": 1, "xmlpi": 1, "xmlroot": 1,
        "xmlserialize": 1, "year": 0, "yes": 0, "zone": 0
    }

    def is_keyword(self, key: str) -> bool:
        """Looks up a string to verify if it is / is not a keyword"""
        return (key in DefaultCompletionHelper.KEYWORDS) or False

    def get_matches(self, start: str, text_range: Range, lowercase: bool) -> List[CompletionItem]:
        """
        Gets matching keywords as a list of CompletionItem.
        """
        matches: List[CompletionItem] = []
        if not start:
            return matches

        start = start.lower()
        for key in DefaultCompletionHelper.KEYWORDS.keys():
            if key.startswith(start):
                matches.append(DefaultCompletionHelper._to_completion_item(key, text_range, lowercase))
        return matches

    @property
    def count_keywords(self) -> int:
        return len(DefaultCompletionHelper.KEYWORDS.keys())

    @classmethod
    def _to_completion_item(cls, key: str, text_range: Range, lowercase: bool) -> CompletionItem:
        key = key.lower() if lowercase else key.upper()
        completion = CompletionItem()
        completion.label = key
        completion.detail = key + ' keyword'
        completion.insert_text = key
        completion.kind = CompletionItemKind.Keyword
        completion.text_edit = TextEdit.from_data(text_range, key)
        return completion