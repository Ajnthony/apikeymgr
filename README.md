# API Key Manager

This is an API key manager built with Python/Django, which can create, rotate, and delete API keys. Users can have multiple API keys and are allowed to name each key for easier reference.

# What this does

This API will perform basic CRUD operation for the API keys that users can use\* and will also manage the auto-rotation of existing API keys for security purpose.

\* actually they cannot; it's just a random string.

## Object model

### API Key

```
{
  id
  api_key_hash
  name
  user
  is_active
  daily_use_count
  total_use_count
  revoked_at
  created_at
  last_used_at
  expires_at
}
```

`id`: id\
`api_key_hash`: the API will generate a new API key for use and hash it before saving it to DB. All the API keys will be stored AFTER hash; no original api key in the DB.\
`name`: name of the API key for easier reference (optional)\
`user`: owner of the API key
`is_active`: a boolean that indicates whether the API key is active or not\
`daily_use_count`: how many times was this key used today?\
`total_use_count`: how many times was this key used since its creation?\
`revoked_at`: timestamp when the API key was revoked (1st DELETE request). If the API key becomes active again then this should be `None`\
`created_at`: timestamp auto-generated at the time of creation\
`last_used_at`: timestamp auto-generated at the time of the most recent usage\
`expires_at` timestamp when the API key will automatically get rotated again

### User

```
{
    id
    full_name
    username
    email
    plan
    created_at
    updated_at
    is_suspended

    # built-in fields
    is_active
    is_staff
    is_superuser
}
```

`id`: user id\
`full_name`: user's full name (optional)\
`username`: username (optional, unique)\
`email`: user's email; they will log in with this (unique)\
`plan`: depending on the plan, users will have different rate limits\
`created_at`: timestamp at the time of user creation\
`updated_at`: timestamp at times of user update - plan change, for example
`is_suspended`: for easier user control - `False` by default. in case a user appears to be spamming, this can be set to `True` instead of revoking all their API keys

## API Endpoints

### Key

#### GET api/key/

Retrieve all API keys the authenticated user owns

#### POST api/key/

Generate a new API key for the signed in user

#### GET api/key/key_id/

Retrieve an API key by id (signed user only, and only one of the keys they own)

#### PATCH api/key/key_id/update/

Update the name for the API key (signed user only, and only one of the keys they own)

#### PATCH api/key/key_id/call/

Simulate the key usage, so its count values will be incremented (signed user only, and only one of the keys they own)

#### PATCH api/key/key_id/delete/

1st hit will be a "soft delete", which will just set `is_active` to `False`.\
2nd hit will actually remove the API key from the DB. (signed user only, and only one of the keys they own)

#### DELETE api/key/key_id/

(ADMIN) removes a key instantly

#### API Key Rotation

To be added

### Token

#### POST api/token/

generates 2 JWT tokens: 1 access and 1 refresh

#### POST api/token/refresh/

refresh token

#### POST api/token/verify/

verify token
