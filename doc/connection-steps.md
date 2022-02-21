## steps
1. Authenticate.
2. OAuth2 Get Token.
3. Request Elements.

#JSON response object:
```
{
    id: String
    name: String
    kind: String -> "eg. listing"
    data: Object
}
```

Listing (not a thing subclass)
```
{
    kind: Listing
    children: List<thing>
}
```
- 60 req per min.
```
{kind, data} -> data: {.., children, after, before}
children: List[Object] -> Object: {data: Object, kind: 't3'}
data: {url, title, subreddit, permalink}
```

```
params = {
    context
    show: all
    sort
    t
    type
    username
    after
    before
    count
    include_categories
    limit
    sr_detail
}
```
