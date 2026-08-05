import React from 'react'
import { useSelector } from 'react-redux';

function Navbar() {
    const cartItems = useSelector((state) => state.cart.cartItems)

    const cartCount = cartItems.length;

    return (
        <nav style={{ display: 'flex', justifyContent: 'space-between', padding: '10px', background: '#eee' }}>
            <h2>Benim E-ticaret Sitem</h2>
            <div>
                <span>Sepetim: ({cartCount})</span>
            </div>
        </nav>
    )
}

export default Navbar;