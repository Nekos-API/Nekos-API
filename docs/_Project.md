An open-source anime images API.

Crediting Nekos API in your projects is not required, but greatly appreciated.

# Conventions

The API follows a set of conventions across all endpoints.

## Pagination

Pagination is always done using limit and offset query parameters.

- `limit` - An integer from 1 to 100, it's the maximum amount of items that will be returned by the
  API in the response.
- `offset` - An integer greater or equal to 0. It's the amount of items to skip before returning a
  page. For example, `?offset=1` will make the page skip 1 item and return items starting from the
  second one.

Paginated response bodies always only contain the following two keys:

- `items` - An array of the items in the page returned.
- `total` - The amount of items available (not just the amount of items returned).

An example is:

```json
{
    "items": [
        { "id": "IE63W3DJzoyy-vPkPKf_V" },
        { "id": "-VcR7RpvK74SHAd9iKCVU" },
        ...
    ],
    "total": 40664
}
```

## List Filters

When a query parameter may take more than one argument, those are specified by specifying the query
parameter multiple times. For example,

```
?tag=Girl&tag=Boy
```