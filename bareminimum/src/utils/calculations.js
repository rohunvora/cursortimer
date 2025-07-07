// Calculation utilities following the layer math rules

export const calculateItemPrice = (item, isMarried, numKids) => {
  let price = item.price;
  
  // Apply spouse variant if married
  if (isMarried && item.spouse_variant_price !== null) {
    price = item.spouse_variant_price;
  }
  
  // Add kid variant prices (additive, not replacement)
  if (numKids > 0 && item.kid_variant_price !== null) {
    price += item.kid_variant_price * numKids;
  }
  
  return price;
};

export const calculateTotals = (cart, items, isMarried, numKids) => {
  // Start with user-selected items
  let subtotal = 0;
  const itemsMap = new Map(items.map(item => [item.id, item]));
  
  // Calculate prices for items in cart
  cart.forEach(cartItem => {
    const item = itemsMap.get(cartItem.id);
    if (item) {
      const itemPrice = calculateItemPrice(item, isMarried, numKids);
      subtotal += itemPrice * cartItem.quantity;
    }
  });
  
  // Add forced items
  let forcedItemsTotal = 0;
  
  // Marriage forced adds
  if (isMarried) {
    // Check if engagement ring and wedding are already in cart
    const hasRing = cart.some(item => item.id === 'engagement-ring');
    const hasWedding = cart.some(item => item.id === 'wedding-ceremony');
    
    if (!hasRing) {
      forcedItemsTotal += 15000; // Engagement ring
    }
    if (!hasWedding) {
      forcedItemsTotal += 25000; // Wedding
    }
  }
  
  // Kids forced adds
  if (numKids > 0) {
    // Check if tuition is already in cart
    const tuitionInCart = cart.find(item => item.id === 'private-school-tuition');
    const tuitionQuantityInCart = tuitionInCart ? tuitionInCart.quantity : 0;
    const tuitionNeeded = Math.max(0, numKids - tuitionQuantityInCart);
    forcedItemsTotal += 35000 * tuitionNeeded;
  }
  
  // Calculate base total
  const baseTotal = subtotal + forcedItemsTotal;
  
  // Apply married multiplier
  const multipliedTotal = isMarried ? baseTotal * 2 : baseTotal;
  
  // Calculate fees (10%)
  const fees = Math.round(multipliedTotal * 0.1);
  
  // Final total
  const total = multipliedTotal + fees;
  
  return {
    subtotal: baseTotal,
    forcedItemsTotal,
    multipliedTotal,
    marriedMultiplier: isMarried ? 2 : 1,
    fees,
    total
  };
};

export const formatPrice = (price) => {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD',
    minimumFractionDigits: 0,
    maximumFractionDigits: 0
  }).format(price);
};

export const generateShareableLink = (cart, isMarried, numKids) => {
  const params = new URLSearchParams();
  
  // Encode cart items
  if (cart.length > 0) {
    const cartString = cart.map(item => `${item.id}:${item.quantity}`).join(',');
    params.set('c', cartString);
  }
  
  // Encode life situation
  if (isMarried) params.set('m', '1');
  if (numKids > 0) params.set('k', numKids.toString());
  
  return `${window.location.origin}?${params.toString()}`;
};

export const parseShareableLink = (searchParams) => {
  const cart = [];
  const cartParam = searchParams.get('c');
  
  if (cartParam) {
    cartParam.split(',').forEach(itemString => {
      const [id, quantity] = itemString.split(':');
      if (id && quantity) {
        cart.push({ id, quantity: parseInt(quantity, 10) });
      }
    });
  }
  
  const isMarried = searchParams.get('m') === '1';
  const numKids = parseInt(searchParams.get('k') || '0', 10);
  
  return { cart, isMarried, numKids };
};