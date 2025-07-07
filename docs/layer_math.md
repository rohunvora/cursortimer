# Basket Layer Logic (Single Source of Truth)

This document captures the **exact** pricing rules that power the cart subtotal ➜ fees ➜ TOTAL pipeline.  Engineering and QA should treat this as normative; any deviation is a bug.

---

## 1. Data Primitives

| Field | Type | Description |
|-------|------|-------------|
| `base_price` | number | Price of the item when added for **you**. |
| `spouse_variant_price` | number\|undefined | Price to add the **same** item for a spouse (if different).  If omitted, use `base_price`. |
| `kid_variant_price` | number\|undefined | Price to add the **same** item for **one** child (if different).  If omitted, use `base_price`. |

---

## 2. Forced-Add Items

These items are *always* injected before any multipliers when the corresponding toggle is active:

| Trigger | Item added | Unit price |
|---------|------------|-----------|
| `Married = ON` | Engagement Ring | **$15 000** |
|             | Wedding (event spend) | **$25 000** |
| `Kids = N`  | Private School Tuition × N | **$35 000** each |

---

## 3. Calculation Order (👇 **do not reorder!**)

1. **User adds/removes items** → basket `subtotal` starts as the sum of their `base_price`s.
2. **Apply forced-adds** (see §2) and append them to the basket.
3. **Apply kid tuition**: if `Kids = N`, append `N` tuition lines at $35 k each.
4. **Spouse Multiplier**
   • If `Married = ON` ➜ *after* steps 2-3, multiply the **entire basket subtotal** by **2**.
5. **Update Cart UI**: display line-item list (including injected ones), `Subtotal`, `Fees`, and **TOTAL**.

> Fees are outside the scope of this doc—handled by the finance module.

---

## 4. Example Walk-Through

Scenario: User adds *Birkin (
$12 000)* and *Tesla Model 3 ($40 000)*, then toggles **Married** and selects **Kids = 2**.

| Step | Basket Lines | Running Subtotal |
|------|--------------|------------------|
| Start | Birkin $12 000<br>Tesla $40 000 | $52 000 |
| Forced Adds | + Engagement Ring $15 000<br>+ Wedding $25 000 | $92 000 |
| Kid Tuition | + Tuition ×2 $70 000 | $162 000 |
| Spouse Multiplier | ×2 | $324 000 |

The UI should now read **Subtotal $324 000** (before fees).

---

## 5. Edge-Case Notes

• Kid dropdown = 0 ➜ skip step 3 entirely.
• Married = OFF ➜ skip steps 2(a-b) and 4.
• Tuition multiplication: tuition is added *before* the spouse multiplier, meaning tuition is also doubled when Married = ON. This is intentional to reflect two-household spend.
• Variant prices: if an item carries `spouse_variant_price` or `kid_variant_price`, substitute those *before* multiplying.

---

## 6. Contract Tests (pseudo-code)

```ts
// married, 1 kid, empty cart
expect(total([],{married:true,kids:1})).toBe((15000+25000+35000)*2)

// unmarried, 0 kids, single rolex
expect(total(["rolex"], {married:false,kids:0})).toBe(12000)

// married, 2 kids, rolex with spouseVariantPrice 11000
expect(total(["rolex"], {married:true,kids:2})).toBe(((11000+15000+25000)+(35000*2))*2)
```

Keep these green in CI.