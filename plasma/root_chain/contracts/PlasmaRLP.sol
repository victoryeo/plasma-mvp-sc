pragma solidity ^0.4.0;

import "./RLPDecode.sol";


library PlasmaRLP {

    struct exitingTx {
        address exitor;
        address token;
        uint256 amount;
        uint256 inputCount;
        bytes dmapping;
    }

    /* Public Functions */

    function getUtxoPos(bytes memory challengingTxBytes, uint256 oIndex)
        internal
        constant
        returns (uint256)
    {
        var txList = RLPDecode.toList(RLPDecode.toRlpItem(challengingTxBytes));
        uint256 oIndexShift = oIndex * 3;
        return
            RLPDecode.toUint(txList[0 + oIndexShift]) * 1000000000 +
            RLPDecode.toUint(txList[1 + oIndexShift]) * 10000 +
            RLPDecode.toUint(txList[2 + oIndexShift]);
    }

    function createExitingTx(bytes memory exitingTxBytes, uint256 oindex)
        internal
        constant
        returns (exitingTx)
    {
        var txList = RLPDecode.toList(RLPDecode.toRlpItem(exitingTxBytes));
        return exitingTx({
            /* exitor is param number 7, newowner1 of Transaction */
            exitor: RLPDecode.toAddress(txList[7 + 2 * oindex]),
            /* token is param number 6, cur12 of Transaction */
            token: RLPDecode.toAddress(txList[6]),
            /* amount is param number 8, amount1 of Transaction */
            amount: RLPDecode.toUint(txList[8 + 2 * oindex]),
            inputCount: RLPDecode.toUint(txList[0]) * RLPDecode.toUint(txList[3]),
            dmapping: RLPDecode.toBytes(txList[12])
        });
    }
}
