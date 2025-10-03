# WebSocket API Specification with OAuth 2.0/OIDC

## Real-time Event Contracts

### Connection
```
WebSocket endpoint: /ws/updates
Authentication: OAuth 2.0 Bearer token via:
  - Query parameter: ?access_token=<jwt_token>
  - Authorization header: Authorization: Bearer <jwt_token>
  - Sec-WebSocket-Protocol: access_token, <jwt_token>
OIDC Requirements: Token must contain valid 'sub', 'aud', and 'scope' claims
Token Validation: JWK Set validation with Keycloak public keys
```

### Authentication Flow
```
1. Client obtains OAuth 2.0 access token from Keycloak
2. Client initiates WebSocket connection with Bearer token
3. Server validates JWT signature and claims
4. Server establishes authenticated session with user context
5. Automatic token refresh handled by client before expiration
```

### Message Format
All messages follow this structure:
```json
{
  "type": "string",
  "event": "string", 
  "data": "object",
  "timestamp": "ISO8601 string"
}
```

## Client → Server Messages

### Subscribe to Group Updates
```json
{
  "type": "subscribe",
  "event": "group_updates",
  "data": {
    "group_id": "uuid"
  }
}
```

### Subscribe to Match Updates  
```json
{
  "type": "subscribe", 
  "event": "match_updates",
  "data": {
    "match_id": "uuid"
  }
}
```

### Subscribe to Leaderboard Updates
```json
{
  "type": "subscribe",
  "event": "leaderboard_updates", 
  "data": {
    "group_id": "uuid",
    "season_id": "uuid" // optional
  }
}
```

### Unsubscribe
```json
{
  "type": "unsubscribe",
  "event": "group_updates|match_updates|leaderboard_updates",
  "data": {
    "group_id": "uuid", // if relevant
    "match_id": "uuid"  // if relevant
  }
}
```

## Server → Client Messages

### Connection Acknowledgment
```json
{
  "type": "ack",
  "event": "connected", 
  "data": {
    "user_id": "uuid",
    "session_id": "uuid"
  },
  "timestamp": "2025-10-03T14:30:00Z"
}
```

### Subscription Confirmation
```json
{
  "type": "ack",
  "event": "subscribed",
  "data": {
    "subscription_type": "group_updates|match_updates|leaderboard_updates",
    "resource_id": "uuid"
  },
  "timestamp": "2025-10-03T14:30:00Z"
}
```

### Match Status Update
```json
{
  "type": "update",
  "event": "match_status_changed",
  "data": {
    "match_id": "uuid",
    "old_status": "scheduled",
    "new_status": "live",
    "scheduled_at": "2025-10-03T15:00:00Z",
    "betting_deadline": "2025-10-03T14:00:00Z"
  },
  "timestamp": "2025-10-03T14:30:00Z"
}
```

### Live Score Update
```json
{
  "type": "update", 
  "event": "score_updated",
  "data": {
    "match_id": "uuid",
    "home_score": 1,
    "away_score": 0,
    "minute": 23,
    "status": "live"
  },
  "timestamp": "2025-10-03T15:23:00Z"
}
```

### Provisional Result Posted
```json
{
  "type": "update",
  "event": "provisional_result",
  "data": {
    "match_id": "uuid", 
    "home_score": 2,
    "away_score": 1,
    "winner": "home",
    "is_provisional": true,
    "entered_at": "2025-10-03T16:45:00Z"
  },
  "timestamp": "2025-10-03T16:45:00Z"
}
```

### Final Result Confirmed
```json
{
  "type": "update",
  "event": "result_finalized",
  "data": {
    "match_id": "uuid",
    "home_score": 2, 
    "away_score": 1,
    "winner": "home",
    "is_provisional": false,
    "finalized_at": "2025-10-03T18:30:00Z"
  },
  "timestamp": "2025-10-03T18:30:00Z"
}
```

### Leaderboard Update
```json
{
  "type": "update",
  "event": "leaderboard_changed", 
  "data": {
    "group_id": "uuid",
    "season_id": "uuid",
    "affected_users": [
      {
        "user_id": "uuid",
        "old_rank": 3,
        "new_rank": 2,
        "points_added": 3,
        "total_points": 15
      }
    ],
    "match_id": "uuid" // which match caused the update
  },
  "timestamp": "2025-10-03T16:45:00Z"
}
```

### Betting Deadline Warning
```json
{
  "type": "notification",
  "event": "deadline_warning",
  "data": {
    "match_id": "uuid",
    "deadline": "2025-10-03T14:00:00Z",
    "minutes_remaining": 15,
    "home_team": "Team A",
    "away_team": "Team B"
  },
  "timestamp": "2025-10-03T13:45:00Z"
}
```

### Deadline Changed
```json
{
  "type": "notification", 
  "event": "deadline_changed",
  "data": {
    "match_id": "uuid",
    "old_deadline": "2025-10-03T14:00:00Z",
    "new_deadline": "2025-10-03T13:30:00Z", 
    "reason": "Match rescheduled",
    "group_id": "uuid" // if group-specific
  },
  "timestamp": "2025-10-03T12:00:00Z"
}
```

### Match Rescheduled
```json
{
  "type": "notification",
  "event": "match_rescheduled", 
  "data": {
    "match_id": "uuid",
    "old_scheduled_at": "2025-10-03T15:00:00Z",
    "new_scheduled_at": "2025-10-04T15:00:00Z",
    "new_betting_deadline": "2025-10-04T14:00:00Z",
    "reason": "Weather conditions"
  },
  "timestamp": "2025-10-03T10:00:00Z"
}
```

### Group Invitation
```json
{
  "type": "notification",
  "event": "group_invitation",
  "data": {
    "group_id": "uuid",
    "group_name": "Friends League",
    "invited_by": "John Doe",
    "expires_at": "2025-10-06T14:30:00Z"
  },
  "timestamp": "2025-10-03T14:30:00Z"
}
```

### User Joined Group
```json
{
  "type": "update",
  "event": "user_joined_group",
  "data": {
    "group_id": "uuid",
    "user": {
      "id": "uuid",
      "display_name": "Jane Smith"
    },
    "member_count": 8
  },
  "timestamp": "2025-10-03T14:35:00Z"
}
```

### Error Messages
```json
{
  "type": "error",
  "event": "subscription_failed",
  "data": {
    "reason": "unauthorized",
    "message": "You are not a member of this group",
    "requested_resource": "group:uuid"
  },
  "timestamp": "2025-10-03T14:30:00Z"
}
```

```json
{
  "type": "error", 
  "event": "rate_limit_exceeded",
  "data": {
    "message": "Too many subscription requests",
    "retry_after": 30
  },
  "timestamp": "2025-10-03T14:30:00Z"
}
```

## Connection Management

### Heartbeat
- Server sends ping every 30 seconds
- Client must respond with pong within 10 seconds
- Connection terminated after 3 missed heartbeats

### Reconnection
- Client should implement exponential backoff (1s, 2s, 4s, 8s, max 30s)
- Server maintains subscription state for 5 minutes after disconnect
- Client must re-authenticate on reconnection

### Rate Limiting
- Maximum 10 subscription requests per minute per user
- Maximum 100 messages per minute per connection
- Violations result in temporary disconnection

## Security Considerations

### Authentication
- Bearer token required for connection
- Token validated on each subscription request
- Expired tokens result in disconnection

### Authorization  
- Users can only subscribe to groups they are members of
- Match subscriptions require group membership for that match
- Admin-only events filtered based on user permissions

### Data Privacy
- Only send data relevant to user's group memberships
- Mask sensitive information (invitation codes, emails)
- Audit log all subscription activities