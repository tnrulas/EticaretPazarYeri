import React from 'react'
import { useSelector } from 'react-redux';
import { useNavigate } from 'react-router-dom';

function Navbar() {
    const navigate = useNavigate();

    const isSeller = localStorage.getItem('is_seller') === 'true';

    return (
        <nav style={{ display: 'flex', justifyContent: 'space-between', padding: '10px', background: '#eee' }}>
            <h2 onClick={() => navigate('/')} style={{ cursor: 'pointer', margin: 0 }}>
                Benim E-ticaret Sitem
            </h2>
            <div>
                <span onClick={() => navigate('/sepet')}>Sepetim</span>
                {isSeller && (
                    <span
                        onClick={() => navigate('/ekle')}
                    >
                        Ürün Ekle
                    </span>
                )}
            </div>
        </nav>
    )
}

export default Navbar;