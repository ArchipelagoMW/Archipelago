"""
Module that provides functions to create AST calls representing various game objects.
"""

import typing
import ast

from ..types.condition import Condition
from ..types.locations import AccessInfo, LocationData
from ..types.regions import RegionConnection
from ..types.items import ItemData, ItemPoolEntry, ProgressiveChainEntry, SingleItemData
from ..types.shops import ShopData


def create_expression_condition(condition: Condition) -> ast.Call:
    """
    Create an expression representing a singular condition.
    """
    result = ast.Call(
        func=ast.Name(condition.__class__.__name__),
        args=[],
        keywords=[ast.keyword(arg=key, value=ast.Constant(value)) for key, value in condition.__dict__.items()],
    )
    ast.fix_missing_locations(result)

    return result

def create_expression_condition_list(conditions: typing.Optional[list[Condition]]) -> ast.expr:
    """
    Create an expression representing a list of conditions.
    """
    if conditions is None:
        return ast.Constant(None)
    result = ast.List(elts=[])

    for condition in conditions:
        result.elts.append(create_expression_condition(condition))

    ast.fix_missing_locations(result)
    return result

def create_expression_access_info(access: AccessInfo):
    """
    Create an expression representing the access information of a location.
    """
    ast_call = ast.Call(
        func=ast.Name("AccessInfo"),
        args=[],
        keywords=[
            ast.keyword(
                arg="region",
                value=ast.Constant(access.region)
            ),
        ]
    )

    if access.cond is not None and access.cond != []:
        ast_call.keywords.append(ast.keyword("cond", create_expression_condition_list(access.cond)))

    ast.fix_missing_locations(ast_call)

    return ast_call

def create_expression_location(data: LocationData) -> ast.Call:
    """
    Create an expression that represents a location.

    Specifically, this will instantiate a new location. Do not use this more than once per location.
    """
    ast_item = ast.Call(
        func=ast.Name("LocationData"),
        args=[],
        keywords=[
            ast.keyword(
                arg="code",
                value=ast.Constant(data.code)
            ),
            ast.keyword(
                arg="name",
                value=ast.Constant(data.name)
            ),
        ]
    )

    if data.area is not None:
        ast_item.keywords.append(ast.keyword(arg="area", value=ast.Constant(data.area)))

    if data.metadata is not None:
        ast_item.keywords.append(ast.keyword(
            arg="metadata",
            value=ast.Dict(
                keys=[ast.Constant(x) for x in data.metadata.keys()],
                values=[ast.Constant(x) for x in data.metadata.values()],
            )
        ))

    ast_item.keywords.append(ast.keyword("access", create_expression_access_info(data.access)))

    ast.fix_missing_locations(ast_item)
    return ast_item

def create_expression_location_ref(data: LocationData):
    """
    Create an expression that represents a location.

    This will reference the variable locations_data. Please make sure that variable in in the scope of the file.
    """
    ast_item = ast.Subscript(
        value=ast.Name("locations_dict"),
        slice=ast.Constant(data.name),
        ctx=ast.Load()
    )
    ast.fix_missing_locations(ast_item)
    return ast_item

def create_expression_single_item(data: SingleItemData):
    """
    Create an expression representing the raw data for an item type.

    Specifically, this will instantiate a new single item. Do not use this more than once per item.
    """
    ast_item = ast.Call(
        func=ast.Name("SingleItemData"),
        args=[],
        keywords=[
            ast.keyword(
                arg="item_id",
                value=ast.Constant(data.item_id)
            ),
            ast.keyword(
                arg="name",
                value=ast.Constant(data.name)
            ),
        ]
    )

    if data.classification.name is not None:
        ast_item.keywords.append(
            ast.keyword(
                arg="classification",
                value=ast.Attribute(
                    value=ast.Name("ItemClassification"),
                    attr=data.classification.name
                )
            )
        )

    if data.unique:
        ast_item.keywords.append(ast.keyword(
            arg="unique",
            value=ast.Constant(True)
        ))

    ast.fix_missing_locations(ast_item)
    return ast_item

