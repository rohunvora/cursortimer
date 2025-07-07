// Design Tokens - Amazon Brutalist Style
// Locked visual constants for bareminimum.xyz

export const tokens = {
  // Typography
  fonts: {
    primary: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif',
    mono: 'Consolas, Monaco, "Andale Mono", "Ubuntu Mono", monospace'
  },
  
  fontSizes: {
    large: '28px',    // Headers, prices
    base: '14px',     // Body text, item names
    small: '12px'     // Metadata, captions
  },
  
  fontWeights: {
    normal: 400,
    bold: 700
  },
  
  // Spacing (8pt grid)
  spacing: {
    xs: '4px',
    sm: '8px',
    md: '16px',
    lg: '24px',
    xl: '32px',
    xxl: '48px'
  },
  
  // Colors
  colors: {
    black: '#000000',
    white: '#FFFFFF',
    gray: {
      100: '#F7F7F7',
      200: '#E5E5E5',
      300: '#D4D4D4',
      400: '#A3A3A3',
      500: '#737373',
      600: '#525252',
      700: '#404040',
      800: '#262626',
      900: '#171717'
    },
    accent: '#FF9500',  // Amazon-like orange for CTAs
    error: '#DC2626',
    success: '#16A34A'
  },
  
  // Borders
  borders: {
    thin: '1px solid',
    thick: '2px solid',
    radius: {
      none: '0px',
      small: '2px',
      medium: '4px'
    }
  },
  
  // Layout
  layout: {
    maxWidth: '1200px',
    gridGap: '16px',
    containerPadding: '16px'
  },
  
  // Components
  components: {
    button: {
      height: '40px',
      padding: '0 24px',
      fontSize: '14px',
      fontWeight: 700,
      borderWidth: '2px',
      copies: {
        addToCart: 'ADD TO CART',
        placeOrder: 'PLACE ORDER', 
        surpriseMe: 'SURPRISE ME',
        removeFromCart: 'REMOVE',
        share: 'SHARE RECEIPT'
      }
    },
    
    input: {
      height: '40px',
      padding: '0 12px',
      fontSize: '14px',
      borderWidth: '1px'
    },
    
    card: {
      padding: '16px',
      borderWidth: '1px',
      aspectRatio: '1 / 1'  // Square product cards
    },
    
    receipt: {
      width: '400px',
      padding: '24px',
      fontSize: '12px',
      lineHeight: 1.5
    },
    
    drawer: {
      width: '400px',
      padding: '24px'
    }
  },
  
  // Animations
  transitions: {
    fast: '150ms ease',
    medium: '250ms ease',
    slow: '350ms ease'
  },
  
  // Z-index scale
  zIndex: {
    base: 0,
    dropdown: 10,
    sticky: 20,
    drawer: 30,
    modal: 40,
    tooltip: 50
  }
};

// CSS Reset for brutalist aesthetic
export const globalStyles = `
  * {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
  }
  
  body {
    font-family: ${tokens.fonts.primary};
    font-size: ${tokens.fontSizes.base};
    line-height: 1.5;
    color: ${tokens.colors.black};
    background: ${tokens.colors.white};
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
  }
  
  button {
    font-family: inherit;
    cursor: pointer;
    border: none;
    background: none;
  }
  
  input, select, textarea {
    font-family: inherit;
    font-size: inherit;
  }
  
  img {
    display: block;
    max-width: 100%;
    height: auto;
  }
  
  a {
    color: inherit;
    text-decoration: none;
  }
  
  /* Utility classes */
  .mono {
    font-family: ${tokens.fonts.mono};
  }
  
  .uppercase {
    text-transform: uppercase;
    letter-spacing: 0.05em;
  }
  
  .truncate {
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }
  
  .no-select {
    user-select: none;
    -webkit-user-select: none;
  }
  
  /* Focus styles */
  *:focus {
    outline: 2px solid ${tokens.colors.black};
    outline-offset: 2px;
  }
  
  *:focus:not(:focus-visible) {
    outline: none;
  }
`;

// Component style generators
export const buttonStyles = {
  primary: `
    height: ${tokens.components.button.height};
    padding: ${tokens.components.button.padding};
    font-size: ${tokens.components.button.fontSize};
    font-weight: ${tokens.components.button.fontWeight};
    background: ${tokens.colors.black};
    color: ${tokens.colors.white};
    border: ${tokens.components.button.borderWidth} solid ${tokens.colors.black};
    text-transform: uppercase;
    letter-spacing: 0.05em;
    transition: all ${tokens.transitions.fast};
    
    &:hover {
      background: ${tokens.colors.white};
      color: ${tokens.colors.black};
    }
    
    &:active {
      transform: translateY(1px);
    }
    
    &:disabled {
      opacity: 0.5;
      cursor: not-allowed;
    }
  `,
  
  secondary: `
    height: ${tokens.components.button.height};
    padding: ${tokens.components.button.padding};
    font-size: ${tokens.components.button.fontSize};
    font-weight: ${tokens.components.button.fontWeight};
    background: ${tokens.colors.white};
    color: ${tokens.colors.black};
    border: ${tokens.components.button.borderWidth} solid ${tokens.colors.black};
    text-transform: uppercase;
    letter-spacing: 0.05em;
    transition: all ${tokens.transitions.fast};
    
    &:hover {
      background: ${tokens.colors.gray[100]};
    }
    
    &:active {
      transform: translateY(1px);
    }
  `,
  
  danger: `
    height: 32px;
    padding: 0 16px;
    font-size: ${tokens.fontSizes.small};
    font-weight: ${tokens.fontWeights.bold};
    background: ${tokens.colors.white};
    color: ${tokens.colors.error};
    border: 1px solid ${tokens.colors.error};
    text-transform: uppercase;
    transition: all ${tokens.transitions.fast};
    
    &:hover {
      background: ${tokens.colors.error};
      color: ${tokens.colors.white};
    }
  `
};

export default tokens;