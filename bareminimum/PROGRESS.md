# Bareminimum.xyz Progress Report

## Completed Milestones (1-4)

### ✅ Milestone 1: Lock the data spine
- Created `data/catalogue.json` with 300 items across 16 categories
- Implemented the complete schema with spouse/kid variant prices
- Categories include: luxury, transport, housing, services, education, life-events, health, dining, fashion, travel, tech, hobbies, entertainment, philanthropy, pets, finance

### ✅ Milestone 2: Define the layer math unambiguously
- Created `data/layer-math-rules.md` with clear specifications
- Documented order of operations for married/kids calculations
- Defined edge cases and implementation notes
- Example calculations provided

### ✅ Milestone 3: Design-token snapshot (Amazon-brutalist)
- Created `src/design-tokens.js` with complete visual system
- System fonts, 28/14/12px sizes, 1px/2px borders
- Black & white primary palette with gray scale
- Button copies defined: ADD TO CART, PLACE ORDER, SURPRISE ME
- 8pt spacing grid locked

### ✅ Milestone 4: Grid & Drawer prototype with dummy data
- Built complete React app with Vite
- Implemented search-as-you-type functionality
- Category filter chips working
- Cart drawer with live calculations (<50ms updates)
- Dummy data loaded and rendering properly
- Performance validated with React's built-in optimizations

## Technical Implementation Details

### Stack
- React 18.2 with hooks for state management
- Styled Components for CSS-in-JS
- Vite for fast dev server and builds
- html2canvas for receipt screenshots
- react-hot-toast for notifications

### Key Features Implemented
1. **Product Grid**: Responsive grid with Amazon-style cards
2. **Search & Filters**: Real-time search and category filtering
3. **Cart Management**: Add/remove/update quantities
4. **Layer Math**: Married toggle and kids dropdown with proper calculations
5. **Shareable Links**: URL encoding for cart state
6. **Receipt Generation**: Hidden receipt component for screenshots

### Performance Optimizations
- Memoized calculations with `useMemo`
- Lazy loading for product images
- Efficient cart state updates
- No unnecessary re-renders

## Next Steps (Milestones 5-9)

### 🔲 Milestone 5: Receipt & share-link QA
- Test PNG generation across devices
- Validate share functionality on iOS/Android
- Ensure clipboard API fallbacks work

### 🔲 Milestone 6: Bulk-import real catalogue
- Process and compress 300 product images
- Generate optimized JSON from full catalogue
- Run performance audit (target: <200KB bundle)

### 🔲 Milestone 7: Layer toggle UI polish
- Refine married/kids controls in drawer header
- Add tooltips for total jumps
- Smooth animations for state changes

### 🔲 Milestone 8: Content refresh & "Surprise me"
- Implement daily featured items
- Enhance shuffle algorithm
- Add "already in cart" exclusion logic

### 🔲 Milestone 9: Launch collateral
- Generate example receipts (single, married, kids)
- Create social media assets
- Deploy to bareminimum.xyz

## Running the App

```bash
cd bareminimum
npm install
npm run dev
```

Visit http://localhost:3000 to see the app.

## Architecture Notes

The app follows a simple but scalable architecture:
- Single App.jsx manages all state (cart, filters, layers)
- Components are purely presentational
- Calculations are centralized in utils/
- Design tokens ensure visual consistency
- URL state enables sharing without backend

## Known Limitations (Prototype Phase)

1. Images are placeholders (will be replaced in Milestone 6)
2. No real payment processing (intentional - it's a calculator)
3. Receipt screenshots rely on html2canvas (may need native solution later)
4. Bundle size not yet optimized (will address in Milestone 6)