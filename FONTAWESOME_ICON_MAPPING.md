# FontAwesome Icon Mapping Guide

This document provides a comprehensive mapping from Material Icons to FontAwesome icons for the Betting League Championship application.

## Conversion Pattern

Replace: `<mat-icon>icon_name</mat-icon>`  
With: `<i class="fas fa-icon-name"></i>`

## Icon Mappings

### Navigation & UI Icons
| Material Icon | FontAwesome Icon | CSS Class | Usage |
|---------------|------------------|-----------|--------|
| `sports` | `trophy` | `fas fa-trophy` | Welcome header, tournaments |
| `live_tv` | `tv` | `fas fa-tv` | Live matches |
| `schedule` | `clock` | `fas fa-clock` | Upcoming matches |
| `history` | `clock-rotate-left` | `fas fa-clock-rotate-left` | Recent matches |
| `history` | `history` | `fas fa-history` | Navigation history |
| `home` | `home` | `fas fa-home` | Home navigation |
| `arrow_back` | `arrow-left` | `fas fa-arrow-left` | Back buttons |
| `arrow_up` / `keyboard_arrow_up` | `chevron-up` | `fas fa-chevron-up` | Increment arrows |
| `arrow_down` / `keyboard_arrow_down` | `chevron-down` | `fas fa-chevron-down` | Decrement arrows |
| `account_circle` | `user-circle` | `fas fa-user-circle` | User menu trigger |

### Sports & Competition Icons
| Material Icon | FontAwesome Icon | CSS Class | Usage |
|---------------|------------------|-----------|--------|
| `sports_soccer` | `futbol` | `fas fa-futbol` | Soccer/Football |
| `emoji_events` | `trophy` | `fas fa-trophy` | Final stage |
| `bronze` | `medal` | `fas fa-medal` | 3rd place |
| `military_tech` | `award` | `fas fa-award` | Semi-final |
| `shield` | `shield-alt` | `fas fa-shield-alt` | Quarter-final |
| `sports` | `futbol` | `fas fa-futbol` | Round of 16 |
| `groups` | `users` | `fas fa-users` | Group stage |
| `group_work` | `user-friends` | `fas fa-user-friends` | Group variations |
| `leaderboard` | `ranking-star` | `fas fa-ranking-star` | Rankings |

### User & Profile Icons
| Material Icon | FontAwesome Icon | CSS Class | Usage |
|---------------|------------------|-----------|--------|
| `person` | `user` | `fas fa-user` | User avatar |
| `account_circle` | `user-circle` | `fas fa-user-circle` | User account |
| `email` | `envelope` | `fas fa-envelope` | Email address |
| `badge` | `id-badge` | `fas fa-id-badge` | User ID |
| `security` | `shield-alt` | `fas fa-shield-alt` | Security settings |
| `admin_panel_settings` | `user-shield` | `fas fa-user-shield` | Admin status |
| `verified_user` | `user-check` | `fas fa-user-check` | Verified user |
| `settings` | `cog` | `fas fa-cog` | Settings |
| `refresh` | `sync-alt` | `fas fa-sync-alt` | Refresh action |
| `dashboard` | `tachometer-alt` | `fas fa-tachometer-alt` | Dashboard |
| `logout` | `sign-out-alt` | `fas fa-sign-out-alt` | Logout |
| `login` | `sign-in-alt` | `fas fa-sign-in-alt` | Login |

### Authentication & Form Icons
| Material Icon | FontAwesome Icon | CSS Class | Usage |
|---------------|------------------|-----------|--------|
| `person_add` | `user-plus` | `fas fa-user-plus` | Registration |
| `visibility` | `eye` | `fas fa-eye` | Show password |
| `visibility_off` | `eye-slash` | `fas fa-eye-slash` | Hide password |
| `info` | `info-circle` | `fas fa-info-circle` | Information |

