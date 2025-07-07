import React, { useRef } from 'react';
import styled from 'styled-components';
import tokens from '../design-tokens';
import { calculateItemPrice, formatPrice, generateShareableLink } from '../utils/calculations';
import html2canvas from 'html2canvas';
import toast from 'react-hot-toast';

const Overlay = styled.div`
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  opacity: ${props => props.isOpen ? 1 : 0};
  pointer-events: ${props => props.isOpen ? 'auto' : 'none'};
  transition: opacity ${tokens.transitions.medium};
  z-index: ${tokens.zIndex.drawer};
`;

const Drawer = styled.div`
  position: fixed;
  right: 0;
  top: 0;
  bottom: 0;
  width: ${tokens.components.drawer.width};
  max-width: 100%;
  background: ${tokens.colors.white};
  border-left: ${tokens.borders.thick} ${tokens.colors.black};
  transform: translateX(${props => props.isOpen ? '0' : '100%'});
  transition: transform ${tokens.transitions.medium};
  display: flex;
  flex-direction: column;
  z-index: ${tokens.zIndex.drawer + 1};
`;

const DrawerHeader = styled.div`
  padding: ${tokens.components.drawer.padding};
  border-bottom: ${tokens.borders.thick} ${tokens.colors.black};
`;

const DrawerTitle = styled.h2`
  font-size: ${tokens.fontSizes.large};
  font-weight: ${tokens.fontWeights.bold};
  margin: 0 0 ${tokens.spacing.md} 0;
  display: flex;
  justify-content: space-between;
  align-items: center;
`;

const CloseButton = styled.button`
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
  background: none;
  border: ${tokens.borders.thin} ${tokens.colors.black};
  cursor: pointer;
  
  &:hover {
    background: ${tokens.colors.gray[100]};
  }
`;

const LayerControls = styled.div`
  display: flex;
  gap: ${tokens.spacing.md};
  align-items: center;
  flex-wrap: wrap;
`;

const LayerToggle = styled.label`
  display: flex;
  align-items: center;
  gap: ${tokens.spacing.sm};
  font-size: ${tokens.fontSizes.base};
  cursor: pointer;
  
  input[type="checkbox"] {
    width: 20px;
    height: 20px;
    cursor: pointer;
  }
`;

const KidsSelect = styled.select`
  height: 32px;
  padding: 0 ${tokens.spacing.sm};
  font-size: ${tokens.fontSizes.base};
  border: ${tokens.borders.thin} ${tokens.colors.black};
  background: ${tokens.colors.white};
  cursor: pointer;
`;

const DrawerContent = styled.div`
  flex: 1;
  overflow-y: auto;
  padding: ${tokens.components.drawer.padding};
`;

const CartItems = styled.div`
  display: flex;
  flex-direction: column;
  gap: ${tokens.spacing.md};
  margin-bottom: ${tokens.spacing.lg};
`;

const CartItem = styled.div`
  display: flex;
  gap: ${tokens.spacing.sm};
  padding: ${tokens.spacing.sm};
  border: ${tokens.borders.thin} ${tokens.colors.gray[300]};
`;

const ItemDetails = styled.div`
  flex: 1;
`;

const ItemName = styled.div`
  font-weight: ${tokens.fontWeights.bold};
  margin-bottom: ${tokens.spacing.xs};
`;

const ItemPrice = styled.div`
  font-size: ${tokens.fontSizes.small};
  color: ${tokens.colors.gray[600]};
  font-family: ${tokens.fonts.mono};
`;

const QuantityControls = styled.div`
  display: flex;
  align-items: center;
  gap: ${tokens.spacing.xs};
`;

const QuantityButton = styled.button`
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: ${tokens.colors.white};
  border: ${tokens.borders.thin} ${tokens.colors.black};
  cursor: pointer;
  font-weight: ${tokens.fontWeights.bold};
  
  &:hover {
    background: ${tokens.colors.gray[100]};
  }
`;

const Quantity = styled.span`
  min-width: 24px;
  text-align: center;
  font-family: ${tokens.fonts.mono};
`;

