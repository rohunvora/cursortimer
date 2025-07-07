import React from 'react';
import styled from 'styled-components';
import tokens from '../design-tokens';
import { formatPrice } from '../utils/calculations';

const HeaderContainer = styled.header`
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  background: ${tokens.colors.white};
  border-bottom: ${tokens.borders.thick} ${tokens.colors.black};
  z-index: ${tokens.zIndex.sticky};
`;

const HeaderContent = styled.div`
  max-width: ${tokens.layout.maxWidth};
  margin: 0 auto;
  padding: ${tokens.spacing.md} ${tokens.layout.containerPadding};
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: ${tokens.spacing.lg};
  
  @media (max-width: 768px) {
    flex-wrap: wrap;
  }
`;

const Logo = styled.h1`
  font-size: ${tokens.fontSizes.large};
  font-weight: ${tokens.fontWeights.bold};
  text-transform: uppercase;
  letter-spacing: -0.02em;
  margin: 0;
  flex-shrink: 0;
`;

const Controls = styled.div`
  display: flex;
  align-items: center;
  gap: ${tokens.spacing.md};
  flex: 1;
  
  @media (max-width: 768px) {
    width: 100%;
    flex-wrap: wrap;
  }
`;

const SearchInput = styled.input`
  height: ${tokens.components.input.height};
  padding: ${tokens.components.input.padding};
  font-size: ${tokens.components.input.fontSize};
  border: ${tokens.components.input.borderWidth} solid ${tokens.colors.black};
  background: ${tokens.colors.white};
  flex: 1;
  max-width: 300px;
  
  &::placeholder {
    color: ${tokens.colors.gray[500]};
  }
`;

const CategorySelect = styled.select`
  height: ${tokens.components.input.height};
  padding: ${tokens.components.input.padding};
  font-size: ${tokens.components.input.fontSize};
  border: ${tokens.components.input.borderWidth} solid ${tokens.colors.black};
  background: ${tokens.colors.white};
  cursor: pointer;
  text-transform: capitalize;
`;

const Button = styled.button`
  height: ${tokens.components.button.height};
  padding: ${tokens.components.button.padding};
  font-size: ${tokens.components.button.fontSize};
  font-weight: ${tokens.components.button.fontWeight};
  background: ${props => props.primary ? tokens.colors.black : tokens.colors.white};
  color: ${props => props.primary ? tokens.colors.white : tokens.colors.black};
  border: ${tokens.components.button.borderWidth} solid ${tokens.colors.black};
  text-transform: uppercase;
  letter-spacing: 0.05em;
  transition: all ${tokens.transitions.fast};
  cursor: pointer;
  white-space: nowrap;
  
  &:hover {
    background: ${props => props.primary ? tokens.colors.white : tokens.colors.gray[100]};
    color: ${props => props.primary ? tokens.colors.black : tokens.colors.black};
  }
  
  &:active {
    transform: translateY(1px);
  }
`;

const CartButton = styled(Button)`
  display: flex;
  align-items: center;
  gap: ${tokens.spacing.sm};
`;

const CartCount = styled.span`
  background: ${tokens.colors.accent};
  color: ${tokens.colors.white};
  padding: 2px 6px;
  border-radius: ${tokens.borders.radius.small};
  font-size: ${tokens.fontSizes.small};
  min-width: 20px;
  text-align: center;
`;

const TotalAmount = styled.span`
  font-family: ${tokens.fonts.mono};
`;

function Header({
  cartCount,
  total,
  onCartClick,
  searchQuery,
  onSearchChange,
  selectedCategory,
  onCategoryChange,
  categories,
  onSurpriseMe
}) {
  return (
    <HeaderContainer>
      <HeaderContent>
        <Logo>Bare Minimum</Logo>
        
        <Controls>
          <SearchInput
            type="text"
            placeholder="Search items..."
            value={searchQuery}
            onChange={(e) => onSearchChange(e.target.value)}
          />
          
          <CategorySelect
            value={selectedCategory}
            onChange={(e) => onCategoryChange(e.target.value)}
          >
            {categories.map(category => (
              <option key={category} value={category}>
                {category === 'all' ? 'All Categories' : category.replace('-', ' ')}
              </option>
            ))}
          </CategorySelect>
          
          <Button onClick={onSurpriseMe}>
            {tokens.components.button.copies.surpriseMe}
          </Button>
        </Controls>
        
        <CartButton primary onClick={onCartClick}>
          <span>Cart</span>
          {cartCount > 0 && <CartCount>{cartCount}</CartCount>}
          <TotalAmount>{formatPrice(total)}</TotalAmount>
        </CartButton>
      </HeaderContent>
    </HeaderContainer>
  );
}

export default Header;