### Status & Validation Icons
| Material Icon | FontAwesome Icon | CSS Class | Usage |
|---------------|------------------|-----------|--------|
| `check_circle` | `check-circle` | `fas fa-check-circle` | Success status |
| `token` | `key` | `fas fa-key` | Token/credential |
| `schedule` | `clock` | `fas fa-clock` | Time/schedule |
| `bug_report` | `bug` | `fas fa-bug` | Bug reports |
| `code` | `code` | `fas fa-code` | Code/development |
| `visibility_off` | `eye-slash` | `fas fa-eye-slash` | Hide content |
| `clear` | `times` | `fas fa-times` | Clear/close |
| `close` | `times` | `fas fa-times` | Close dialog |
| `preview` | `eye` | `fas fa-eye` | Preview content |

### Sports & Betting Icons
| Material Icon | FontAwesome Icon | CSS Class | Usage |
|---------------|------------------|-----------|--------|
| `sports_score` | `calculator` | `fas fa-calculator` | Score calculation |
| `radio_button_checked` | `circle` | `fas fa-circle` | Live indicator |

### Error & System Icons
| Material Icon | FontAwesome Icon | CSS Class | Usage |
|---------------|------------------|-----------|--------|
| `search_off` | `search-minus` | `fas fa-search-minus` | Search not found |
| `lock` | `lock` | `fas fa-lock` | Access denied |

## Bet Status Icons with Colors

The `getBetStatusIconClass()` method returns FontAwesome classes with Bootstrap-style colors:

```typescript
getBetStatusIconClass(status: string): string {
  switch (status) {
    case 'PENDING': return 'fas fa-clock text-warning';
    case 'WON': return 'fas fa-check-circle text-success'; 
    case 'LOST': return 'fas fa-times-circle text-danger';
    case 'VOID': return 'fas fa-ban text-muted';
    default: return 'fas fa-question-circle text-secondary';
  }
}
```

## CSS Class Updates

Update CSS selectors from `mat-icon` to `i`:

```css
/* Old */
.user-avatar mat-icon { color: #666; }

/* New */  
.user-avatar i { color: #666; }
```

## Pro Icons

If using FontAwesome Pro, consider these enhanced alternatives:
- `fad` prefix for duotone icons
- `fal` prefix for light weight  
- `far` prefix for regular weight
- `fab` prefix for brand icons

## Implementation Notes

1. **Color Classes**: Use Bootstrap utility classes (`text-success`, `text-warning`, etc.) for consistent coloring
2. **Sizing**: FontAwesome icons scale naturally with font-size
3. **Accessibility**: FontAwesome icons inherit ARIA support
4. **Performance**: CDN loading provides optimal performance vs npm packages

## Conversion Checklist

- [x] Dashboard navigation icons (trophy, tv, clock, etc.)
- [x] Bet status icons with dynamic colors  
- [x] Score increment/decrement arrows
- [x] Sports and competition icons
- [x] Stage icons (final, semi-final, etc.)
- [x] Not-found page icons (search-minus, home, arrow-left)
- [x] Unauthorized page icons (lock, home, sign-in-alt)
- [x] Profile component icons (user, envelope, shield, etc.)
- [x] Dashboard component icons (trophy, circle, futbol, ranking-star)
- [x] Bet dialog component icons (futbol, times, calculator, check-circle)
- [x] Login component icons (futbol, shield-alt, user-check, users, sign-in-alt, user-plus, info-circle)
- [x] Register component icons (user-plus, user, user-circle, envelope, eye/eye-slash)
- [x] **Navigation bar icons (futbol brand, user-circle menu, user, history, cog, sign-out-alt)**
- [x] CSS selector updates throughout (mat-icon → i)
- [x] Dynamic icon classes with conditional binding
- [x] **Complete Material Icon elimination verified**
- [x] Final build verification successful

## 🎉 **COMPLETE CONVERSION VERIFIED!** 🎉

**ALL Material Icons have been successfully converted to FontAwesome icons throughout the entire application, including the navigation bar!**