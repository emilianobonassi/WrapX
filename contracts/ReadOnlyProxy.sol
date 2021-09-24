// SPDX-License-Identifier: Unlicense

pragma solidity ^0.8.0;

abstract contract ReadOnlyProxy {
    function getTarget() external virtual returns (address) {
        return _getTarget();
    }

    function _getTarget() internal virtual returns (address);

    fallback() external virtual {
        address _target = _getTarget();

        assembly {
            let free_ptr := mload(0x40)
            calldatacopy(free_ptr, 0, calldatasize())

            let result := staticcall(gas(), _target, free_ptr, calldatasize(), 0, 0)
            returndatacopy(free_ptr, 0, returndatasize())

            if iszero(result) {
                revert(free_ptr, returndatasize())
            }
            return(free_ptr, returndatasize())
        }
    }
}
