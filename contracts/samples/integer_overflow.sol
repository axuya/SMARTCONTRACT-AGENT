// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract IntegerArithmeticExample {
    uint256 public total;

    function addUnchecked(uint256 amount) external {
        unchecked {
            total += amount;
        }
    }
}

