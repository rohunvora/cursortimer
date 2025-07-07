import React, { useState, useEffect, useMemo } from 'react';
import styled from 'styled-components';
import { dummyItems, categories } from './dummy-data';
import tokens from './design-tokens';
import ProductGrid from './components/ProductGrid';
import CartDrawer from './components/CartDrawer';
import Header from './components/Header';
import { calculateTotals, parseShareableLink } from './utils/calculations';
import toast from 'react-hot-toast';

const AppContainer = styled.div`
  min-height: 100vh;
  background: ${tokens.colors.white};
`;

const MainContent = styled.main`
  max-width: ${tokens.layout.maxWidth};
  margin: 0 auto;
  padding: ${tokens.layout.containerPadding};
  padding-top: 80px; // Account for fixed header
`;

function App() {
  // State
  const [cart, setCart] = useState([]);
  const [isMarried, setIsMarried] = useState(false);
  const [numKids, setNumKids] = useState(0);
  const [isDrawerOpen, setIsDrawerOpen] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('all');
  
  // Load from URL on mount
  useEffect(() => {
    const params = new URLSearchParams(window.location.search);
    const { cart: urlCart, isMarried: urlMarried, numKids: urlKids } = parseShareableLink(params);
    
    if (urlCart.length > 0) {
      setCart(urlCart);
      setIsMarried(urlMarried);
      setNumKids(urlKids);
      toast.success('Loaded shared cart');
    }
  }, []);
  
  // Filter items based on search and category
  const filteredItems = useMemo(() => {
    let items = dummyItems;
    
    // Category filter
    if (selectedCategory !== 'all') {
      items = items.filter(item => item.category === selectedCategory);
    }
    
    // Search filter
    if (searchQuery) {
      const query = searchQuery.toLowerCase();
      items = items.filter(item => 
        item.name.toLowerCase().includes(query) ||
        item.category.toLowerCase().includes(query)
      );
    }
    
    return items;
  }, [searchQuery, selectedCategory]);
  
  // Calculate totals
  const totals = useMemo(() => {
    return calculateTotals(cart, dummyItems, isMarried, numKids);
  }, [cart, isMarried, numKids]);
  
  // Cart actions
  const addToCart = (itemId) => {
    const existingItem = cart.find(item => item.id === itemId);
    
    if (existingItem) {
      setCart(cart.map(item => 
        item.id === itemId 
          ? { ...item, quantity: item.quantity + 1 }
          : item
      ));
    } else {
      setCart([...cart, { id: itemId, quantity: 1 }]);
    }
    
    toast.success('Added to cart');
  };
  
  const removeFromCart = (itemId) => {
    setCart(cart.filter(item => item.id !== itemId));
    toast.success('Removed from cart');
  };
  
  const updateQuantity = (itemId, quantity) => {
    if (quantity <= 0) {
      removeFromCart(itemId);
    } else {
      setCart(cart.map(item => 
        item.id === itemId 
          ? { ...item, quantity }
          : item
      ));
    }
  };
  
  const clearCart = () => {
    setCart([]);
    setIsMarried(false);
    setNumKids(0);
    toast.success('Cart cleared');
  };
  
  const surpriseMe = () => {
    // Get random items not in cart
    const availableItems = dummyItems.filter(item => 
      !cart.some(cartItem => cartItem.id === item.id)
    );
    
    if (availableItems.length === 0) {
      toast.error('All items already in cart!');
      return;
    }
    
    // Add 3-5 random items
    const numItems = Math.floor(Math.random() * 3) + 3;
    const randomItems = [];
    
    for (let i = 0; i < Math.min(numItems, availableItems.length); i++) {
      const randomIndex = Math.floor(Math.random() * availableItems.length);
      const item = availableItems.splice(randomIndex, 1)[0];
      randomItems.push({ id: item.id, quantity: 1 });
    }
    
    setCart([...cart, ...randomItems]);
    toast.success(`Added ${randomItems.length} surprise items!`);
  };
  
  return (
    <AppContainer>
      <Header
        cartCount={cart.reduce((sum, item) => sum + item.quantity, 0)}
        total={totals.total}
        onCartClick={() => setIsDrawerOpen(true)}
        searchQuery={searchQuery}
        onSearchChange={setSearchQuery}
        selectedCategory={selectedCategory}
        onCategoryChange={setSelectedCategory}
        categories={categories}
        onSurpriseMe={surpriseMe}
      />
      
      <MainContent>
        <ProductGrid
          items={filteredItems}
          cart={cart}
          onAddToCart={addToCart}
          isMarried={isMarried}
          numKids={numKids}
        />
      </MainContent>
      
      <CartDrawer
        isOpen={isDrawerOpen}
        onClose={() => setIsDrawerOpen(false)}
        cart={cart}
        items={dummyItems}
        isMarried={isMarried}
        numKids={numKids}
        onIsMarriedChange={setIsMarried}
        onNumKidsChange={setNumKids}
        onUpdateQuantity={updateQuantity}
        onRemoveFromCart={removeFromCart}
        onClearCart={clearCart}
        totals={totals}
      />
    </AppContainer>
  );
}

export default App;