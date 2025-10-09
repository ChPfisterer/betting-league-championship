# FontAwesome Integration Guide

## Installation

```bash
npm install @fortawesome/angular-fontawesome @fortawesome/fontawesome-svg-core @fortawesome/free-solid-svg-icons @fortawesome/free-regular-svg-icons @fortawesome/free-brands-svg-icons
```

## 1. Update Component Imports

Replace Material Icon imports with FontAwesome:

```typescript
// OLD - Material Icons
import { MatIconModule } from '@angular/material/icon';

// NEW - FontAwesome
import { FontAwesomeModule } from '@fortawesome/angular-fontawesome';
import { FaIconLibrary } from '@fortawesome/angular-fontawesome';
import { fas } from '@fortawesome/free-solid-svg-icons';
import { far } from '@fortawesome/free-regular-svg-icons';
import { fab } from '@fortawesome/free-brands-svg-icons';
```

## 2. Component Class Configuration

```typescript
export class YourComponent implements OnInit {
  constructor(private library: FaIconLibrary) {
    // Add icon packs to the library
    library.addIconPacks(fas, far, fab);
  }
}
```

## 3. Template Conversion Examples

### Sports & Gaming Icons
```html
<!-- OLD Material Icons -->
<mat-icon>sports</mat-icon>
<mat-icon>sports_soccer</mat-icon>
<mat-icon>live_tv</mat-icon>
<mat-icon>schedule</mat-icon>

<!-- NEW FontAwesome Icons -->
<fa-icon [icon]="['fas', 'trophy']"></fa-icon>
<fa-icon [icon]="['fas', 'futbol']"></fa-icon>
<fa-icon [icon]="['fas', 'tv']"></fa-icon>
<fa-icon [icon]="['fas', 'clock']"></fa-icon>
```

### Arrow Icons
```html
<!-- OLD Material Icons -->
<mat-icon>keyboard_arrow_up</mat-icon>
<mat-icon>keyboard_arrow_down</mat-icon>

<!-- NEW FontAwesome Icons -->
<fa-icon [icon]="['fas', 'chevron-up']"></fa-icon>
<fa-icon [icon]="['fas', 'chevron-down']"></fa-icon>
```

### Action Icons
```html
<!-- OLD Material Icons -->
<mat-icon>check_circle</mat-icon>
<mat-icon>close</mat-icon>
<mat-icon>settings</mat-icon>

<!-- NEW FontAwesome Icons -->
<fa-icon [icon]="['fas', 'circle-check']"></fa-icon>
<fa-icon [icon]="['fas', 'xmark']"></fa-icon>
<fa-icon [icon]="['fas', 'gear']"></fa-icon>
```

## 4. Icon Styling

FontAwesome icons can be styled like regular elements:

```html
<!-- Size variations -->
<fa-icon [icon]="['fas', 'futbol']" size="xs"></fa-icon>
<fa-icon [icon]="['fas', 'futbol']" size="sm"></fa-icon>
<fa-icon [icon]="['fas', 'futbol']" size="lg"></fa-icon>
<fa-icon [icon]="['fas', 'futbol']" size="2x"></fa-icon>

<!-- Custom CSS classes -->
<fa-icon [icon]="['fas', 'futbol']" class="text-primary"></fa-icon>

<!-- Inline styles -->
<fa-icon [icon]="['fas', 'futbol']" [styles]="{'color': 'red'}"></fa-icon>
```

## 5. Pro Icons (if you have FontAwesome Pro)

For Pro icons, install additional packages:

```bash
npm install @fortawesome/pro-solid-svg-icons @fortawesome/pro-regular-svg-icons @fortawesome/pro-light-svg-icons
```

Then import and use:

```typescript
import { faPro } from '@fortawesome/pro-solid-svg-icons';

// In template
<fa-icon [icon]="['fad', 'futbol']"></fa-icon> <!-- Duotone -->
<fa-icon [icon]="['fal', 'futbol']"></fa-icon> <!-- Light -->
```

## 6. Icon Mapping for Your App

Here's a mapping of your current Material Icons to FontAwesome equivalents:

| Material Icon | FontAwesome Equivalent | Usage |
|---------------|------------------------|-------|
| `sports` | `['fas', 'trophy']` | General sports |
| `sports_soccer` | `['fas', 'futbol']` | Football/Soccer |
| `live_tv` | `['fas', 'tv']` | Live matches |
| `schedule` | `['fas', 'clock']` | Time/Schedule |
| `keyboard_arrow_up` | `['fas', 'chevron-up']` | Increment |
| `keyboard_arrow_down` | `['fas', 'chevron-down']` | Decrement |
| `check_circle` | `['fas', 'circle-check']` | Success/Submit |
| `close` | `['fas', 'xmark']` | Close/Cancel |
| `menu` | `['fas', 'bars']` | Menu |
| `person` | `['fas', 'user']` | User profile |
| `logout` | `['fas', 'right-from-bracket']` | Logout |
| `history` | `['fas', 'clock-rotate-left']` | History |
| `preview` | `['fas', 'eye']` | Preview |

## 7. Complete Component Example

```typescript
import { Component, OnInit } from '@angular/core';
import { FontAwesomeModule, FaIconLibrary } from '@fortawesome/angular-fontawesome';
import { fas } from '@fortawesome/free-solid-svg-icons';

@Component({
  selector: 'app-example',
  standalone: true,
  imports: [FontAwesomeModule],
  template: `
    <button>
      <fa-icon [icon]="['fas', 'futbol']"></fa-icon>
      Football Match
    </button>
    <fa-icon [icon]="['fas', 'chevron-up']" (click)="increment()"></fa-icon>
  `
})
export class ExampleComponent {
  constructor(library: FaIconLibrary) {
    library.addIconPacks(fas);
  }
}
```

## 8. Advantages of FontAwesome over Material Icons

1. **More Sports Icons**: Better selection for sports apps
2. **Consistent Styling**: More predictable across browsers
3. **Pro Version**: Access to premium icons if needed
4. **Better Performance**: SVG-based, smaller bundle size
5. **Theming**: Easier to style and customize

## 9. Migration Steps

1. Install FontAwesome packages
2. Update component imports
3. Add FontAwesome to component imports array
4. Configure icon library in constructor
5. Replace `<mat-icon>` with `<fa-icon [icon]="...">` in templates
6. Test all icon displays
7. Remove unused Material Icon imports