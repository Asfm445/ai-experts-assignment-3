# EXPLANATION

## What was the bug?

The `Client.request()` method assumes that `oauth2_token` is always an `OAuth2Token` instance when checking expiration and attaching the Authorization header. However, the type of `oauth2_token` is declared as:

 Union[OAuth2Token, Dict[str, Any], None]




When a valid token is stored as a dictionary (e.g., retrieved from cache or deserialized from JSON), the client does not recognize it as an `OAuth2Token`. As a result, the expiration check is skipped and the Authorization header is not added to outgoing API requests.

## Why did it happen?

The logic in `request()` only performs expiry checks and header attachment if the token is an instance of `OAuth2Token`. Dictionary-based tokens bypass these checks entirely, even if they contain valid credentials, causing authenticated requests to be sent without an Authorization header.

Additionally, if a dictionary contains an ISO-8601 expiration string, directly constructing an `OAuth2Token` results in a runtime error when comparing string expiry values to integer timestamps.

## Why does your fix solve it?

The fix normalizes dictionary tokens into valid `OAuth2Token` instances before any expiration checks. If the expiration value is an ISO-8601 string, it is parsed using the existing `token_from_iso()` helper to ensure a valid integer timestamp is stored. This guarantees consistent token handling and ensures authenticated requests include the correct Authorization header.

## One realistic case your tests still don’t cover

The tests do not cover malformed token dictionaries (e.g., missing `access_token` or `expires_at`), which could still lead to runtime errors during normalization.