const RemoveButton = styled.button`
  padding: ${tokens.spacing.xs} ${tokens.spacing.sm};
  font-size: ${tokens.fontSizes.small};
  color: ${tokens.colors.error};
  border: ${tokens.borders.thin} ${tokens.colors.error};
  background: ${tokens.colors.white};
  cursor: pointer;
  text-transform: uppercase;
  
  &:hover {
    background: ${tokens.colors.error};
    color: ${tokens.colors.white};
  }
`;

const EmptyCart = styled.div`
  text-align: center;
  padding: ${tokens.spacing.xxl} 0;
  color: ${tokens.colors.gray[500]};
`;

const DrawerFooter = styled.div`
  padding: ${tokens.components.drawer.padding};
  border-top: ${tokens.borders.thick} ${tokens.colors.black};
`;

const TotalsBreakdown = styled.div`
  margin-bottom: ${tokens.spacing.lg};
  font-family: ${tokens.fonts.mono};
  font-size: ${tokens.fontSizes.small};
  
  > div {
    display: flex;
    justify-content: space-between;
    padding: ${tokens.spacing.xs} 0;
    
    &.total {
      font-size: ${tokens.fontSizes.base};
      font-weight: ${tokens.fontWeights.bold};
      border-top: ${tokens.borders.thin} ${tokens.colors.black};
      margin-top: ${tokens.spacing.sm};
      padding-top: ${tokens.spacing.sm};
    }
  }
`;

const FooterActions = styled.div`
  display: flex;
  flex-direction: column;
  gap: ${tokens.spacing.sm};
`;

const ActionButton = styled.button`
  width: 100%;
  height: ${tokens.components.button.height};
  font-size: ${tokens.components.button.fontSize};
  font-weight: ${tokens.components.button.fontWeight};
  background: ${props => props.primary ? tokens.colors.black : tokens.colors.white};
  color: ${props => props.primary ? tokens.colors.white : tokens.colors.black};
  border: ${tokens.components.button.borderWidth} solid ${tokens.colors.black};
  text-transform: uppercase;
  letter-spacing: 0.05em;
  transition: all ${tokens.transitions.fast};
  cursor: pointer;
  
  &:hover {
    background: ${props => props.primary ? tokens.colors.gray[800] : tokens.colors.gray[100]};
  }
  
  &:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }
`;

// Receipt component for screenshot
const Receipt = styled.div`
  position: fixed;
  left: -9999px;
  width: ${tokens.components.receipt.width};
  background: ${tokens.colors.white};
  padding: ${tokens.components.receipt.padding};
  font-family: ${tokens.fonts.mono};
  font-size: ${tokens.components.receipt.fontSize};
  line-height: ${tokens.components.receipt.lineHeight};
  color: ${tokens.colors.black};
  
  h1 {
    font-size: 18px;
    text-align: center;
    margin-bottom: ${tokens.spacing.md};
    text-transform: uppercase;
  }
  
  .divider {
    border-top: 1px dashed ${tokens.colors.black};
    margin: ${tokens.spacing.md} 0;
  }
  
  .item {
    display: flex;
    justify-content: space-between;
    margin-bottom: ${tokens.spacing.xs};
  }
  
  .total-section {
    margin-top: ${tokens.spacing.md};
    padding-top: ${tokens.spacing.md};
    border-top: 2px solid ${tokens.colors.black};
    
    .total {
      font-weight: ${tokens.fontWeights.bold};
      font-size: 16px;
    }
  }
  
  .footer {
    text-align: center;
    margin-top: ${tokens.spacing.lg};
    font-size: 10px;
    color: ${tokens.colors.gray[600]};
  }
`;

