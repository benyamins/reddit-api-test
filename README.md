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

## Headers

``` python
r.get/post(
    'url'
    params={},
    headers={},
    data={},

try:
    response: requests.Response = requests.get('https://httpbin.org/get')
    # response: requests.Response = requests.get(REDDIT + TRENDING)
    response.raise_for_status()
except HTTPError as err:
    print(f'Http error {err}')
else:
    print('Succesfull Request')
    print(response.text)  # or .json()
```


{
 'all_awardings': [],
 'allow_live_comments': True,
 'approved_at_utc': None,
 'approved_by': None,
 'archived': False,
 'author': 'Ainar-G',
 'author_flair_background_color': None,
 'author_flair_css_class': None,
 'author_flair_richtext': [],
 'author_flair_template_id': None,
 'author_flair_text': None,
 'author_flair_text_color': None,
 'author_flair_type': 'text',
 'author_fullname': 't2_5odlw',
 'author_patreon_flair': False,
 'awarders': [],
 'banned_at_utc': None,
 'banned_by': None,
 'can_gild': True,
 'can_mod_post': False,
 'category': None,
 'clicked': False,
 'content_categories': None,
 'contest_mode': False,
 'created': 1573196358.0,
 'created_utc': 1573167558.0,
 'discussion_type': None,
 'distinguished': None,
 'domain': 'blog.golang.org',
 'downs': 0,
 'edited': False,
 'gilded': 0,
 'gildings': {},
 'hidden': False,
 'hide_score': False,
 'id': 'dt5yvr',
 'is_crosspostable': True,
 'is_meta': False,
 'is_original_content': False,
 'is_reddit_media_domain': False,
 'is_robot_indexable': True,
 'is_self': False,
 'is_video': False,
 'likes': True,
 'link_flair_background_color': '',
 'link_flair_css_class': None,
 'link_flair_richtext': [],
 'link_flair_text': None,
 'link_flair_text_color': 'dark',
 'link_flair_type': 'text',
 'locked': False,
 'media': None,
 'media_embed': {},
 'media_only': False,
 'mod_note': None,
 'mod_reason_by': None,
 'mod_reason_title': None,
 'mod_reports': [],
 'name': 't3_dt5yvr',
 'no_follow': False,
 'num_comments': 60,
 'num_crossposts': 0,
 'num_reports': None,
 'over_18': False,
 'parent_whitelist_status': 'all_ads',
 'permalink': '/r/golang/comments/dt5yvr/go_modules_v2_and_beyond_the_go_blog/',
 'pinned': False,
 'post_hint': 'link',
 'preview': {'enabled': False,
             'images': [{'id': 'E7oKIfMRuMfDDSZCLXVig__RU2za_Xxr7sK14HMILQE',
                         'resolutions': [{'height': 68,
                                          'url': 'https://external-preview.redd.it/zHrVWNaw0APpJIrFxhDL391gij4nO_PKUy
nhVbFCtW0.jpg?width=108&amp;crop=smart&amp;auto=webp&amp;s=4c54c1980eca6a00d9e1d606d7e4ee5d222a72e5',
                                          'width': 108},
                                         {'height': 136,
                                          'url': 'https://external-preview.redd.it/zHrVWNaw0APpJIrFxhDL391gij4nO_PKUy
nhVbFCtW0.jpg?width=216&amp;crop=smart&amp;auto=webp&amp;s=c64fd27d6ac2e1037cfd6269ddbc96582fd714d1',
                                          'width': 216},
                                         {'height': 202,
                                          'url': 'https://external-preview.redd.it/zHrVWNaw0APpJIrFxhDL391gij4nO_PKUy
nhVbFCtW0.jpg?width=320&amp;crop=smart&amp;auto=webp&amp;s=ba678b1106c159c0948083a74a7365db316fbbc0',
                                          'width': 320}],
                         'source': {'height': 202,
                                    'url': 'https://external-preview.redd.it/zHrVWNaw0APpJIrFxhDL391gij4nO_PKUynhVbFC
tW0.jpg?auto=webp&amp;s=a0bc9ba23aa380b1808f482242ca216ac4f58e81',
                                    'width': 320},
                         'variants': {}}]},
 'pwls': 6,
 'quarantine': False,
 'removal_reason': None,
 'report_reasons': None,
 'saved': True,
 'score': 101,
 'secure_media': None,
 'secure_media_embed': {},
 'selftext': '',
 'selftext_html': None,
 'send_replies': True,
 'spoiler': False,
 'steward_reports': [],
 'stickied': False,
 'subreddit': 'golang',
 'subreddit_id': 't5_2rc7j',
 'subreddit_name_prefixed': 'r/golang',
 'subreddit_subscribers': 93043,
 'subreddit_type': 'public',
 'suggested_sort': None,
 'thumbnail': 'default',
 'thumbnail_height': 88,
 'thumbnail_width': 140,
 'title': 'Go Modules: v2 and Beyond - The Go Blog',
 'total_awards_received': 0,
 'ups': 101,
 'url': 'https://blog.golang.org/v2-go-modules',
 'user_reports': [],
 'view_count': None,
 'visited': False,
 'whitelist_status': 'all_ads',
 'wls': 6}