def create_expression_item(data: ItemData):
    """
    Create an expression representing an item with a quantity.

    Specifically, this will instantiate a new item. Do not use this more than once per item.
    """
    ast_item = ast.Call(
        func=ast.Name("ItemData"),
        args=[],
        keywords=[
            ast.keyword(
                arg="item",
                value=ast.Subscript(
                    value=ast.Name("single_items_dict"),
                    slice=ast.Constant(data.item.name),
                    ctx=ast.Load()
                )
            ),
            ast.keyword(
                arg="amount",
                value=ast.Constant(data.amount)
            ),
            ast.keyword(
                arg="combo_id",
                value=ast.Constant(data.combo_id)
            )
        ]
    )
    ast.fix_missing_locations(ast_item)
    return ast_item

def create_expression_item_ref(data: ItemData):
    """
    Create an expression representing an item with a quantity.

    This will reference the variable items_dict. Please make sure that variable in in the scope of the file.
    """
    ast_item = ast.Subscript(
        value=ast.Name("items_dict"),
        slice=ast.Tuple(elts=[
            ast.Constant(data.item.name),
            ast.Constant(data.amount)]
        ),
        ctx=ast.Load()
    )
    ast.fix_missing_locations(ast_item)
    return ast_item

def create_expression_progressive_chain_entry(entry: ProgressiveChainEntry):
    """
    Create an expression representing an entry in a chain of progressive items.
    """
    ast_item = ast.Call(
        func=ast.Name("ProgressiveChainEntry"),
        args=[],
        keywords=[
            ast.keyword(
                arg="item",
                value=create_expression_item_ref(entry.item),
            ),
        ]
    )

    if entry.metadata is not None:
        # this will never be none, but it must claim that it can be to satisfy the typing gods
        keys: list[ast.expr | None] = [ast.Constant(k) for k in entry.metadata.keys()]
        values: list[ast.expr] = [ast.Constant(k) for k in entry.metadata.values()]

        ast_item.keywords.append(ast.keyword(
            arg="metadata",
            value=ast.Dict(
                keys=keys,
                values=values,
            )
        ))

    ast.fix_missing_locations(ast_item)
    return ast_item

def create_expression_item_pool_entry(entry: ItemPoolEntry):
    """
    Create an expression representing an entry in an item pool, with possible conditional inclusion.
    """
    ast_item = ast.Call(
        func=ast.Name("ItemPoolEntry"),
        args=[],
        keywords=[
            ast.keyword(
                arg="item",
                value=create_expression_item_ref(entry.item),
            ),
            ast.keyword(
                arg="quantity",
                value=ast.Constant(entry.quantity)
            ),
        ]
    )

    if entry.metadata is not None:
        keys: list[ast.expr | None] = [ast.Constant(k) for k in entry.metadata.keys()]
        values: list[ast.expr] = [ast.Constant(k) for k in entry.metadata.values()]

        ast_item.keywords.append(ast.keyword(
            arg="metadata",
            value=ast.Dict(
                keys=keys,
                values=values,
            )
        ))

    ast.fix_missing_locations(ast_item)
    return ast_item

def create_expression_region_connection(conn: RegionConnection):
    """
    Create an expression representing a connection between two regions.
    """
    ast_region = ast.Call(
        func=ast.Name("RegionConnection"),
        args=[],
        keywords=[
            ast.keyword(
                arg="region_from",
                value=ast.Constant(conn.region_from)
            ),
            ast.keyword(
                arg="region_to",
                value=ast.Constant(conn.region_to)
            ),
            ast.keyword(
                arg="cond",
                value=create_expression_condition_list(conn.cond)
            ),
        ]
    )

    ast.fix_missing_locations(ast_region)

    return ast_region

def create_expression_shop(data: ShopData) -> ast.Call:
    """
    Create an expression that represents a shop region.

    Specifically, this will instantiate a new ShopData. Do not use this more than once per location.
    """
    ast_item = ast.Call(
        func=ast.Name("ShopData"),
        args=[],
        keywords=[
            ast.keyword(
                arg="internal_name",
                value=ast.Constant(data.internal_name)
            ),
            ast.keyword(
                arg="name",
                value=ast.Constant(data.name)
            ),
        ]
    )

    if data.metadata is not None:
        ast_item.keywords.append(ast.keyword(
            arg="metadata",
            value=ast.Dict(
                keys=[ast.Constant(x) for x in data.metadata.keys()],
                values=[ast.Constant(x) for x in data.metadata.values()],
            )
        ))

    ast_item.keywords.append(ast.keyword("access", create_expression_access_info(data.access)))

    ast.fix_missing_locations(ast_item)
    return ast_item