function CartDrawer({
  isOpen,
  onClose,
  cart,
  items,
  isMarried,
  numKids,
  onIsMarriedChange,
  onNumKidsChange,
  onUpdateQuantity,
  onRemoveFromCart,
  onClearCart,
  totals
}) {
  const receiptRef = useRef(null);
  const itemsMap = new Map(items.map(item => [item.id, item]));
  
  const handleShare = async () => {
    const link = generateShareableLink(cart, isMarried, numKids);
    
    try {
      await navigator.clipboard.writeText(link);
      toast.success('Link copied to clipboard!');
    } catch (err) {
      toast.error('Failed to copy link');
    }
  };
  
  const handleScreenshot = async () => {
    if (!receiptRef.current) return;
    
    // Show receipt temporarily
    receiptRef.current.style.left = '0';
    
    try {
      const canvas = await html2canvas(receiptRef.current, {
        backgroundColor: '#FFFFFF',
        scale: 2
      });
      
      // Convert to blob
      canvas.toBlob(async (blob) => {
        try {
          // Try to share via Web Share API
          if (navigator.share && navigator.canShare({ files: [new File([blob], 'receipt.png', { type: 'image/png' })] })) {
            await navigator.share({
              files: [new File([blob], 'receipt.png', { type: 'image/png' })],
              title: 'My Bare Minimum Receipt',
              text: `My bare minimum lifestyle costs ${formatPrice(totals.total)}`
            });
          } else {
            // Fallback: download the image
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'bare-minimum-receipt.png';
            a.click();
            URL.revokeObjectURL(url);
            toast.success('Receipt downloaded!');
          }
        } catch (err) {
          toast.error('Failed to share receipt');
        }
      }, 'image/png');
    } catch (err) {
      toast.error('Failed to generate receipt');
    } finally {
      // Hide receipt again
      receiptRef.current.style.left = '-9999px';
    }
  };
  
  return (
    <>
      <Overlay isOpen={isOpen} onClick={onClose} />
      
      <Drawer isOpen={isOpen}>
        <DrawerHeader>
          <DrawerTitle>
            Your Cart
            <CloseButton onClick={onClose}>×</CloseButton>
          </DrawerTitle>
          
          <LayerControls>
            <LayerToggle>
              <input
                type="checkbox"
                checked={isMarried}
                onChange={(e) => onIsMarriedChange(e.target.checked)}
              />
              Married
            </LayerToggle>
            
            <label>
              Kids:
              <KidsSelect
                value={numKids}
                onChange={(e) => onNumKidsChange(parseInt(e.target.value, 10))}
              >
                {[0, 1, 2, 3, 4, 5].map(n => (
                  <option key={n} value={n}>{n}</option>
                ))}
              </KidsSelect>
            </label>
          </LayerControls>
        </DrawerHeader>
        
        <DrawerContent>
          {cart.length === 0 ? (
            <EmptyCart>Your cart is empty</EmptyCart>
          ) : (
            <CartItems>
              {cart.map(cartItem => {
                const item = itemsMap.get(cartItem.id);
                if (!item) return null;
                
                const itemPrice = calculateItemPrice(item, isMarried, numKids);
                
                return (
                  <CartItem key={cartItem.id}>
                    <ItemDetails>
                      <ItemName>{item.name}</ItemName>
                      <ItemPrice>{formatPrice(itemPrice)} each</ItemPrice>
                    </ItemDetails>
                    
                    <QuantityControls>
                      <QuantityButton onClick={() => onUpdateQuantity(cartItem.id, cartItem.quantity - 1)}>
                        -
                      </QuantityButton>
                      <Quantity>{cartItem.quantity}</Quantity>
                      <QuantityButton onClick={() => onUpdateQuantity(cartItem.id, cartItem.quantity + 1)}>
                        +
                      </QuantityButton>
                    </QuantityControls>
                    
                    <RemoveButton onClick={() => onRemoveFromCart(cartItem.id)}>
                      Remove
                    </RemoveButton>
                  </CartItem>
                );
              })}
              
              {/* Show forced items */}
              {isMarried && !cart.some(item => item.id === 'engagement-ring') && (
                <CartItem style={{ opacity: 0.7 }}>
                  <ItemDetails>
                    <ItemName>Engagement Ring (Required)</ItemName>
                    <ItemPrice>{formatPrice(15000)}</ItemPrice>
                  </ItemDetails>
                </CartItem>
              )}
              
              {isMarried && !cart.some(item => item.id === 'wedding-ceremony') && (
                <CartItem style={{ opacity: 0.7 }}>
                  <ItemDetails>
                    <ItemName>Wedding (Required)</ItemName>
                    <ItemPrice>{formatPrice(25000)}</ItemPrice>
                  </ItemDetails>
                </CartItem>
              )}
              
              {numKids > 0 && (
                <CartItem style={{ opacity: 0.7 }}>
                  <ItemDetails>
                    <ItemName>Private School Tuition × {numKids}</ItemName>
                    <ItemPrice>{formatPrice(35000)} per child</ItemPrice>
                  </ItemDetails>
                </CartItem>
              )}
            </CartItems>
          )}
        </DrawerContent>
        
        <DrawerFooter>
          <TotalsBreakdown>
            <div>
              <span>Subtotal</span>
              <span>{formatPrice(totals.subtotal)}</span>
            </div>
            {totals.marriedMultiplier > 1 && (
              <div>
                <span>Married (×{totals.marriedMultiplier})</span>
                <span>{formatPrice(totals.multipliedTotal)}</span>
              </div>
            )}
            <div>
              <span>Fees (10%)</span>
              <span>{formatPrice(totals.fees)}</span>
            </div>
            <div className="total">
              <span>TOTAL</span>
              <span>{formatPrice(totals.total)}</span>
            </div>
          </TotalsBreakdown>
          
          <FooterActions>
            <ActionButton primary onClick={handleScreenshot} disabled={cart.length === 0}>
              {tokens.components.button.copies.placeOrder}
            </ActionButton>
            <ActionButton onClick={handleShare} disabled={cart.length === 0}>
              {tokens.components.button.copies.share}
            </ActionButton>
            <ActionButton onClick={onClearCart} disabled={cart.length === 0}>
              Clear Cart
            </ActionButton>
          </FooterActions>
        </DrawerFooter>
      </Drawer>
      
      {/* Hidden receipt for screenshot */}
      <Receipt ref={receiptRef}>
        <h1>BARE MINIMUM</h1>
        <div>
          Order #{Math.random().toString(36).substr(2, 9).toUpperCase()}
          <br />
          {new Date().toLocaleDateString()}
        </div>
        
        <div className="divider" />
        
        {cart.map(cartItem => {
          const item = itemsMap.get(cartItem.id);
          if (!item) return null;
          
          const itemPrice = calculateItemPrice(item, isMarried, numKids);
          
          return (
            <div key={cartItem.id} className="item">
              <span>{cartItem.quantity}x {item.name}</span>
              <span>{formatPrice(itemPrice * cartItem.quantity)}</span>
            </div>
          );
        })}
        
        {/* Forced items */}
        {isMarried && !cart.some(item => item.id === 'engagement-ring') && (
          <div className="item">
            <span>1x Engagement Ring</span>
            <span>{formatPrice(15000)}</span>
          </div>
        )}
        
        {isMarried && !cart.some(item => item.id === 'wedding-ceremony') && (
          <div className="item">
            <span>1x Wedding</span>
            <span>{formatPrice(25000)}</span>
          </div>
        )}
        
        {numKids > 0 && (
          <div className="item">
            <span>{numKids}x Private School</span>
            <span>{formatPrice(35000 * numKids)}</span>
          </div>
        )}
        
        <div className="total-section">
          <div className="item">
            <span>Subtotal</span>
            <span>{formatPrice(totals.subtotal)}</span>
          </div>
          {totals.marriedMultiplier > 1 && (
            <div className="item">
              <span>Married ×2</span>
              <span>{formatPrice(totals.multipliedTotal)}</span>
            </div>
          )}
          <div className="item">
            <span>Fees</span>
            <span>{formatPrice(totals.fees)}</span>
          </div>
          <div className="item total">
            <span>TOTAL</span>
            <span>{formatPrice(totals.total)}</span>
          </div>
        </div>
        
        <div className="footer">
          bareminimum.xyz<br />
          Your bare minimum lifestyle calculator
        </div>
      </Receipt>
    </>
  );
}

export default CartDrawer;