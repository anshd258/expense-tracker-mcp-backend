# Authentication Guide

This API uses JWT Bearer token authentication. All endpoints except authentication endpoints require a valid Bearer token.

## Authentication Setup

The API uses HTTP Bearer authentication with JWT tokens. The authentication is configured to:
- Show properly in Swagger UI (`/docs`) with an "Authorize" button
- Validate tokens on all protected endpoints
- Return proper 401 errors for invalid/missing tokens

## How to Authenticate

### 1. Register a New User
```bash
POST /api/v1/auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "yourpassword",
  "full_name": "Your Name"
}
```

### 2. Login to Get Token
You can use either endpoint:

**Option A: JSON Login (Recommended for APIs)**
```bash
POST /api/v1/auth/token
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "yourpassword"
}
```

**Option B: Form Login (OAuth2 Compatible)**
```bash
POST /api/v1/auth/login
Content-Type: application/x-www-form-urlencoded

username=user@example.com&password=yourpassword
```

Both return:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer"
}
```

### 3. Use the Token
Include the token in the Authorization header for all protected endpoints:
```bash
GET /api/v1/auth/me
Authorization: Bearer eyJhbGciOiJIUzI1NiIs...
```

## Testing in Swagger UI

1. Navigate to `/docs`
2. Click the "Authorize" button (top right)
3. Enter your token in the format: `Bearer <your-token>` or just `<your-token>`
4. Click "Authorize"
5. Now you can test all protected endpoints directly from Swagger UI

## Authentication Options

### Current Setup: Dependency Injection
The current implementation uses FastAPI's dependency injection system with `Depends(get_current_user)` on each protected endpoint. This provides:
- Fine-grained control over which endpoints require authentication
- Easy to test individual endpoints
- Clear in code which endpoints are protected

### Alternative: Middleware-Based Authentication
If you prefer global authentication with exceptions for public routes, you can enable the middleware by uncommenting these lines in `main.py`:

```python
from app.middleware import AuthMiddleware
# ...
app.add_middleware(AuthMiddleware)
```

The middleware will:
- Automatically protect all routes except those in the PUBLIC_ROUTES list
- Attach user info to `request.state.user`
- Simplify endpoint definitions (no need for `Depends(get_current_user)`)

## Security Considerations

1. **Token Expiration**: Tokens expire after the time set in `ACCESS_TOKEN_EXPIRE_MINUTES` (default: 30 minutes)
2. **HTTPS**: Always use HTTPS in production to protect tokens in transit
3. **Token Storage**: Store tokens securely on the client side (not in localStorage for web apps)
4. **CORS**: Configure CORS appropriately for your frontend domain in production

## Troubleshooting

### "Not authenticated" Error
- Ensure you're including the Authorization header
- Check that the header format is: `Authorization: Bearer <token>`
- Verify the token hasn't expired

### Token Not Showing in Swagger UI
- Make sure you're using the correct format when authorizing
- Try refreshing the page after authorizing
- Check browser console for any errors

### Can't See Authorize Button
- Ensure the OpenAPI schema is properly configured
- Check that the server has restarted after code changes
- Clear browser cache and reload