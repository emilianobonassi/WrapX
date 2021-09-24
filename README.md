# WrapX

Supercharge your NFTs with new behaviours and superpowers!

WrapX is a collection of Wrappers (currently one - WrapXSet) to decorate your NTFs adding new capabilities

NFTs exist outside any chain, smart contracts are just projections/representations/slices which sometimes are limiting their full potential

This means that wrappers allow multiple legitimate representations of NFTs

Wrappers are means to supercharge NFT actions and capabilities

**NB: WrapX is currently EXPERIMENTAL and NOT AUDITED/REVIEWED. Do Your Own Research and Use At Your Own Risk.**

## Use-cases

1. NFTs can hold other NFTs and execute actions on their own (WrapXSet leveraging NFTSet tech)
2. ...


## How to use

### Create an WrapXSet
You will own a new ERC721 with the symbol and the name you specified at `tokenId = 0`

### Deposit assets
Just transfer ERC20, ERC721, ERC1155 and ETH to the desidered WrapXSet address.

### Wrap your main NFT
Use `setWrappedToken(address tokenAddress, uint256 tokenId)`, automagically your WrapXSet will inherit all the properties of your original NFT plus the capability to hold other assets and execute transactions.

### Withdraw assets
Based on the category of asset you want to withdraw call on your WrapXSet respectively:
- `withdrawERC721(address tokenAddress, uint256 tokenId)` or `safeWithdrawERC721(address tokenAddress, uint256 tokenId)`
- `withdrawERC1155(address tokenAddress, uint256 tokenId, uint256 amount, bytes memory data)`
- `withdrawERC20(address tokenAddress, uint256 amount)`
- `withdrawETH(uint256 amount)`

These methods can be called only by the owner (or the approved spenders).

### Transfer ownership
Your WrapXSet is an NFT, technically the owner is the holder of the `tokenId = 0`. Transfer that id to the new desidered owner and you are done. Transfering a smart-wallet has never been easier!

`transferFrom(currentOwner, newOwner, 0)`

### Use your WrapXSet as a smart wallet
Your WrapXSet add smart-wallet capabilities to your NFT so you can interact with other smart-contracts. You can execute a generic transaction via

```
execute(
    address to,
    uint256 value,
    bytes memory data,
    bool isDelegateCall,
    uint256 txGas
)
```

e.g. Your WrapXSet can lend its tokens to Aave or Compound

### DISCLAIMER: Approved spenders
As soon as you approve your WrapXSet to someone else, it can not only transfer your WrapXSet but also withdraw the tokens inside of it!
Consider carefully when you delegate these rights, it can be useful (e.g. cold/hot wallet) but can be harmful.