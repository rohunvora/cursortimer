# Bare Minimum - Elite Lifestyle Calculator

A brutalist shopping cart application that calculates the true cost of elite lifestyle tiers with personalization layers.

## ✅ Implemented Milestones

### Milestone #1: Data Spine ✅
- Created product data structure with exact schema:
  - `id` (slug), `name`, `category`, `price`, `img_url`
  - `spouse_variant_price`, `kid_variant_price` (null if N/A)
- 20 dummy products across 6 categories (luxury, housing, transport, services, lifestyle)

### Milestone #2: Layer Math ✅
- **Married toggle** → adds Engagement Ring $15k + Wedding $25k, then multiplies full basket × 2
- **Kids dropdown** → adds Private School Tuition $35k per child
- Prevents "is it a bug or the rule?" debates with clear logic

### Milestone #3: Design Tokens ✅
- **Amazon-brutalist styling**:
  - System font stack
  - Font sizes: 28px/14px/12px
  - Border weights: 1px/2px
  - 8pt grid spacing
- **Button copies**: ADD TO CART, PLACE ORDER, SURPRISE ME

### Milestone #4: Grid & Drawer Prototype ✅
- Product grid with 20 dummy items following new data schema
- Search-as-you-type functionality
- Filter chips for categories
- Subtotal → Fees → TOTAL updates in <50ms
- Performance optimized

### Milestone #7: Layer Toggle UI ✅
- Married pill and Kids dropdown in drawer header
- Live cart updates with layer math
- Real-time total calculations

### Milestone #8: "Surprise Me" ✅
- Shuffle button that ignores already-in-cart items
- Adds 1-3 random products to cart

## 🚀 Quick Start

1. **Serve the application:**
   ```bash
   npm start
   # or
   python3 -m http.server 8000
   ```

2. **Open in browser:**
   ```
   http://localhost:8000
   ```

## 🎯 Key Features

- **Real-time Search**: Filter products by name or category
- **Category Filters**: Luxury, Housing, Transport, Services, Lifestyle
- **Layer Math**: 
  - Married: +$40k forced adds + 2x multiplier
  - Kids: +$35k per child
- **Performance**: Cart updates in <50ms
- **Responsive**: Works on desktop and mobile
- **Brutalist Design**: Clean, functional Amazon-inspired UI

## 📊 Current Data

- 20 products across 6 categories
- Price range: $3,000 - $50,000
- Variant pricing for spouse/kids where applicable
- Categories: luxury, housing, transport, services, lifestyle

## 🔧 Layer Math Logic

```javascript
// Base calculation
const baseSubtotal = cart.reduce((sum, item) => sum + item.price, 0);

// Married layer
if (isMarried) {
  forcedAdds += 15000; // Engagement ring
  forcedAdds += 25000; // Wedding
  multiplier = 2; // Double the basket
}

// Kids layer
if (numberOfKids > 0) {
  forcedAdds += 35000 * numberOfKids; // Private school per child
}

// Final calculation
const total = (baseSubtotal + forcedAdds) * multiplier;
```

## 🚧 Next Steps (Remaining Milestones)

- **Milestone #5**: Receipt & share-link functionality
- **Milestone #6**: Bulk-import real 300-item catalogue
- **Milestone #9**: Launch collateral and deployment

## 📱 Mobile Responsive

The app automatically adapts to mobile devices with:
- Stacked layout on screens <768px
- Touch-friendly buttons and controls
- Optimized cart drawer positioning

## 🎨 Design System

- **Colors**: Black on white, brutalist aesthetic
- **Typography**: System font stack for fast loading
- **Spacing**: 8pt grid system
- **Borders**: 1px standard, 2px for emphasis
- **Interactions**: Minimal hover effects, instant feedback

---

Ready to calculate your elite lifestyle tier? 🏆