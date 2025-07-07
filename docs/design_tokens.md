# Design-Token Snapshot — "Amazon-Brutalist"

Locked **2025-07-07** — freeze dates matter so marketing & dev can sync screenshots.

---

## 1. Typography

| Token | Value | Notes |
|-------|-------|-------|
| `fontFamily-system` | `-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Oxygen, Ubuntu, Cantarell, "Open Sans", "Helvetica Neue", sans-serif` | No web-font download. |
| `fontSize-xl` | `28px` | Hero cost figures & drawer header. |
| `fontSize-md` | `14px` | Body copy, chips, totals. |
| `fontSize-sm` | `12px` | Caption, fine print. |

## 2. Spacing & Sizing

8-pt grid ➜ use multiples of **8** only.

| Token | Pixels |
|-------|--------|
| `space-1` | 8px |
| `space-2` | 16px |
| `space-3` | 24px |
| `space-4` | 32px |
| `borderRadius-card` | 2px |
| `borderWidth-thin` | 1px |
| `borderWidth-thick` | 2px |

## 3. Button Copy (exact, all-caps)

* `ADD TO CART`
* `PLACE ORDER`
* `SURPRISE ME`

No secondary variants for launch—stick to primary style.

## 4. Color Cheatsheet (minimum viable palette)

| Role | Hex | WCAG contrast vs white |
|------|-----|------------------------|
| `brand-blue` | `#146FF5` | 5.9:1 (AA) |
| `neutral-900` | `#101010` | — |
| `neutral-100` | `#FFFFFF` | — |

## 5. CSS Custom Properties Example

```css
:root {
  /* Typography */
  --font-family-system: -apple-system, BlinkMacSystemFont,"Segoe UI",Roboto,Oxygen,Ubuntu,Cantarell,"Open Sans","Helvetica Neue",sans-serif;
  --font-size-xl: 28px;
  --font-size-md: 14px;
  --font-size-sm: 12px;

  /* Spacing */
  --space-1: 8px;
  --space-2: 16px;
  --space-3: 24px;
  --space-4: 32px;

  /* Borders */
  --border-width-thin: 1px;
  --border-width-thick: 2px;
  --border-radius-card: 2px;

  /* Colors */
  --color-brand-blue: #146FF5;
  --color-neutral-900: #101010;
  --color-neutral-100: #FFFFFF;
}
```

Copy/paste into your root CSS module; update only via PRs referencing this doc.