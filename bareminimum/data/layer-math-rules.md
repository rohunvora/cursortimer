# Layer Math Rules Specification

## Overview
The layer math system applies multipliers and forced additions based on user's life situation toggles.

## Rules

### 1. Married Toggle
When the "Married" toggle is activated:

1. **First**: Add these forced items to the cart (if not already present):
   - Engagement Ring: $15,000
   - Wedding Ceremony & Reception: $25,000

2. **Then**: Apply a 2x multiplier to the ENTIRE basket total
   - This includes all items in cart PLUS the forced additions
   - Formula: `final_total = (subtotal + forced_items) × 2`

3. **Special handling for spouse variants**:
   - Some items have `spouse_variant_price` defined
   - When married toggle is ON, these items use their spouse variant price instead of base price
   - If spouse variant exists, it replaces the base price (not added to it)

### 2. Kids Dropdown
When kids count is > 0:

1. **For each child**, add these forced items:
   - Private School Tuition: $35,000 per child
   - These stack (2 kids = $70,000 in tuition)

2. **Special handling for kid variants**:
   - Some items have `kid_variant_price` defined
   - When kids > 0, these items ADD their kid variant price × number of kids
   - Formula for items with kid variants: `item_total = base_price + (kid_variant_price × num_kids)`

### 3. Order of Operations
This is critical for consistent calculations:

1. Start with base cart items at base prices
2. If married: swap in spouse variant prices where applicable
3. If kids > 0: add kid variant prices where applicable
4. Add forced items (engagement ring, wedding, tuition)
5. Calculate subtotal
6. If married: multiply entire subtotal by 2
7. Add fees (10% of post-multiplier total)
8. Calculate final total

### 4. Edge Cases

- **Item already in cart**: If user manually added engagement ring before toggling married, don't add it again
- **Removing toggles**: When married toggle turned OFF, remove forced items UNLESS user manually added them
- **Price display**: Always show breakdown clearly in receipt
- **Rounding**: All calculations round to nearest dollar

## Example Calculation

Cart: Rolex ($8,500), Birkin Bag ($12,000)
Married: Yes (with spouse who wants their own Rolex and Birkin)
Kids: 2

1. Base items with spouse variants: $8,500 + $8,500 + $12,000 + $12,000 = $41,000
2. Add forced items: $15,000 + $25,000 = $40,000
3. Add kid items: $35,000 × 2 = $70,000
4. Subtotal: $41,000 + $40,000 + $70,000 = $151,000
5. Married multiplier: $151,000 × 2 = $302,000
6. Fees (10%): $30,200
7. **Total: $332,200**

## Implementation Notes

- Store forced items separately from user-added items in state
- Track which items were force-added vs manually added
- Update calculations reactively when toggles change
- Show clear line items in receipt for transparency