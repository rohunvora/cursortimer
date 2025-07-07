import React from 'react';
import styled from 'styled-components';
import tokens from '../design-tokens';
import { calculateItemPrice, formatPrice } from '../utils/calculations';

const Grid = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: ${tokens.layout.gridGap};
  margin-bottom: ${tokens.spacing.xxl};
`;

const ProductCard = styled.div`
  border: ${tokens.components.card.borderWidth} solid ${tokens.colors.black};
  background: ${tokens.colors.white};
  overflow: hidden;
  display: flex;
  flex-direction: column;
  transition: all ${tokens.transitions.fast};
  
  &:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  }
`;

const ImageContainer = styled.div`
  position: relative;
  aspect-ratio: ${tokens.components.card.aspectRatio};
  background: ${tokens.colors.gray[100]};
  overflow: hidden;
  border-bottom: ${tokens.borders.thin} ${tokens.colors.black};
`;

const ProductImage = styled.img`
  width: 100%;
  height: 100%;
  object-fit: cover;
`;

const ImagePlaceholder = styled.div`
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: ${tokens.fontSizes.small};
  color: ${tokens.colors.gray[500]};
  text-transform: uppercase;
  letter-spacing: 0.05em;
`;

const ProductInfo = styled.div`
  padding: ${tokens.components.card.padding};
  flex: 1;
  display: flex;
  flex-direction: column;
`;

const ProductName = styled.h3`
  font-size: ${tokens.fontSizes.base};
  font-weight: ${tokens.fontWeights.bold};
  margin: 0 0 ${tokens.spacing.xs} 0;
  line-height: 1.3;
`;

const ProductCategory = styled.span`
  font-size: ${tokens.fontSizes.small};
  color: ${tokens.colors.gray[600]};
  text-transform: uppercase;
  letter-spacing: 0.05em;
  margin-bottom: ${tokens.spacing.sm};
`;

const PriceContainer = styled.div`
  margin-top: auto;
  padding-top: ${tokens.spacing.sm};
`;

const Price = styled.div`
  font-size: ${tokens.fontSizes.large};
  font-weight: ${tokens.fontWeights.bold};
  font-family: ${tokens.fonts.mono};
  margin-bottom: ${tokens.spacing.xs};
`;

const PriceVariants = styled.div`
  font-size: ${tokens.fontSizes.small};
  color: ${tokens.colors.gray[600]};
  line-height: 1.4;
`;

const AddButton = styled.button`
  width: 100%;
  height: ${tokens.components.button.height};
  font-size: ${tokens.components.button.fontSize};
  font-weight: ${tokens.components.button.fontWeight};
  background: ${tokens.colors.black};
  color: ${tokens.colors.white};
  border: none;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  transition: all ${tokens.transitions.fast};
  cursor: pointer;
  margin-top: ${tokens.spacing.md};
  
  &:hover {
    background: ${tokens.colors.gray[800]};
  }
  
  &:active {
    transform: translateY(1px);
  }
  
  &:disabled {
    background: ${tokens.colors.gray[400]};
    cursor: not-allowed;
  }
`;

const InCartBadge = styled.div`
  position: absolute;
  top: ${tokens.spacing.sm};
  right: ${tokens.spacing.sm};
  background: ${tokens.colors.accent};
  color: ${tokens.colors.white};
  padding: 4px 8px;
  font-size: ${tokens.fontSizes.small};
  font-weight: ${tokens.fontWeights.bold};
  border-radius: ${tokens.borders.radius.small};
`;

function ProductGrid({ items, cart, onAddToCart, isMarried, numKids }) {
  const getItemQuantityInCart = (itemId) => {
    const cartItem = cart.find(item => item.id === itemId);
    return cartItem ? cartItem.quantity : 0;
  };
  
  return (
    <Grid>
      {items.map(item => {
        const inCart = getItemQuantityInCart(item.id);
        const displayPrice = calculateItemPrice(item, isMarried, numKids);
        
        return (
          <ProductCard key={item.id}>
            <ImageContainer>
              {item.img_url ? (
                <ProductImage 
                  src={item.img_url} 
                  alt={item.name}
                  loading="lazy"
                  onError={(e) => {
                    e.target.style.display = 'none';
                    e.target.nextSibling.style.display = 'flex';
                  }}
                />
              ) : null}
              <ImagePlaceholder style={{ display: item.img_url ? 'none' : 'flex' }}>
                No Image
              </ImagePlaceholder>
              {inCart > 0 && (
                <InCartBadge>In Cart ({inCart})</InCartBadge>
              )}
            </ImageContainer>
            
            <ProductInfo>
              <ProductName>{item.name}</ProductName>
              <ProductCategory>{item.category.replace('-', ' ')}</ProductCategory>
              
              <PriceContainer>
                <Price>{formatPrice(displayPrice)}</Price>
                <PriceVariants>
                  {item.spouse_variant_price && (
                    <div>+ Spouse: {formatPrice(item.spouse_variant_price)}</div>
                  )}
                  {item.kid_variant_price && (
                    <div>+ Per kid: {formatPrice(item.kid_variant_price)}</div>
                  )}
                </PriceVariants>
              </PriceContainer>
              
              <AddButton onClick={() => onAddToCart(item.id)}>
                {tokens.components.button.copies.addToCart}
              </AddButton>
            </ProductInfo>
          </ProductCard>
        );
      })}
    </Grid>
  );
}

export default ProductGrid;