# VS Code Extension Publishing Guide

This guide covers publishing the Cursor ETA Indicator VS Code extension to Open VSX and VS Code Marketplace.

## Prerequisites

1. **Open VSX Account**: https://open-vsx.org/
2. **VS Code Publisher Account**: https://marketplace.visualstudio.com/manage
3. **GitHub repository secrets configured**

## Required Secrets

Add these secrets in GitHub repository settings:

### Open VSX Token
1. Sign in to https://open-vsx.org/
2. Go to Settings → Access Tokens
3. Generate new token with "Publish" scope
4. Add as `OVSX_TOKEN` in GitHub secrets

### VS Code Marketplace Token
1. Sign in to https://dev.azure.com/
2. Go to User Settings → Personal Access Tokens
3. Create token with:
   - Organization: All accessible organizations
   - Scopes: Marketplace → Manage
4. Add as `VSCODE_MARKETPLACE_TOKEN` in GitHub secrets

## Publisher Setup

### Creating a Publisher

1. **Open VSX**:
   - Go to https://open-vsx.org/user-settings/namespaces
   - Create namespace: `cursor-eta`

2. **VS Code Marketplace**:
   - Go to https://marketplace.visualstudio.com/manage
   - Create publisher: `cursor-eta`
   - Display name: "Cursor ETA"

## Publishing Process

### Automatic Publishing

1. **Update version** in `vscode-extension/package.json`

2. **Commit and tag**:
   ```bash
   git add -A
   git commit -m "Release VS Code extension v0.1.0"
   git tag v0.1.0
   git push && git push --tags
   ```

3. **GitHub Actions** automatically:
   - Builds the extension
   - Tests on multiple platforms
   - Publishes to Open VSX
   - Publishes to VS Code Marketplace (optional)
   - Creates GitHub release with VSIX

### Manual Publishing

#### Build locally:
```bash
cd vscode-extension
npm install
npm run compile
vsce package
```

#### Publish to Open VSX:
```bash
# Install ovsx CLI
npm install -g ovsx

# Publish (requires token)
ovsx publish cursor-eta-0.1.0.vsix -p <token>

# Or with stored token
ovsx publish
```

#### Publish to VS Code Marketplace:
```bash
# Install vsce CLI
npm install -g @vscode/vsce

# Publish (requires token)
vsce publish --packagePath cursor-eta-0.1.0.vsix -p <token>

# Or with stored token
vsce publish
```

## Extension Configuration

### Required Fields

Ensure `package.json` contains:
- `name`: Must match publisher.extension format
- `displayName`: Human-readable name
- `description`: Clear description
- `version`: Semantic version
- `publisher`: Your publisher ID
- `icon`: 128x128 PNG icon
- `repository`: GitHub repository
- `license`: License type

### Recommended Fields
- `categories`: Help users find extension
- `keywords`: Search terms
- `galleryBanner`: Marketplace appearance
- `badges`: Build status, version, etc.

## Testing

### Local Testing
```bash
# Install locally
code --install-extension cursor-eta-0.1.0.vsix

# Test
code --list-extensions | grep cursor-eta
```

### Pre-release Testing
1. Publish to Open VSX first
2. Test installation: `code --install-extension cursor-eta.cursor-eta`
3. Verify functionality
4. Then publish to VS Code Marketplace

## Troubleshooting

### "Publisher not found"
- Ensure publisher exists on target platform
- Verify `publisher` field matches exactly

### "Invalid extension ID"
- ID must be lowercase
- Format: `publisher.extension-name`
- No spaces or special characters

### "Missing required fields"
- Check all required fields in package.json
- Validate with: `vsce ls`

### Icon issues
- Must be exactly 128x128 pixels
- PNG format only
- File must exist at path specified

## Version Management

- Extension version independent of Python package
- Can release extension updates without Python changes
- Use same version when releasing together

## Quick Commands

```bash
# Check package validity
vsce ls

# Package extension
vsce package

# Show package contents
vsce show cursor-eta-0.1.0.vsix

# Publish to Open VSX
ovsx publish *.vsix -p $OVSX_TOKEN

# Publish to VS Code Marketplace  
vsce publish --packagePath *.vsix -p $VSCE_PAT
```

## Security Notes

- Never commit tokens
- Use GitHub secrets for CI/CD
- Rotate tokens periodically
- Use minimal required scopes