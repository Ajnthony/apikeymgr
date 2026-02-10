# API Key Manager

This is an API key manager built with Python/Django, which can create, rotate, and delete API keys. Users can have multiple API keys and are allowed to name each key for easier reference.

# What this does

This API will perform basic CRUD operation, and will also manage the auto-rotation of existing API keys for security purpose. It goes without saying that the signed in user can interact with the API keys they own only...

## Object model

### API Key

```
{
  id
  api_key
  name
  user
  is_active
  revoked_at
  created_at
  last_used_at
  expires_at
}
```

`id`: id\
`api_key`: the API will generate a new API key for use and hash it before saving it to DB. All the API keys will be stored AFTER hash; no original api key in the DB.\
`name`: name of the API key for easier reference (optional)\
`user`: owner of the API key
`is_active`: a boolean that indicates whether the API key is active or not\
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
    is_blocked

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
`is_blocked`: for easier user control - `False` by default. in case a user appears to be spamming, this can be set to `True` instead of revoking all their API keys

## API Endpoints

### GET key/

Retrieve all API keys the authenticated user owns

### POST key/

Generate a new API key

### GET key/key_id/

Retrieve an API key by id

### PATCH key/key_id/

Update the name for the API key

### DELETE key/key_id/

1st hit will be a "soft delete", which will just set `is_active` to `False`.\
2nd hit will actually remove the API key from the DB.

### API Key Rotation

To be added
