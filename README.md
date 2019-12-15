# Plan

response <- request.get()

`response.status_code` == 400 or 200

200 success else fails


## steps
1. Authenticate
OAuth2
2. Requests
#JSON response object:
{
    id: String
    name: String
    kind: String -> "eg. listing"
    data: Object
}

Listing (not a thing subclass)
query arguments -> args: befor, after, count # for previous & next page

{
    kind: Listing
    children: List<thing>
}
- 60 req per min.
- 

{kind, data} -> data: {.., children, after, before}
children: List[Object] -> Object: {data: Object, kind: 't3'}
data: {url, title, subreddit, permalink}

request.get('/user/madeto_be/saved',
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

