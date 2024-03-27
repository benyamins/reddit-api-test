# Testing out Rust with the Reddit API


## Example

``` bash
rr list saved --last 2 --filter soccer

# |----|-----------|--------|--------------------|
# | id | subreddit | title  | url                |
# |----|-----------|--------|--------------------|
# | 1  | Soccer    | Goal!  | https:\\reddit.... |
# |----|-----------|--------|--------------------|
# | 2  | News      | BadNws | https:\\reddit.... |
# |----|-----------|--------|--------------------|

rr list subreddits [saved,hidden]
```

## Help

``` bash
rr add <user_name> --fetch [saved, hidden]  # add a user (with requiered stuff)
rr remove <user_name>  # remove the contents
rr use <user_name>
rr fetch <saved, hidden> [user_name]
rr list saved [--last <number>, --filter <subreddit>]
rr list hidden [--last <number>, --filter <subreddit>]
rr list subreddits [saved, hidden]
```
