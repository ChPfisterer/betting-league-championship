# FontAwesome CDN Usage Guide

## Using FontAwesome with CDN Kit

Since you've included FontAwesome via CDN kit, you can use icons directly with CSS classes:

### Basic Icon Usage:
```html
<!-- Simple icon -->
<i class="fas fa-futbol"></i>
<i class="fas fa-trophy"></i>
<i class="fas fa-chevron-up"></i>

<!-- Icon with text -->
<button>
  <i class="fas fa-futbol"></i>
  Football Match
</button>
```

### Size Variations:
```html
<i class="fas fa-futbol fa-xs"></i>    <!-- Extra small -->
<i class="fas fa-futbol fa-sm"></i>    <!-- Small -->
<i class="fas fa-futbol"></i>          <!-- Normal -->
<i class="fas fa-futbol fa-lg"></i>    <!-- Large -->
<i class="fas fa-futbol fa-xl"></i>    <!-- Extra large -->
<i class="fas fa-futbol fa-2x"></i>    <!-- 2x size -->
<i class="fas fa-futbol fa-3x"></i>    <!-- 3x size -->
```

### Icon Types (with your kit):
```html
<!-- Solid icons (fas) -->
<i class="fas fa-futbol"></i>
<i class="fas fa-trophy"></i>
<i class="fas fa-chevron-up"></i>

<!-- Regular icons (far) -->
<i class="far fa-futbol"></i>

<!-- Brands (fab) -->
<i class="fab fa-facebook"></i>

<!-- Pro icons (if available in your kit) -->
<i class="fal fa-futbol"></i>   <!-- Light -->
<i class="fad fa-futbol"></i>   <!-- Duotone -->
```

### Your Material Icon Replacements:

| Material Icon | FontAwesome CSS Class | HTML |
|---------------|----------------------|------|
| `sports` | `fas fa-trophy` | `<i class="fas fa-trophy"></i>` |
| `sports_soccer` | `fas fa-futbol` | `<i class="fas fa-futbol"></i>` |
| `schedule` | `fas fa-clock` | `<i class="fas fa-clock"></i>` |
| `keyboard_arrow_up` | `fas fa-chevron-up` | `<i class="fas fa-chevron-up"></i>` |
| `keyboard_arrow_down` | `fas fa-chevron-down` | `<i class="fas fa-chevron-down"></i>` |
| `check_circle` | `fas fa-circle-check` | `<i class="fas fa-circle-check"></i>` |
| `close` | `fas fa-xmark` | `<i class="fas fa-xmark"></i>` |
| `live_tv` | `fas fa-tv` | `<i class="fas fa-tv"></i>` |

### Styling Examples:
```html
<!-- Custom colors -->
<i class="fas fa-futbol" style="color: #4caf50;"></i>

<!-- CSS classes -->
<i class="fas fa-trophy text-warning"></i>

<!-- Combined with Angular -->
<i class="fas fa-chevron-up" 
   [class.text-success]="score > 0"
   [class.text-muted]="score === 0"></i>
```